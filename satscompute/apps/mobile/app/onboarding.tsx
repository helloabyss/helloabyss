import { projectSatsPerHour, projectSession, type MarketQuote } from '@satscompute/core';
import { router } from 'expo-router';
import { useMemo, useState } from 'react';
import { View } from 'react-native';
import { Button, Card, Row, Screen, T, ToggleRow } from '../src/components/ui';
import { buildProfile } from '../src/device/profile';
import { useApp } from '../src/state/store';
import { colors, space } from '../src/theme';

/** Used only until the coordinator's live quote arrives. Deliberately conservative. */
const FALLBACK_MARKET: MarketQuote = { msatPerUnit: 2, utilization: { p10: 0.1, p50: 0.35, p90: 0.7 }, btcUsd: null, asOf: '' };

const STEPS = ['what', 'control', 'money', 'consent'] as const;

export default function Onboarding() {
  const [i, setI] = useState(0);
  const [agree, setAgree] = useState(false);
  const [stats, setStats] = useState(false);
  const store = useApp();

  const profile = useMemo(() => {
    if (store.profile) return store.profile;
    const p = buildProfile();
    store.setProfile(p);
    return p;
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const night = projectSession(projectSatsPerHour(profile, store.policy.maxCpuPercent / 100, store.market ?? FALLBACK_MARKET, 'standard'), 8);
  const step = STEPS[i]!;

  const finish = () => {
    store.setPrivacy({ analytics: stats });
    if (agree) store.setPolicy({ enabled: true });
    store.completeOnboarding();
    router.replace('/');
  };

  return (
    <Screen scroll={false}>
      <Row style={{ gap: space(1.5) }}>
        {STEPS.map((s, n) => (
          <View key={s} style={{ flex: 1, height: 3, borderRadius: 2, backgroundColor: n <= i ? colors.accent : colors.border }} />
        ))}
      </Row>

      <View style={{ flex: 1, justifyContent: 'center', gap: space(5) }}>
        {step === 'what' && (
          <>
            <T v="display">Earn sats with idle compute.</T>
            <T>Your phone runs small AI jobs — search embeddings, text sorting, dataset cleanup — for people who need them done cheaply. You're paid in bitcoin over Lightning.</T>
            <Card>
              <T v="heading">What this is not</T>
              <T v="small">It is not Bitcoin mining. Phones can't mine profitably, and we don't pretend otherwise. Every sat you earn comes from real work a customer paid for.</T>
            </Card>
          </>
        )}
        {step === 'control' && (
          <>
            <T v="title">You stay in control.</T>
            <Card>
              <T>• Only while charging and on Wi-Fi</T>
              <T>• Uses at most {store.policy.maxCpuPercent}% of the processor, resting in between</T>
              <T>• Stops as soon as the phone gets warm</T>
              <T>• Pauses whenever you pick up the phone</T>
              <T>• Off by default — and one tap to turn off</T>
            </Card>
            <T v="small">You can change every limit in Controls. Task data is processed on your device; only the result is sent back.</T>
          </>
        )}
        {step === 'money' && (
          <>
            <T v="title">Honest numbers.</T>
            <Card tone="accent">
              <T v="small">A night on the charger, for this device, right now:</T>
              <T v="display">
                {Math.floor(night.low)}–{Math.floor(night.high)} sats
              </T>
              <T v="small">That's small. It depends on demand, which we don't control, and it isn't guaranteed.</T>
            </Card>
            <T v="small">
              The platform keeps 20% of each task's price. You can withdraw once you have 250 sats, to any Lightning wallet you choose. We hold only your unpaid balance —
              never your keys.
            </T>
          </>
        )}
        {step === 'consent' && (
          <>
            <T v="title">Your call.</T>
            <Card>
              <ToggleRow label="Share idle compute" hint="Under the limits you just saw. You can start later instead." value={agree} onChange={setAgree} />
              <ToggleRow label="Share anonymous usage stats" hint="Bucketed weekly counters. No IDs. Helps us fix bugs." value={stats} onChange={setStats} />
            </Card>
          </>
        )}
      </View>

      <Row style={{ gap: space(3) }}>
        {i > 0 && (
          <View style={{ flex: 1 }}>
            <Button title="Back" kind="ghost" onPress={() => setI(i - 1)} />
          </View>
        )}
        <View style={{ flex: 2 }}>
          {i < STEPS.length - 1 ? <Button title="Continue" onPress={() => setI(i + 1)} /> : <Button title={agree ? 'Start' : 'Finish'} onPress={finish} />}
        </View>
      </Row>
    </Screen>
  );
}
