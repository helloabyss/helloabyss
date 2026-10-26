import { bech32 } from '@scure/base';

/**
 * Lightning payout destinations. Users bring their own wallet; we never hold keys.
 *
 *  - Lightning Address (LUD-16): user@domain → https://domain/.well-known/lnurlp/user
 *  - LNURL-pay (LUD-06): bech32 "lnurl1..." string
 *  - BOLT11 invoice: one-off withdrawal for an exact amount
 */

export type Destination =
  | { type: 'lightning-address'; value: string; user: string; domain: string }
  | { type: 'lnurl'; value: string }
  | { type: 'bolt11'; value: string; network: 'mainnet' | 'testnet' | 'signet' | 'regtest'; amountMsat: number | null };

export class DestinationError extends Error {
  override name = 'DestinationError';
}

const ADDRESS_RE = /^([a-z0-9\-_.+]+)@([a-z0-9-]+(?:\.[a-z0-9-]+)+)$/i;

export function parseDestination(raw: string): Destination {
  const value = raw.trim().replace(/^lightning:/i, '');
  const lower = value.toLowerCase();
  const addr = ADDRESS_RE.exec(lower);
  if (addr) return { type: 'lightning-address', value: lower, user: addr[1]!, domain: addr[2]! };
  if (lower.startsWith('lnurl1')) return { type: 'lnurl', value: lower };
  const inv = /^ln(bcrt|tbs|tb|bc)(\d+[munp]?)?1[02-9ac-hj-np-z]+$/.exec(lower);
  if (inv) {
    const network = ({ bc: 'mainnet', tb: 'testnet', tbs: 'signet', bcrt: 'regtest' } as const)[inv[1] as 'bc'];
    return { type: 'bolt11', value: lower, network, amountMsat: inv[2] ? bolt11AmountMsat(inv[2]) : null };
  }
  throw new DestinationError('Enter a Lightning address (name@wallet.com), an LNURL, or a Lightning invoice.');
}

/** BOLT11 human-readable amount → msat. "2500u" = 2500 µBTC = 250,000 sats. */
export function bolt11AmountMsat(amt: string): number {
  const m = /^(\d+)([munp]?)$/.exec(amt);
  if (!m) throw new DestinationError('Bad invoice amount');
  const n = BigInt(m[1]!);
  // 1 BTC = 1e11 msat
  const msat: Record<string, bigint> = {
    '': n * 100_000_000_000n,
    m: n * 100_000_000n,
    u: n * 100_000n,
    n: n * 100n,
    p: n / 10n,
  };
  if (m[2] === 'p' && n % 10n !== 0n) throw new DestinationError('Invoice amount has sub-msat precision');
  return Number(msat[m[2]!]);
}

export interface LnurlPayParams {
  callback: string;
  minSendable: number; // msat
  maxSendable: number; // msat
  metadata: string;
  commentAllowed?: number;
}

/** LUD-16: resolve a Lightning Address to LNURL-pay parameters. Used to validate on save. */
export async function resolveLightningAddress(
  d: Extract<Destination, { type: 'lightning-address' }>,
  fetchImpl: typeof fetch = fetch,
): Promise<LnurlPayParams> {
  const url = `https://${d.domain}/.well-known/lnurlp/${encodeURIComponent(d.user)}`;
  let res: Response;
  try {
    res = await fetchImpl(url, { headers: { accept: 'application/json' } });
  } catch {
    throw new DestinationError(`Couldn't reach ${d.domain}. Check the address or try again.`);
  }
  if (!res.ok) throw new DestinationError(`${d.domain} doesn't recognise "${d.user}".`);
  return parsePayParams(await res.json());
}

function parsePayParams(raw: unknown): LnurlPayParams {
  const j = raw as Partial<LnurlPayParams> & { tag?: string; status?: string; reason?: string };
  if (j.status === 'ERROR') throw new DestinationError(j.reason ?? 'Wallet returned an error');
  if (j.tag !== 'payRequest' || !j.callback || !j.minSendable || !j.maxSendable) {
    throw new DestinationError('That address is not a Lightning payment address.');
  }
  if (!j.callback.startsWith('https://') && !j.callback.includes('.onion')) {
    throw new DestinationError('Wallet callback must be HTTPS');
  }
  return {
    callback: j.callback,
    minSendable: j.minSendable,
    maxSendable: j.maxSendable,
    metadata: j.metadata ?? '[]',
    commentAllowed: j.commentAllowed,
  };
}

/** LUD-06 step 2: ask the wallet's server for an invoice of `amountMsat`. Coordinator-side. */
export async function fetchInvoice(
  params: LnurlPayParams,
  amountMsat: number,
  comment?: string,
  fetchImpl: typeof fetch = fetch,
): Promise<string> {
  if (amountMsat < params.minSendable || amountMsat > params.maxSendable) {
    throw new DestinationError(
      `Wallet accepts ${Math.ceil(params.minSendable / 1000)}–${Math.floor(params.maxSendable / 1000)} sats per payment.`,
    );
  }
  const u = new URL(params.callback);
  u.searchParams.set('amount', String(amountMsat));
  if (comment && params.commentAllowed) u.searchParams.set('comment', comment.slice(0, params.commentAllowed));
  const res = await fetchImpl(u.toString());
  const j = (await res.json()) as { pr?: string; status?: string; reason?: string };
  if (j.status === 'ERROR' || !j.pr) throw new DestinationError(j.reason ?? 'Wallet did not return an invoice');
  const parsed = parseDestination(j.pr);
  if (parsed.type !== 'bolt11' || parsed.amountMsat !== amountMsat) {
    throw new DestinationError('Wallet returned an invoice for the wrong amount');
  }
  return j.pr;
}

/** LUD-01: decode a bech32 "lnurl1..." string to its HTTPS URL. */
export function decodeLnurl(lnurl: string): string {
  try {
    const { prefix, words } = bech32.decode(lnurl.toLowerCase() as `${string}1${string}`, 2000);
    if (prefix !== 'lnurl') throw new Error('prefix');
    // URLs inside LNURLs are ASCII; avoid TextDecoder (missing on some RN engines).
    const bytes = bech32.fromWords(words);
    if (bytes.some((b) => b > 0x7e || b < 0x20)) throw new Error('non-ascii');
    const url = String.fromCharCode(...bytes);
    if (!url.startsWith('https://') && !/^http:\/\/[^/]+\.onion/.test(url)) throw new Error('scheme');
    return url;
  } catch {
    throw new DestinationError('That LNURL is not valid.');
  }
}

/** Resolve any LNURL-pay capable destination (address or lnurl string). */
export async function resolvePayParams(d: Destination, fetchImpl: typeof fetch = fetch): Promise<LnurlPayParams> {
  if (d.type === 'lightning-address') return resolveLightningAddress(d, fetchImpl);
  if (d.type !== 'lnurl') throw new DestinationError('Invoices are paid directly, not resolved.');
  const res = await fetchImpl(decodeLnurl(d.value)).catch(() => {
    throw new DestinationError("Couldn't reach the wallet behind that LNURL.");
  });
  return parsePayParams(await res.json());
}

export function maskDestination(v: string): string {
  if (v.includes('@')) return v;
  return v.length > 24 ? `${v.slice(0, 12)}…${v.slice(-8)}` : v;
}
