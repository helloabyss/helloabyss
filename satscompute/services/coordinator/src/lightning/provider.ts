import { randomBytes, createHash } from 'node:crypto';

/**
 * Outbound Lightning payments from the platform node to users' own wallets.
 *
 * Implementations:
 *  - MockLightningProvider: dev only.
 *  - LndRestProvider: any LND node over REST — Voltage-hosted nodes work as-is.
 *  - Lightspark / other: implement this interface with their SDK.
 */
export interface PaymentResult {
  preimageHex: string;
  paymentHashHex: string;
  feeSats: number;
}

export interface LightningProvider {
  readonly name: string;
  /** Pays a BOLT11 invoice. `amountSats` is only sent for zero-amount invoices. Throws on failure. */
  payInvoice(bolt11: string, opts: { maxFeeSats: number; amountSats?: number; timeoutSeconds?: number }): Promise<PaymentResult>;
}

export class LightningPaymentError extends Error {
  override name = 'LightningPaymentError';
}

export class MockLightningProvider implements LightningProvider {
  readonly name = 'mock';
  async payInvoice(bolt11: string): Promise<PaymentResult> {
    if (bolt11.endsWith('zzzz')) throw new LightningPaymentError('mock: no route');
    const pre = randomBytes(32);
    return { preimageHex: pre.toString('hex'), paymentHashHex: createHash('sha256').update(pre).digest('hex'), feeSats: 0 };
  }
}

const b64ToHex = (b: string) => Buffer.from(b, 'base64').toString('hex');

/** LND REST SendPaymentSync: POST /v1/channels/transactions. */
export class LndRestProvider implements LightningProvider {
  readonly name = 'lnd';
  constructor(
    private readonly restUrl: string,
    private readonly macaroonHex: string,
    private readonly fetchImpl: typeof fetch = fetch,
  ) {}

  async payInvoice(bolt11: string, opts: { maxFeeSats: number; amountSats?: number; timeoutSeconds?: number }): Promise<PaymentResult> {
    const res = await this.fetchImpl(`${this.restUrl.replace(/\/$/, '')}/v1/channels/transactions`, {
      method: 'POST',
      headers: { 'Grpc-Metadata-macaroon': this.macaroonHex, 'content-type': 'application/json' },
      body: JSON.stringify({
        payment_request: bolt11,
        fee_limit: { fixed: String(opts.maxFeeSats) },
        ...(opts.amountSats ? { amt: String(opts.amountSats) } : {}),
      }),
      signal: AbortSignal.timeout((opts.timeoutSeconds ?? 60) * 1000),
    });
    const j = (await res.json().catch(() => ({}))) as {
      payment_error?: string;
      payment_preimage?: string;
      payment_hash?: string;
      payment_route?: { total_fees?: string };
      message?: string;
    };
    if (!res.ok) throw new LightningPaymentError(j.message ?? `LND HTTP ${res.status}`);
    if (j.payment_error) throw new LightningPaymentError(j.payment_error);
    if (!j.payment_preimage) throw new LightningPaymentError('LND returned no preimage');
    return {
      preimageHex: b64ToHex(j.payment_preimage),
      paymentHashHex: b64ToHex(j.payment_hash ?? ''),
      feeSats: Number(j.payment_route?.total_fees ?? 0),
    };
  }
}
