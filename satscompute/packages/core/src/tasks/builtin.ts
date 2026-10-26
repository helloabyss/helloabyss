import { cosine, outputHash } from '../proof';
import type { TaskKind } from '../types';
import { assertStringArray, ExecutorRegistry, TaskInputError, type Executor } from './executor';
import { embed, EMBED_DIM, embedFloat } from './hashing-embedder';

/** Texts per checkpoint. Small enough that a checkpoint lands every few ms on a phone. */
const CHUNK = 4;

// ---------------------------------------------------------------- embeddings

export interface EmbeddingInput {
  texts: string[];
  dim: number;
}

export const embeddingExecutor: Executor<EmbeddingInput, { vectors: number[][] }> = {
  kind: 'embedding',
  version: 'hash-embed@1',
  parse(input) {
    const i = input as Partial<EmbeddingInput>;
    const dim = i.dim ?? EMBED_DIM;
    if (![64, 128, 256, 512].includes(dim)) throw new TaskInputError('dim must be 64|128|256|512');
    return { texts: assertStringArray(i.texts, 'texts'), dim };
  },
  async run({ texts, dim }, ctx) {
    const vectors: number[][] = [];
    for (let i = 0; i < texts.length; i++) {
      vectors.push(embed(texts[i]!, dim));
      if (i % CHUNK === CHUNK - 1) await ctx.checkpoint((i + 1) / texts.length);
    }
    return { vectors };
  },
};

// ---------------------------------------------------------------- zero-shot classification

export interface ClassificationInput {
  texts: string[];
  /** label -> short description used as the label prototype. */
  labels: Record<string, string>;
}

export const classificationExecutor: Executor<
  ClassificationInput,
  { labels: string[]; scores: number[] }
> = {
  kind: 'classification',
  version: 'hash-zeroshot@1',
  parse(input) {
    const i = input as Partial<ClassificationInput>;
    if (!i.labels || typeof i.labels !== 'object' || Object.keys(i.labels).length < 2) {
      throw new TaskInputError('labels must map at least 2 labels to descriptions');
    }
    return { texts: assertStringArray(i.texts, 'texts'), labels: i.labels };
  },
  async run({ texts, labels }, ctx) {
    const protos = Object.entries(labels).map(([label, desc]) => ({ label, v: embedFloat(`${label} ${desc}`) }));
    const out = { labels: [] as string[], scores: [] as number[] };
    for (let i = 0; i < texts.length; i++) {
      const v = embedFloat(texts[i]!);
      let best = protos[0]!;
      let bestScore = -Infinity;
      for (const p of protos) {
        const s = cosine(v, p.v);
        if (s > bestScore) {
          bestScore = s;
          best = p;
        }
      }
      out.labels.push(best.label);
      out.scores.push(Math.round(bestScore * 1000) / 1000);
      if (i % CHUNK === CHUNK - 1) await ctx.checkpoint((i + 1) / texts.length);
    }
    return out;
  },
};

// ---------------------------------------------------------------- data filtering

export interface FilterInput {
  texts: string[];
  minChars: number;
  /** Near-duplicate threshold on cosine similarity. */
  dedupeThreshold: number;
}

export const filterExecutor: Executor<FilterInput, { keep: number[]; dropped: Record<string, number> }> = {
  kind: 'filter',
  version: 'filter@1',
  parse(input) {
    const i = input as Partial<FilterInput>;
    return {
      texts: assertStringArray(i.texts, 'texts', 1024),
      minChars: Math.max(0, Number(i.minChars ?? 20)),
      dedupeThreshold: Math.min(1, Math.max(0.5, Number(i.dedupeThreshold ?? 0.95))),
    };
  },
  async run({ texts, minChars, dedupeThreshold }, ctx) {
    const kept: { idx: number; v: number[] }[] = [];
    const dropped = { short: 0, duplicate: 0 };
    for (let i = 0; i < texts.length; i++) {
      const t = texts[i]!.trim();
      if (t.length < minChars) dropped.short++;
      else {
        const v = embedFloat(t);
        if (kept.some((k) => cosine(k.v, v) >= dedupeThreshold)) dropped.duplicate++;
        else kept.push({ idx: i, v });
      }
      if (i % CHUNK === CHUNK - 1) await ctx.checkpoint((i + 1) / texts.length);
    }
    return { keep: kept.map((k) => k.idx), dropped };
  },
};

// ---------------------------------------------------------------- verification

export interface VerificationInput {
  /** Another task to re-execute, and the hash a different device claimed for it. */
  target: { taskId: string; kind: TaskKind; input: unknown };
  claimedHash: string;
}

export function verificationExecutor(registry: ExecutorRegistry): Executor<VerificationInput, { match: boolean }> {
  return {
    kind: 'verification',
    version: 'verify@1',
    parse(input) {
      const i = input as Partial<VerificationInput>;
      if (!i.target || typeof i.claimedHash !== 'string') throw new TaskInputError('target and claimedHash required');
      if (i.target.kind === 'verification') throw new TaskInputError('cannot verify a verification');
      return i as VerificationInput;
    },
    async run({ target, claimedHash }, ctx) {
      const ex = registry.get(target.kind);
      if (!ex) throw new TaskInputError(`no executor for ${target.kind}`);
      const out = await ex.run(ex.parse(target.input), ctx);
      return { match: outputHash(target.taskId, target.kind, out) === claimedHash };
    },
  };
}

/** Registry with every built-in executor. Platforms add model-backed ones (e.g. 'llm-small'). */
export function createDefaultRegistry(): ExecutorRegistry {
  const r = new ExecutorRegistry();
  r.register(embeddingExecutor).register(classificationExecutor).register(filterExecutor);
  r.register(verificationExecutor(r));
  return r;
}
