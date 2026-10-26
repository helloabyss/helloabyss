import {
  CoordinatorError,
  DestinationError,
  parseDestination,
  resolvePayParams,
  routingFeeLimit,
  type Payout,
} from '@satscompute/core';
import * as Clipboard from 'expo-clipboard';
import * as Haptics from 'expo-haptics';
import { router, useLocalSearchParams } from 'expo-router';
import { useEffect, useMemo, useState } from 'react';
import { TextInput, View } from 'react-native';
import { Banner, Button, Card, Row, Screen, T } from '../src/components/ui';
import { getRuntime, payoutLedgerEntry } from '../src/engine/runtime';
import { useApp } from '../src/state/store';
import { colors, radius, space } from '../src/theme';

type Step = 'form' | 'sending' | 'done';

/**
 * Lightning payout flow:
 *  1. destination (Lightning address / LNURL / invoice) — validated locally, then resolved
 *     against the user's wallet so typos fail here, not after funds move
 *  2. amount, with the routing-fee cap shown up front
 *  3. coordinator pays from the platform node; we show the preimage as proof of payment
 */
export default function PayoutScreen() {
  const { setup } = useLocalSearchParams<{ setup?: string }>();
  const saved = useApp((s) => s.payout);
  const balance = useApp((s) => s.balance);
  const { setPayout, upsertLedger, setBalance } = useApp.getState();

  const [dest, setDest] = useState(saved.destination ?? '');
  const [check, setCheck] = useState<{ ok: boolean; msg: string; min?: number; max?: number } | null>(null);
  const [checking, setChecking] = useState(false);
  const availableSats = Math.floor((balance?.availableMsat ?? 0) / 1000);
  const [amountText, setAmountText] = useState('');
  const [step, setStep] = useState<Step>('form');
  const [result, setResult] = useState<Payout | null>(null);
  const [error, setError] = useState<string | null>(null);
  const minSats = saved.thresholdSats;

  const parsed = useMemo(() => {
    try {
      return dest ? parseDestination(dest) : null;
    } catch {
      return null;
    }
  }, [dest]);

  // Invoice amounts are fixed; otherwise default to the max we can send after fee headroom.
  const invoiceSats = parsed?.type === 'bolt11' && parsed.amountMsat ? parsed.amountMsat / 1000 : null;
  const maxSendable = Math.max(0, availableSats - routingFeeLimit(availableSats));
  useEffect(() => {
    if (invoiceSats) setAmountText(String(invoiceSats));
    else if (!amountText && maxSendable >= minSats) setAmountText(String(maxSendable));
  }, [invoiceSats, maxSendable]); // eslint-disable-line react-hooks/exhaustive-deps

  const amount = Number(amountText) || 0;
  const fee = routingFeeLimit(amount);

  const verify = async () => {
    setChecking(true);
    setCheck(null);
    try {
      const d = parseDestination(dest);
      if (d.type === 'bolt11') {
        setCheck({ ok: true, msg: d.amountMsat ? `Invoice for ${d.amountMsat / 1000} sats.` : 'Invoice without amount — we’ll pay the amount below.' });
      } else {
        const p = await resolvePayParams(d);
        setCheck({ ok: true, msg: 'Wallet found.', min: Math.ceil(p.minSendable / 1000), max: Math.floor(p.maxSendable / 1000) });
        setPayout({ destination: d.value, verifiedAt: new Date().toISOString() });
      }
    } catch (e) {
      setCheck({ ok: false, msg: e instanceof DestinationError ? e.message : 'Could not verify that destination.' });
    } finally {
      setChecking(false);
    }
  };

  const send = async () => {
    setError(null);
    setStep('sending');
    try {
      const rt = await getRuntime();
      const p = await rt.client.requestPayout(dest.trim(), amount);
      upsertLedger(payoutLedgerEntry(p));
      setBalance(await rt.client.balance());
      setResult(p);
      setStep('done');
      void Haptics.notificationAsync(p.status === 'succeeded' ? Haptics.NotificationFeedbackType.Success : Haptics.NotificationFeedbackType.Error);
    } catch (e) {
      setError(e instanceof CoordinatorError || e instanceof Error ? e.message : String(e));
      setStep('form');
    }
  };

  if (step === 'done' && result) {
    const ok = result.status === 'succeeded';
    return (
      <Screen>
        <Card tone={ok ? 'accent' : 'danger'}>
          <T v="title">{ok ? `Sent ${result.amountSats.toLocaleString('en-US')} sats` : 'Payout failed'}</T>
          {ok ? (
            <>
              <T v="small">Routing fee: {result.routingFeeSats} sats</T>
              <T v="small">Proof of payment (preimage):</T>
              <T v="mono" selectable>
                {result.preimage}
              </T>
              <Button title="Copy preimage" kind="ghost" onPress={() => result.preimage && void Clipboard.setStringAsync(result.preimage)} />
            </>
          ) : (
            <T>{result.error ?? 'The payment did not go through. Your balance was not charged.'}</T>
          )}
        </Card>
        <Button title="Done" onPress={() => router.back()} />
      </Screen>
    );
  }

  const canSend =
    !!parsed &&
    amount >= minSats &&
    amount + fee <= availableSats &&
    (!check?.min || amount >= check.min) &&
    (!check?.max || amount <= check.max) &&
    step === 'form';

  return (
    <Screen>
      <Card>
        <T v="heading">Send to</T>
        <TextInput
          value={dest}
          onChangeText={(t) => {
            setDest(t);
            setCheck(null);
          }}
          placeholder="you@wallet.com, LNURL or invoice"
          placeholderTextColor={colors.faint}
          autoCapitalize="none"
          autoCorrect={false}
          style={inputStyle}
          accessibilityLabel="Lightning destination"
        />
        <Row style={{ gap: space(2) }}>
          <View style={{ flex: 1 }}>
            <Button title="Paste" kind="ghost" onPress={() => void Clipboard.getStringAsync().then(setDest)} />
          </View>
          <View style={{ flex: 1 }}>
            <Button title="Verify" kind="secondary" loading={checking} disabled={!parsed} onPress={() => void verify()} />
          </View>
        </Row>
        {dest.length > 4 && !parsed && <T v="small" style={{ color: colors.warn }}>That doesn’t look like a Lightning address, LNURL or invoice.</T>}
        {check && (
          <T v="small" style={{ color: check.ok ? colors.positive : colors.danger }}>
            {check.msg}
            {check.min ? ` Accepts ${check.min.toLocaleString()}–${check.max?.toLocaleString()} sats.` : ''}
          </T>
        )}
        <T v="small">Don’t have a wallet? Any Lightning wallet works — self-custodial ones (you hold the keys) are recommended.</T>
      </Card>

      {setup ? (
        <Button title="Save wallet" disabled={!check?.ok || parsed?.type === 'bolt11'} onPress={() => router.back()} />
      ) : (
        <>
          <Card>
            <T v="heading">Amount</T>
            <TextInput
              value={amountText}
              onChangeText={(t) => setAmountText(t.replace(/\D/g, ''))}
              editable={!invoiceSats}
              keyboardType="number-pad"
              style={[inputStyle, { fontSize: 28 }]}
              accessibilityLabel="Amount in sats"
            />
            <T v="small">
              Available {availableSats.toLocaleString('en-US')} sats · minimum {minSats} · routing fee up to {fee} sats (unused fee is refunded)
            </T>
          </Card>
          {availableSats < minSats + routingFeeLimit(minSats) && <Banner tone="muted" text={`You need at least ${minSats + routingFeeLimit(minSats)} sats to withdraw.`} />}
          {error && <Banner tone="danger" text={error} />}
          <Button title={`Withdraw ${amount ? amount.toLocaleString('en-US') : ''} sats`} disabled={!canSend} loading={step === 'sending'} onPress={() => void send()} />
        </>
      )}
    </Screen>
  );
}

const inputStyle = {
  color: colors.text,
  backgroundColor: colors.surfaceAlt,
  borderRadius: radius.sm,
  padding: space(3),
  fontSize: 16,
} as const;
