import { maskDestination, PAYOUT, type LeaderboardRow } from '@satscompute/core';
import { router } from 'expo-router';
import { useEffect, useState } from 'react';
import { Alert, TextInput } from 'react-native';
import { hasNativeThermal } from '../../modules/thermal-state';
import { Banner, Button, Card, Row, Screen, Section, Stepper, T, ToggleRow } from '../../src/components/ui';
import { buildProfile } from '../../src/device/profile';
import { getRuntime, isMockBackend } from '../../src/engine/runtime';
import { useApp } from '../../src/state/store';
import { colors, radius, space } from '../../src/theme';

export default function Settings() {
  const payout = useApp((s) => s.payout);
  const privacy = useApp((s) => s.privacy);
  const profile = useApp((s) => s.profile);
  const { setPayout, setPrivacy, setProfile, resetAll } = useApp.getState();
  const [handle, setHandle] = useState(privacy.handle ?? '');
  const [board, setBoard] = useState<LeaderboardRow[] | null>(null);
  const [boardError, setBoardError] = useState<string | null>(null);

  useEffect(() => {
    if (!privacy.leaderboard) return setBoard(null);
    getRuntime()
      .then((rt) => rt.client.leaderboard())
      .then(setBoard, (e: Error) => setBoardError(e.message));
  }, [privacy.leaderboard, privacy.handle]);

  const saveHandle = async (on: boolean) => {
    const h = handle.trim().slice(0, 20);
    if (on && !/^[a-z0-9_]{3,20}$/i.test(h)) return Alert.alert('Pick a handle', '3–20 letters, numbers or underscores. Don’t use your real name.');
    try {
      const rt = await getRuntime();
      await rt.client.setLeaderboardHandle(on ? h : null);
      setPrivacy({ leaderboard: on, handle: on ? h : null });
    } catch (e) {
      Alert.alert('Could not update leaderboard', (e as Error).message);
    }
  };

  return (
    <Screen>
      <T v="title">Settings</T>

      <Section title="Payouts">
        <Card>
          <Row style={{ justifyContent: 'space-between' }}>
            <T>Destination</T>
            <T v="small">{payout.destination ? maskDestination(payout.destination) : 'Not set'}</T>
          </Row>
          <Button title={payout.destination ? 'Change wallet' : 'Add Lightning wallet'} kind="secondary" onPress={() => router.push('/payout?setup=1')} />
          <ToggleRow
            label="Automatic payouts"
            hint="Sends your balance to your wallet whenever it passes the threshold."
            value={payout.autoPayout}
            disabled={!payout.destination}
            onChange={(v) => setPayout({ autoPayout: v })}
          />
          <Stepper
            label="Payout threshold"
            hint={`Minimum ${PAYOUT.minSats} sats keeps routing fees reasonable.`}
            value={payout.thresholdSats}
            step={250}
            min={PAYOUT.minSats}
            max={21_000}
            format={(v) => v.toLocaleString('en-US')}
            onChange={(v) => setPayout({ thresholdSats: v })}
          />
        </Card>
      </Section>

      <Section title="Privacy">
        <Card>
          <ToggleRow
            label="Anonymous usage stats"
            hint="Weekly bucketed counters (tasks done, errors). No device ID, no wallet, no task content."
            value={privacy.analytics}
            onChange={(v) => setPrivacy({ analytics: v })}
          />
          <ToggleRow label="Show me on the leaderboard" hint="Weekly sats, rounded to the nearest 100, under a handle you choose." value={privacy.leaderboard} onChange={(v) => void saveHandle(v)} />
          {!privacy.leaderboard && (
            <TextInput
              value={handle}
              onChangeText={setHandle}
              placeholder="handle"
              placeholderTextColor={colors.faint}
              autoCapitalize="none"
              autoCorrect={false}
              style={{ color: colors.text, borderColor: colors.border, borderWidth: 1, borderRadius: radius.sm, padding: space(3) }}
            />
          )}
        </Card>
      </Section>

      {privacy.leaderboard && (
        <Section title="This week">
          <Card>
            {boardError && <Banner tone="muted" text={boardError} />}
            {board?.length === 0 && <T v="small">No one has opted in yet this week.</T>}
            {board?.map((r, i) => (
              <Row key={r.handle} style={{ justifyContent: 'space-between' }}>
                <T style={{ color: r.handle === privacy.handle ? colors.accent : colors.text }}>
                  {i + 1}. {r.handle}
                </T>
                <T v="small">~{r.satsRounded.toLocaleString('en-US')} sats</T>
              </Row>
            ))}
          </Card>
        </Section>
      )}

      <Section title="This device">
        <Card>
          <Row style={{ justifyContent: 'space-between' }}>
            <T>Benchmark</T>
            <T v="small">{profile?.benchmarkUnitsPerSec.toLocaleString('en-US') ?? '—'} units/s</T>
          </Row>
          <Row style={{ justifyContent: 'space-between' }}>
            <T>Thermal sensor</T>
            <T v="small">{hasNativeThermal ? 'Available' : 'Unavailable (reduced speed)'}</T>
          </Row>
          <Row style={{ justifyContent: 'space-between' }}>
            <T>Backend</T>
            <T v="small">{isMockBackend ? 'Demo (offline)' : 'Coordinator'}</T>
          </Row>
          <Button title="Re-run benchmark" kind="ghost" onPress={() => setProfile(buildProfile())} />
        </Card>
      </Section>

      <Section title="About">
        <Card>
          <T v="small">
            SatsCompute runs small AI workloads on your device and pays you in bitcoin over Lightning. It does not mine Bitcoin. Earnings depend on demand and
            are not guaranteed. Your wallet is yours — we never hold your keys; we only hold your unpaid balance until it reaches your payout threshold.
          </T>
        </Card>
      </Section>

      <Button
        title="Erase local data"
        kind="danger"
        onPress={() =>
          Alert.alert('Erase local data?', 'Settings and local history are removed. Your server-side balance is not affected.', [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Erase', style: 'destructive', onPress: resetAll },
          ])
        }
      />
    </Screen>
  );
}
