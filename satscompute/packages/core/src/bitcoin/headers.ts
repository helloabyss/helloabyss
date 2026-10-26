import { sha256 } from '@noble/hashes/sha256';
import { bytesToHex, hexToBytes } from '@noble/hashes/utils';

/**
 * Optional "Bitcoin contribution" mode, phone edition: independently verify the proof-of-work
 * on recent block headers. This is NOT mining and earns nothing. It lets a user check the chain
 * tip for themselves instead of trusting an API, and is the on-ramp to running a real pruned
 * node from the desktop agent, which is where actual network support happens.
 */

export interface ParsedHeader {
  version: number;
  prevHash: string; // big-endian display hex
  merkleRoot: string;
  time: number;
  bits: number;
  nonce: number;
  hash: string; // big-endian display hex
}

const reverseHex = (b: Uint8Array) => bytesToHex(Uint8Array.from(b).reverse());

export function parseHeader(hex: string): ParsedHeader {
  const b = hexToBytes(hex);
  if (b.length !== 80) throw new Error('Block header must be 80 bytes');
  const dv = new DataView(b.buffer, b.byteOffset, 80);
  return {
    version: dv.getInt32(0, true),
    prevHash: reverseHex(b.slice(4, 36)),
    merkleRoot: reverseHex(b.slice(36, 68)),
    time: dv.getUint32(68, true),
    bits: dv.getUint32(72, true),
    nonce: dv.getUint32(76, true),
    hash: reverseHex(sha256(sha256(b))),
  };
}

/** Expand compact "bits" into the 256-bit target. */
export function bitsToTarget(bits: number): bigint {
  const exp = bits >>> 24;
  const mant = BigInt(bits & 0x007fffff);
  return exp <= 3 ? mant >> BigInt(8 * (3 - exp)) : mant << BigInt(8 * (exp - 3));
}

export function meetsTarget(h: ParsedHeader): boolean {
  return BigInt(`0x${h.hash}`) <= bitsToTarget(h.bits);
}

/** Verify a contiguous run of headers: each meets its own target and links to the previous one. */
export function verifyHeaderChain(hexes: string[]): { ok: boolean; tip: string | null; failedAt?: number } {
  let prev: ParsedHeader | null = null;
  for (let i = 0; i < hexes.length; i++) {
    const h = parseHeader(hexes[i]!);
    if (!meetsTarget(h)) return { ok: false, tip: prev?.hash ?? null, failedAt: i };
    if (prev && h.prevHash !== prev.hash) return { ok: false, tip: prev.hash, failedAt: i };
    prev = h;
  }
  return { ok: true, tip: prev?.hash ?? null };
}
