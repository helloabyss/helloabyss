import {
  headlineInsights,
  KIND_EXPLAINER,
  KIND_LABEL,
  projectSatsPerHour,
  projectSession,
  REASON_COPY,
  satsToUsd,
} from '@satscompute/core';
import { router, useFocusEffect } from 'expo-router';
import { useCallback, useMemo } from 'react';
import { View } from 'react-native';
import { phaseCopy } from '../../src/components/phase';
import { Banner, Button, Card, Pill, Progress, Row, Screen, Section, Stat, T } from '../../src/components/ui';
import { isMockBackend } from '../../src/engine/runtime';
import { useEngine } from '../../src/engine/useEngine';
import { useApp } from '../../src/state/store';
import { colors, space } from '../../src/theme';

const fmt = (n: number) => Math.floor(n).toLocaleString('en-US');

export default function Dashboard() {
  const { runtime, snap, error, retry } = useEngine();
  const policy = useApp((s) => s.policy);
  const balance = useApp((s) => s.balance);
  const market = useApp((s) => s.market);
  const profile = useApp((s) => s.profile);
  const ledger = useApp((s) => s.ledger);
  const ent = useApp((s) => s.entitlements);
  const bitcoinMode = useApp((s) => s.bitcoinMode);

  useFocusEffect(
    useCallback(() => {
      void runtime?.refresh();
    }, [runtime]),
  );

  const est = useMemo(() => {
    if (!profile || !market) return null;
    const boosted = !!ent.priorityBoostUntil && Date.parse(ent.priorityBoostUntil) > Date.now();
    const perHour = projectSatsPerHour(profile, policy.maxCpuPercent / 100, market, ent.feeTier, boosted);
    return { perHour, night: projectSession(perHour, 8) };
  }, [profile, market, policy.maxCpuPercent, ent]);

  const insights = useMemo(() => headlineInsights(ledger), [ledger]);
  const phase = phaseCopy(snap);
  const available = (balance?.availableMsat ?? 0) / 1000;
  const pending = (balance?.pendingMsat ?? 0) / 1000;
  const usd = satsToUsd(available, market?.btcUsd ?? null);

  return (
    <Screen>
      <Row style={{ justifyContent: 'space-between' }}>
        <T v="title">SatsCompute</T>
        <Pill label={phase.label} tone={phase.tone} />
      </Row>

      {error && <Banner tone="danger" text={`Can't reach the network: ${error}`} action={{ label: 'Retry', onPress: retry }} />}
      {isMockBackend && <Banner tone="muted" text="Demo mode: sample tasks, no real sats. Set EXPO_PUBLIC_COORDINATOR_URL to connect." />}

      <Card tone="accent">
        <T v="small">Available to withdraw</T>
        <T v="display">{fmt(available)} sats</T>
        <Row style={{ gap: space(3) }}>
          {pending > 0 && <T v="small">+{fmt(pending)} pending verification</T>}
          {usd !== null && <T v="small">≈ ${usd.toFixed(2)} at reference price</T>}
        </Row>
        <Button title="Withdraw to Lightning" kind="secondary" onPress={() => router.push('/payout')} disabled={available <= 0} />
      </Card>

      <Card>
        <Row style={{ justifyContent: 'space-between' }}>
          <T v="heading">Right now</T>
          {snap && snap.dutyCycle > 0 && <T v="small">{Math.round(snap.dutyCycle * 100)}% duty cycle</T>}
        </Row>
        {!policy.enabled ? (
          <T v="small">Sharing is off. Turn it on in Controls when you're ready — nothing runs until you do.</T>
        ) : snap?.current ? (
          <View style={{ gap: space(2) }}>
            <Pill label={KIND_LABEL[snap.current.task.kind]} tone="accent" />
            <T>{snap.current.task.explainer}</T>
            <T v="small">For: {snap.current.task.requester}</T>
            <Progress value={snap.current.progress} />
          </View>
        ) : snap?.reasons.length ? (
          snap.reasons.map((r) => (
            <T key={r} v="small">
              • {REASON_COPY[r]}
            </T>
          ))
        ) : (
          <T v="small">Start a Nightstand session while charging, or let the OS run short background windows.</T>
        )}
        {snap && snap.session.tasksCompleted > 0 && (
          <Row style={{ gap: space(4) }}>
            <Stat label="This session" value={`${fmt(snap.session.creditedMsat / 1000)} sats`} sub={snap.session.pendingMsat ? `+${fmt(snap.session.pendingMsat / 1000)} pending` : undefined} />
            <Stat label="Tasks" value={String(snap.session.tasksCompleted)} sub={snap.session.tasksRejected ? `${snap.session.tasksRejected} rejected` : undefined} />
          </Row>
        )}
        {policy.enabled ? (
          <Button title="Start Nightstand session" onPress={() => router.push('/session')} />
        ) : (
          <Button title="Set up sharing" onPress={() => router.push('/controls')} />
        )}
      </Card>

      {est && (
        <Card>
          <T v="heading">Estimated earnings</T>
          <Row style={{ gap: space(4) }}>
            <Stat label="Per hour" value={`${fmt(est.perHour.low)}–${fmt(est.perHour.high)}`} sub="sats" />
            <Stat label="8h overnight" value={`${fmt(est.night.low)}–${fmt(est.night.high)}`} sub="sats" />
          </Row>
          <T v="small">
            Based on this device's benchmark, your {policy.maxCpuPercent}% limit and current demand. Not guaranteed — if nobody needs work done,
            you earn nothing.
          </T>
        </Card>
      )}

      {insights.length > 0 && (
        <Section title="Insights">
          <Card>
            {insights.map((i) => (
              <T key={i}>{i}</T>
            ))}
          </Card>
        </Section>
      )}

      {bitcoinMode && (
        <Card>
          <T v="heading">Bitcoin mode</T>
          <T v="small">Check the latest blocks' proof-of-work yourself. No mining, no earnings — just verification.</T>
          <Button title="Verify latest blocks" kind="ghost" onPress={() => router.push('/bitcoin')} />
        </Card>
      )}

      <Section title="What your device does">
        {policy.allowedKinds.map((k) => (
          <Card key={k}>
            <T v="heading">{KIND_LABEL[k]}</T>
            <T v="small">{KIND_EXPLAINER[k]}</T>
          </Card>
        ))}
      </Section>

      <T v="small" style={{ color: colors.faint, textAlign: 'center' }}>
        SatsCompute does not mine Bitcoin. Your device runs small AI jobs for paying customers; you're paid in sats over Lightning.
      </T>
    </Screen>
  );
}
