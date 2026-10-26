import type { TaskKind, TaskSpec } from '../types';

/**
 * Realistic sample workloads used by the mock coordinator and dev server until real requesters
 * post work. Each one carries an explainer the dashboard shows verbatim.
 */

const PRODUCT_REVIEWS = [
  'Battery lasts two days and the screen is bright outdoors.',
  'Stopped charging after a week, support never replied.',
  'Decent headphones for the price, bass is a little muddy.',
  'Arrived broken. Box was crushed. Requesting a refund.',
  'Setup took five minutes and it just works with my laptop.',
  'The app keeps logging me out, very frustrating.',
  'Great value, would buy again for the kids.',
  'Fan noise is louder than advertised under load.',
];

const DOCS = [
  'How to reset your router to factory settings.',
  'Configuring two-factor authentication for your account.',
  'Troubleshooting slow Wi-Fi in large homes.',
  'Exporting your data as CSV from the dashboard.',
  'Understanding your monthly invoice and line items.',
  'Pairing a Bluetooth keyboard with a tablet.',
  'Updating firmware safely without losing settings.',
  'What to do when the device will not power on.',
  'Setting up guest network access for visitors.',
  'Recovering a forgotten password by email.',
  'Scheduling automatic backups every night.',
  'Changing the display language and region.',
];

const SCRAPED = [
  'Click here to subscribe',
  'Lightning payments settle in seconds with low fees on small amounts.',
  'Lightning payments settle in seconds with low fees on small amounts!',
  'ok',
  'Solar panels convert sunlight into electricity using photovoltaic cells.',
  'Sign up now',
  'A heat pump moves heat rather than generating it, which makes it efficient.',
  'A heat pump moves heat instead of generating it, which makes it efficient.',
];

let seq = 0;
const id = (kind: TaskKind) => `t_${kind.slice(0, 3)}_${Date.now().toString(36)}_${(seq++).toString(36)}`;

/** Gross price ≈ 2 msat per work unit. Placeholder market rate, served by the coordinator in prod. */
const MSAT_PER_UNIT = 2;

export function sampleTask(kind: TaskKind, now = new Date(), leaseSeconds = 300): TaskSpec {
  const lease = new Date(now.getTime() + leaseSeconds * 1000).toISOString();
  const base = { id: id(kind), leaseExpiresAt: lease, replication: 2 };
  switch (kind) {
    case 'embedding': {
      const texts = DOCS;
      const workUnits = texts.length * 40;
      return {
        ...base,
        kind,
        explainer: 'Generating search embeddings for a help-centre search tool.',
        requester: 'Helpdesk search (sample)',
        requirements: { minMemoryMb: 64, needsGpu: false, workUnits, payloadKb: 24 },
        rewardMsat: workUnits * MSAT_PER_UNIT,
        input: { texts, dim: 256 },
      };
    }
    case 'classification': {
      const workUnits = PRODUCT_REVIEWS.length * 60;
      return {
        ...base,
        kind,
        explainer: 'Sorting product reviews into praise, complaints and refund requests for a small shop.',
        requester: 'Review triage (sample)',
        requirements: { minMemoryMb: 64, needsGpu: false, workUnits, payloadKb: 4 },
        rewardMsat: workUnits * MSAT_PER_UNIT,
        input: {
          texts: PRODUCT_REVIEWS,
          labels: {
            praise: 'great good works value happy recommend buy again',
            complaint: 'bad noisy frustrating broken muddy logging out slow',
            refund: 'refund broken arrived crushed return money back',
          },
        },
      };
    }
    case 'filter': {
      const workUnits = SCRAPED.length * 50;
      return {
        ...base,
        kind,
        explainer: 'Removing junk and near-duplicate lines from a web dataset before AI training.',
        requester: 'Open dataset cleanup (sample)',
        requirements: { minMemoryMb: 64, needsGpu: false, workUnits, payloadKb: 3 },
        rewardMsat: workUnits * MSAT_PER_UNIT,
        input: { texts: SCRAPED, minChars: 20, dedupeThreshold: 0.9 },
      };
    }
    case 'verification':
    case 'llm-small':
      // Verification tasks are minted by the coordinator from real results; llm-small needs a model.
      return sampleTask('embedding', now, leaseSeconds);
  }
}

export const SAMPLE_KINDS: TaskKind[] = ['embedding', 'classification', 'filter'];
