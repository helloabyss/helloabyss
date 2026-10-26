import { FEE_BPS, type Product } from '@satscompute/core';
import { useEffect, useState } from 'react';
import { Alert, View } from 'react-native';
import { Banner, Button, Card, Pill, Row, Screen, Section, T } from '../../src/components/ui';
import { EARNINGS_IAP_ENABLED, isMockStore, loadStoreItems, purchase, restorePurchases, type StoreItem } from '../../src/iap/purchases';
import { useApp } from '../../src/state/store';
import { space } from '../../src/theme';

const GROUPS: { id: Product['group']; title: string }[] = [
  { id: 'boost', title: 'Boosts' },
  { id: 'tier', title: 'Tiers' },
  { id: 'insight', title: 'Insights' },
  { id: 'setup', title: 'Setup' },
  { id: 'cosmetic', title: 'Themes' },
];

export default function Store() {
  const ent = useApp((s) => s.entitlements);
  const [items, setItems] = useState<StoreItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);

  const load = () => {
    setError(null);
    loadStoreItems().then(setItems, (e: Error) => setError(e.message));
  };
  useEffect(load, []);

  const owned = (p: Product) =>
    (p.id === 'analytics_pro' && ent.advancedAnalytics) ||
    (p.id === 'setup_pack' && ent.setupPack) ||
    (p.id === 'premium_tasks_monthly' && ent.premiumTasks) ||
    (p.id === 'tier_plus_monthly' && ent.feeTier === 'plus') ||
    (p.id === 'tier_pro_monthly' && ent.feeTier === 'pro') ||
    ent.cosmetics.includes(p.id);

  const buy = async (p: StoreItem) => {
    setBusy(p.id);
    try {
      await purchase(p.id);
    } catch (e) {
      const msg = (e as Error & { userCancelled?: boolean }).userCancelled ? null : (e as Error).message;
      if (msg) Alert.alert('Purchase failed', msg);
    } finally {
      setBusy(null);
    }
  };

  const boostUntil = ent.priorityBoostUntil && Date.parse(ent.priorityBoostUntil) > Date.now() ? new Date(ent.priorityBoostUntil) : null;

  return (
    <Screen>
      <T v="title">Store</T>
      <Card>
        <Row style={{ justifyContent: 'space-between' }}>
          <T>Platform fee</T>
          <T v="heading">{FEE_BPS[ent.feeTier] / 100}%</T>
        </Row>
        {boostUntil && <T v="small">Priority Boost active until {boostUntil.toLocaleString()}</T>}
        <T v="small">Nothing here guarantees earnings. Purchases change your share and priority, not how much work exists.</T>
      </Card>
      {isMockStore && <Banner tone="muted" text="Dev store: purchases are simulated and free. Add RevenueCat keys for real billing." />}
      {!EARNINGS_IAP_ENABLED && <Banner tone="muted" text="Boosts and fee tiers are not offered in this build." />}
      {error && <Banner tone="danger" text={`Store unavailable: ${error}`} action={{ label: 'Retry', onPress: load }} />}

      {items &&
        GROUPS.map((g) => {
          const list = items.filter((i) => i.group === g.id);
          if (!list.length) return null;
          return (
            <Section key={g.id} title={g.title}>
              {list.map((p) => (
                <Card key={p.id}>
                  <Row style={{ justifyContent: 'space-between', gap: space(2) }}>
                    <T v="heading" style={{ flex: 1 }}>
                      {p.title}
                    </T>
                    {owned(p) ? <Pill label="Owned" tone="positive" /> : <T v="heading">{p.price}</T>}
                  </Row>
                  <T v="small">{p.description}</T>
                  {!owned(p) && (
                    <View style={{ marginTop: space(1) }}>
                      <Button title={p.type === 'subscription' ? 'Subscribe' : 'Buy'} kind="secondary" loading={busy === p.id} onPress={() => void buy(p)} />
                    </View>
                  )}
                </Card>
              ))}
            </Section>
          );
        })}

      <Button title="Restore purchases" kind="ghost" onPress={() => void restorePurchases().catch((e: Error) => Alert.alert('Restore failed', e.message))} />
    </Screen>
  );
}
