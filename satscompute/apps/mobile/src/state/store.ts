import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  DEFAULT_ENTITLEMENTS,
  defaultPolicy,
  PAYOUT,
  sanitizePolicy,
  type Balance,
  type ContributionPolicy,
  type DeviceProfile,
  type Entitlements,
  type LedgerEntry,
  type MarketQuote,
} from '@satscompute/core';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

/**
 * App state, persisted locally so settings work offline and the earnings history is
 * readable without a network. Secrets (device token) live in SecureStore, not here.
 */

const LEDGER_CAP = 2000;

export interface PayoutSettings {
  destination: string | null;
  /** When the destination was last confirmed reachable (LNURL resolve). */
  verifiedAt: string | null;
  autoPayout: boolean;
  thresholdSats: number;
}

export interface PrivacySettings {
  analytics: boolean;
  leaderboard: boolean;
  handle: string | null;
}

interface AppState {
  hydrated: boolean;
  onboarded: boolean;
  installedAt: string;
  policy: ContributionPolicy;
  payout: PayoutSettings;
  privacy: PrivacySettings;
  entitlements: Entitlements;
  bitcoinMode: boolean;
  ledger: LedgerEntry[];
  balance: Balance | null;
  market: MarketQuote | null;
  profile: DeviceProfile | null;

  setPolicy: (patch: Partial<ContributionPolicy>) => void;
  setPayout: (patch: Partial<PayoutSettings>) => void;
  setPrivacy: (patch: Partial<PrivacySettings>) => void;
  setEntitlements: (e: Entitlements) => void;
  upsertLedger: (e: LedgerEntry) => void;
  setBalance: (b: Balance) => void;
  setMarket: (m: MarketQuote) => void;
  setProfile: (p: DeviceProfile) => void;
  setBitcoinMode: (on: boolean) => void;
  completeOnboarding: () => void;
  resetAll: () => void;
}

const initial = () => ({
  onboarded: false,
  installedAt: new Date().toISOString(),
  policy: defaultPolicy('phone'),
  payout: { destination: null, verifiedAt: null, autoPayout: false, thresholdSats: PAYOUT.minSats },
  privacy: { analytics: false, leaderboard: false, handle: null },
  entitlements: DEFAULT_ENTITLEMENTS,
  bitcoinMode: false,
  ledger: [] as LedgerEntry[],
  balance: null,
  market: null,
  profile: null,
});

export const useApp = create<AppState>()(
  persist(
    (set) => ({
      hydrated: false,
      ...initial(),
      setPolicy: (patch) => set((s) => ({ policy: sanitizePolicy({ ...s.policy, ...patch }) })),
      setPayout: (patch) =>
        set((s) => ({
          payout: {
            ...s.payout,
            ...patch,
            thresholdSats: Math.min(PAYOUT.maxThresholdSats, Math.max(PAYOUT.minSats, patch.thresholdSats ?? s.payout.thresholdSats)),
          },
        })),
      setPrivacy: (patch) => set((s) => ({ privacy: { ...s.privacy, ...patch } })),
      setEntitlements: (entitlements) => set({ entitlements }),
      upsertLedger: (e) =>
        set((s) => {
          const rest = s.ledger.filter((x) => x.id !== e.id);
          return { ledger: [e, ...rest].slice(0, LEDGER_CAP) };
        }),
      setBalance: (balance) => set({ balance }),
      setMarket: (market) => set({ market }),
      setProfile: (profile) => set({ profile }),
      setBitcoinMode: (bitcoinMode) => set({ bitcoinMode }),
      completeOnboarding: () => set({ onboarded: true }),
      resetAll: () => set({ ...initial() }),
    }),
    {
      name: 'satscompute-v1',
      version: 1,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: ({ hydrated: _h, ...rest }) => rest,
      // Re-clamp on load so a corrupted or older settings blob can't bypass limits.
      merge: (persisted, current) => {
        const p = (persisted ?? {}) as Partial<AppState>;
        return { ...current, ...p, policy: sanitizePolicy({ ...current.policy, ...(p.policy ?? {}) }) };
      },
      onRehydrateStorage: () => () => useApp.setState({ hydrated: true }),
    },
  ),
);

export const selectLifetimeSats = (s: AppState) =>
  Math.floor(s.ledger.filter((e) => e.kind === 'task' && e.status === 'accepted').reduce((a, e) => a + e.amountMsat, 0) / 1000);
