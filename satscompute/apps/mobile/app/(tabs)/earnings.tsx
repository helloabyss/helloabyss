import {
  allBadges,
  badgeStats,
  contributionStreak,
  dailySeries,
  earnedBadges,
  KIND_LABEL,
  kindBreakdown,
  type LedgerEntry,
} from '@satscompute/core';
import * as Clipboard from 'expo-clipboard';
import { router } from 'expo-router';
import { useMemo } from 'react';
import { Alert, Pressable, useWindowDimensions, View } from 'react-native';
import { BarChart } from '../../src/components/BarChart';
import { Button, Card, Pill, Row, Screen, Section, Stat, T } from '../../src/components/ui';
import { useApp } from '../../src/state/store';
import { colors, space } from '../../src/theme';

const fmt = (n: number) => Math.floor(n).toLocaleString('en-US');

export default function Earnings() {
  const ledger = useApp((s) => s.ledger);
  const balance = useApp((s) => s.balance);
  const advanced = useApp((s) => s.entitlements.advancedAnalytics);
  const { width } = useWindowDimensions();

  const days = advanced ? 30 : 7;
  const series = useMemo(() => dailySeries(ledger, days), [ledger, days]);
  const stats = useMemo(() => badgeStats(ledger), [ledger]);
  const earned = useMemo(() => new Set(earnedBadges(stats).map((b) => b.id)), [stats]);
  const breakdown = useMemo(() => kindBreakdown(ledger), [ledger]);
  const streak = contributionStreak(ledger);

  return (
    <Screen>
      <T v="title">Earnings</T>
      <Card>
        <Row style={{ gap: space(4) }}>
          <Stat label="Available" value={`${fmt((balance?.availableMsat ?? 0) / 1000)}`} sub="sats" />
          <Stat label="Lifetime" value={fmt(stats.lifetimeSats)} sub="sats" />
          <Stat label="Streak" value={`${streak}d`} sub={`${stats.tasks} tasks`} />
        </Row>
        <Button title="Withdraw" onPress={() => router.push('/payout')} />
      </Card>

      <Section title={`Last ${days} days`}>
        <Card>
          <BarChart
            width={width - space(18)}
            data={series.map((d, i) => ({ label: days <= 7 || i % 5 === 0 ? d.day.slice(8) : '', value: d.sats }))}
          />
          {!advanced && <T v="small">30-day history and per-task-type breakdown come with Advanced Analytics.</T>}
        </Card>
      </Section>

      {advanced && breakdown.length > 0 && (
        <Section title="By task type">
          <Card>
            {breakdown.map((b) => (
              <Row key={b.kind} style={{ justifyContent: 'space-between' }}>
                <T>{KIND_LABEL[b.kind]}</T>
                <T v="small">
                  {fmt(b.sats)} sats · {b.tasks} tasks
                </T>
              </Row>
            ))}
          </Card>
        </Section>
      )}

      <Section title="Badges">
        <Row style={{ flexWrap: 'wrap', gap: space(2) }}>
          {allBadges().map((b) => (
            <Pressable key={b.id} onPress={() => Alert.alert(b.title, b.description)}>
              <Pill label={b.title} tone={earned.has(b.id) ? 'accent' : 'muted'} />
            </Pressable>
          ))}
        </Row>
      </Section>

      <Section title="History">
        {ledger.length === 0 ? (
          <T v="small">No tasks yet. Completed work shows up here with its proof hash.</T>
        ) : (
          <Card style={{ gap: 0, paddingVertical: space(1) }}>
            {ledger.slice(0, 200).map((e, i) => (
              <LedgerRow key={e.id} e={e} last={i === Math.min(ledger.length, 200) - 1} />
            ))}
          </Card>
        )}
      </Section>
    </Screen>
  );
}

const STATUS: Record<LedgerEntry['status'], { label: string; tone: 'positive' | 'warn' | 'danger' | 'muted' }> = {
  accepted: { label: 'Verified', tone: 'positive' },
  'pending-verification': { label: 'Pending', tone: 'warn' },
  rejected: { label: 'Rejected', tone: 'danger' },
  paid: { label: 'Paid out', tone: 'muted' },
  failed: { label: 'Failed', tone: 'danger' },
};

function LedgerRow({ e, last }: { e: LedgerEntry; last: boolean }) {
  const st = STATUS[e.status];
  const title = e.kind === 'payout' ? 'Lightning payout' : e.taskKind ? KIND_LABEL[e.taskKind] : 'Adjustment';
  const showProof = () =>
    Alert.alert(
      e.kind === 'payout' ? 'Payment hash' : 'Proof of work',
      `${e.explainer ? `${e.explainer}\n\n` : ''}${e.kind === 'task' ? 'Output hash (sha256), compared against other devices that ran the same task:\n' : ''}${e.outputHash ?? '—'}\n\nPlatform fee: ${Math.floor(e.feeMsat / 1000)} sats`,
      [{ text: 'Copy', onPress: () => e.outputHash && void Clipboard.setStringAsync(e.outputHash) }, { text: 'Close' }],
    );
  return (
    <Pressable onPress={showProof} style={{ paddingVertical: space(3), borderBottomWidth: last ? 0 : 0.5, borderColor: colors.border }}>
      <Row style={{ justifyContent: 'space-between', gap: space(2) }}>
        <View style={{ flex: 1, gap: 2 }}>
          <T>{title}</T>
          <T v="small" numberOfLines={1}>
            {new Date(e.at).toLocaleString()} {e.outputHash ? `· ${e.outputHash.slice(0, 10)}…` : ''}
          </T>
        </View>
        <View style={{ alignItems: 'flex-end', gap: 4 }}>
          <T v="heading" style={{ color: e.amountMsat < 0 ? colors.muted : colors.text }}>
            {e.amountMsat < 0 ? '−' : '+'}
            {fmt(Math.abs(e.amountMsat) / 1000)}
          </T>
          <Pill label={st.label} tone={st.tone} />
        </View>
      </Row>
    </Pressable>
  );
}
