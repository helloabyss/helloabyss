import { PAYOUT } from '@satscompute/core';

const env = process.env;

export interface Config {
  port: number;
  host: string;
  tokenPepper: string;
  seedSampleTasks: boolean;
  requesterApiKeys: string[];
  payoutMinSats: number;
  lightning: { provider: 'mock' } | { provider: 'lnd'; restUrl: string; macaroonHex: string };
  revenueCatSecret: string | null;
  btcUsdReference: number | null;
}

export function loadConfig(overrides: Partial<Config> = {}): Config {
  const provider = env.LIGHTNING_PROVIDER ?? 'mock';
  const lightning: Config['lightning'] =
    provider === 'lnd'
      ? { provider: 'lnd', restUrl: required('LND_REST_URL'), macaroonHex: required('LND_MACAROON_HEX') }
      : { provider: 'mock' };
  const cfg: Config = {
    port: Number(env.PORT ?? 8787),
    host: env.HOST ?? '0.0.0.0',
    tokenPepper: env.TOKEN_PEPPER ?? 'dev-only-pepper',
    seedSampleTasks: (env.SEED_SAMPLE_TASKS ?? 'true') === 'true',
    requesterApiKeys: (env.REQUESTER_API_KEYS ?? '').split(',').filter(Boolean),
    payoutMinSats: Math.max(PAYOUT.minSats, Number(env.PAYOUT_MIN_SATS ?? PAYOUT.minSats)),
    lightning,
    revenueCatSecret: env.REVENUECAT_WEBHOOK_SECRET || null,
    btcUsdReference: env.BTC_USD_REFERENCE ? Number(env.BTC_USD_REFERENCE) : null,
    ...overrides,
  };
  if (env.NODE_ENV === 'production') {
    if (cfg.tokenPepper === 'dev-only-pepper') throw new Error('TOKEN_PEPPER must be set in production');
    if (cfg.seedSampleTasks) throw new Error('SEED_SAMPLE_TASKS must be false in production: sample tasks pay real sats');
    if (cfg.lightning.provider === 'mock') throw new Error('LIGHTNING_PROVIDER=mock is not allowed in production');
  }
  return cfg;
}

function required(k: string): string {
  const v = env[k];
  if (!v) throw new Error(`${k} is required`);
  return v;
}
