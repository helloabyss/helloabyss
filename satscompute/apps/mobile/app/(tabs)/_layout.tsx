import { Redirect, Tabs } from 'expo-router';
import { Text, type ColorValue } from 'react-native';
import { useApp } from '../../src/state/store';
import { colors } from '../../src/theme';

// Text glyphs keep the bundle free of an icon font; swap for an icon set if desired.
const icon = (glyph: string) => ({ color }: { color: ColorValue }) => <Text style={{ color, fontSize: 18 }}>{glyph}</Text>;

export default function TabsLayout() {
  const onboarded = useApp((s) => s.onboarded);
  if (!onboarded) return <Redirect href="/onboarding" />;
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: { backgroundColor: colors.bg, borderTopColor: colors.border },
        tabBarActiveTintColor: colors.accent,
        tabBarInactiveTintColor: colors.faint,
      }}
    >
      <Tabs.Screen name="index" options={{ title: 'Dashboard', tabBarIcon: icon('◆') }} />
      <Tabs.Screen name="controls" options={{ title: 'Controls', tabBarIcon: icon('◐') }} />
      <Tabs.Screen name="earnings" options={{ title: 'Earnings', tabBarIcon: icon('▤') }} />
      <Tabs.Screen name="store" options={{ title: 'Store', tabBarIcon: icon('◇') }} />
      <Tabs.Screen name="settings" options={{ title: 'Settings', tabBarIcon: icon('≡') }} />
    </Tabs>
  );
}
