import '../src/engine/background'; // registers the TaskManager task at module load
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { AppState, View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { flushAnalytics } from '../src/analytics';
import { syncBackgroundRegistration } from '../src/engine/background';
import { useApp } from '../src/state/store';
import { colors } from '../src/theme';

export default function RootLayout() {
  const hydrated = useApp((s) => s.hydrated);
  const enabled = useApp((s) => s.policy.enabled);

  useEffect(() => {
    if (hydrated) void syncBackgroundRegistration(enabled).catch(() => {});
  }, [hydrated, enabled]);

  useEffect(() => {
    const sub = AppState.addEventListener('change', (st) => st === 'background' && void flushAnalytics());
    return () => sub.remove();
  }, []);

  if (!hydrated) return <View style={{ flex: 1, backgroundColor: colors.bg }} />;

  return (
    <SafeAreaProvider>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: colors.bg },
          headerTintColor: colors.text,
          headerShadowVisible: false,
          contentStyle: { backgroundColor: colors.bg },
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="onboarding" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="session" options={{ headerShown: false, presentation: 'fullScreenModal' }} />
        <Stack.Screen name="payout" options={{ title: 'Withdraw', presentation: 'modal' }} />
        <Stack.Screen name="bitcoin" options={{ title: 'Bitcoin mode' }} />
      </Stack>
    </SafeAreaProvider>
  );
}
