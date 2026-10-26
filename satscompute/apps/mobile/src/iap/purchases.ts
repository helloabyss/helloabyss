import { applyPurchase, PRODUCTS, type Entitlements, type Product, type ProductId } from '@satscompute/core';
import { Platform } from 'react-native';
import { analytics } from '../analytics';
import { getRuntime, isMockBackend } from '../engine/runtime';
import { useApp } from '../state/store';

/**
 * Store purchases via RevenueCat (StoreKit 2 / Play Billing). The coordinator learns about a
 * purchase from RevenueCat's webhook and is the source of truth for entitlements; the app just
 * re-fetches them. Without RevenueCat keys we run a dev mock that grants locally.
 */

export const EARNINGS_IAP_ENABLED = process.env.EXPO_PUBLIC_EARNINGS_IAP_ENABLED === 'true';

const RC_KEY = Platform.OS === 'ios' ? process.env.EXPO_PUBLIC_REVENUECAT_IOS_KEY : process.env.EXPO_PUBLIC_REVENUECAT_ANDROID_KEY;
export const isMockStore = !RC_KEY;

export interface StoreItem extends Product {
  price: string;
}

export function visibleProducts(): Product[] {
  return PRODUCTS.filter((p) => EARNINGS_IAP_ENABLED || !p.affectsEarnings);
}

let configured = false;
async function purchasesSdk() {
  const { default: Purchases } = await import('react-native-purchases');
  if (!configured) {
    const rt = await getRuntime();
    Purchases.configure({ apiKey: RC_KEY!, appUserID: rt.accountId || null });
    configured = true;
  }
  return Purchases;
}

export async function loadStoreItems(): Promise<StoreItem[]> {
  const products = visibleProducts();
  if (isMockStore) return products.map((p) => ({ ...p, price: p.fallbackPrice }));
  const Purchases = await purchasesSdk();
  const live = await Purchases.getProducts(products.map((p) => p.id));
  return products.map((p) => ({ ...p, price: live.find((l) => l.identifier === p.id)?.priceString ?? p.fallbackPrice }));
}

export async function purchase(id: ProductId): Promise<Entitlements> {
  analytics.track({ type: 'iap', product: id });
  const s = useApp.getState();
  if (isMockStore) {
    if (!__DEV__) throw new Error('Store is not configured');
    const next = applyPurchase(s.entitlements, id, new Date());
    s.setEntitlements(next);
    return next;
  }
  const Purchases = await purchasesSdk();
  const [product] = await Purchases.getProducts([id]);
  if (!product) throw new Error('Product unavailable in this store');
  await Purchases.purchaseStoreProduct(product);
  return refreshEntitlementsAfterPurchase();
}

export async function restorePurchases(): Promise<Entitlements> {
  if (isMockStore) return useApp.getState().entitlements;
  const Purchases = await purchasesSdk();
  await Purchases.restorePurchases();
  return refreshEntitlementsAfterPurchase();
}

/** Webhook → coordinator is async; poll briefly. */
async function refreshEntitlementsAfterPurchase(): Promise<Entitlements> {
  const rt = await getRuntime();
  let ent = useApp.getState().entitlements;
  for (let i = 0; i < 5; i++) {
    ent = await rt.client.entitlements();
    if (JSON.stringify(ent) !== JSON.stringify(useApp.getState().entitlements)) break;
    await new Promise((r) => setTimeout(r, 1500));
  }
  if (!isMockBackend) useApp.getState().setEntitlements(ent);
  return ent;
}
