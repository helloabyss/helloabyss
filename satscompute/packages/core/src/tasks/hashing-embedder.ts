/**
 * Feature-hashing text embedder (the "hashing trick"): unigrams + bigrams hashed into a fixed
 * number of signed buckets, L2-normalised, then int8-quantised.
 *
 * This is a real, deterministic embedding baseline, and it's what the sample tasks run so the
 * whole pipeline (lease → run → proof → verify → pay) works end to end with no model download.
 * Swap in an on-device model (ONNX Runtime / ExecuTorch) behind the same Executor interface.
 */

export const EMBED_DIM = 256;

/** FNV-1a 32-bit. Stable across JS engines, unlike String.hashCode-style tricks. */
export function fnv1a(s: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

/**
 * Lowercase, split on anything that isn't a letter or digit. Hand-rolled (no Unicode property
 * regex, no normalize()) so Hermes, JSC and V8 produce byte-identical tokens — replicas on
 * different phones must hash the same output.
 */
export function tokenize(text: string): string[] {
  const out: string[] = [];
  let cur = '';
  for (const ch of text.toLowerCase()) {
    const isWord = (ch >= '0' && ch <= '9') || ch.toLowerCase() !== ch.toUpperCase();
    if (isWord) cur += ch;
    else if (cur) {
      out.push(cur);
      cur = '';
    }
  }
  if (cur) out.push(cur);
  return out;
}

export function embedFloat(text: string, dim = EMBED_DIM): number[] {
  const v = new Array<number>(dim).fill(0);
  const toks = tokenize(text);
  const feats = [...toks, ...toks.slice(1).map((t, i) => `${toks[i]}_${t}`)];
  for (const f of feats) {
    const h = fnv1a(f);
    const sign = h & 1 ? 1 : -1;
    v[(h >>> 1) % dim]! += sign;
  }
  const norm = Math.sqrt(v.reduce((a, x) => a + x * x, 0)) || 1;
  return v.map((x) => x / norm);
}

/** int8 quantisation makes output bit-identical across devices, so replicas can hash-match. */
export function quantize(v: number[]): number[] {
  return v.map((x) => Math.max(-127, Math.min(127, Math.round(x * 127))));
}

export function embed(text: string, dim = EMBED_DIM): number[] {
  return quantize(embedFloat(text, dim));
}

/** Single-thread benchmark in work units/s (1 embedded doc = 40 units, matching samples.ts). */
export function benchmarkFallback(budgetMs = 250): number {
  const start = Date.now();
  let n = 0;
  while (Date.now() - start < budgetMs) embed(`benchmark document number ${n++} for throughput`);
  return Math.round((n / (Math.max(1, Date.now() - start) / 1000)) * 40);
}
