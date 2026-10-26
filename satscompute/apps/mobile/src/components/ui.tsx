import type { ReactNode } from 'react';
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, Switch, Text, View, type TextStyle, type ViewStyle } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, radius, space, type } from '../theme';
import { LowPoly } from './LowPoly';

export function Screen({ children, scroll = true, backdrop = true }: { children: ReactNode; scroll?: boolean; backdrop?: boolean }) {
  return (
    <SafeAreaView style={s.screen} edges={['top', 'left', 'right']}>
      {backdrop && <LowPoly style={StyleSheet.absoluteFill} />}
      {scroll ? <ScrollView contentContainerStyle={s.scroll}>{children}</ScrollView> : <View style={[s.scroll, { flex: 1 }]}>{children}</View>}
    </SafeAreaView>
  );
}

export function T({ v = 'body', style, children, ...rest }: { v?: keyof typeof type; style?: TextStyle; children: ReactNode; numberOfLines?: number; selectable?: boolean }) {
  return (
    <Text style={[type[v], style]} {...rest}>
      {children}
    </Text>
  );
}

export function Card({ children, style, tone }: { children: ReactNode; style?: ViewStyle; tone?: 'accent' | 'warn' | 'danger' }) {
  const border = tone === 'accent' ? colors.accent : tone === 'warn' ? colors.warn : tone === 'danger' ? colors.danger : colors.border;
  return <View style={[s.card, { borderColor: border }, style]}>{children}</View>;
}

export function Section({ title, children, right }: { title: string; children: ReactNode; right?: ReactNode }) {
  return (
    <View style={{ gap: space(2) }}>
      <View style={s.row}>
        <T v="small" style={{ textTransform: 'uppercase', letterSpacing: 1, flex: 1 }}>
          {title}
        </T>
        {right}
      </View>
      {children}
    </View>
  );
}

export function Button({
  title,
  onPress,
  kind = 'primary',
  disabled,
  loading,
}: {
  title: string;
  onPress: () => void;
  kind?: 'primary' | 'secondary' | 'ghost' | 'danger';
  disabled?: boolean;
  loading?: boolean;
}) {
  const bg = kind === 'primary' ? colors.accent : kind === 'danger' ? colors.danger : kind === 'secondary' ? colors.surfaceAlt : 'transparent';
  const fg = kind === 'primary' || kind === 'danger' ? '#111' : colors.text;
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ disabled: disabled || loading }}
      onPress={onPress}
      disabled={disabled || loading}
      style={({ pressed }) => [s.button, { backgroundColor: bg, opacity: disabled ? 0.4 : pressed ? 0.8 : 1 }, kind === 'ghost' && s.ghost]}
    >
      {loading ? <ActivityIndicator color={fg} /> : <Text style={[type.heading, { color: fg }]}>{title}</Text>}
    </Pressable>
  );
}

export function ToggleRow({ label, hint, value, onChange, disabled }: { label: string; hint?: string; value: boolean; onChange: (v: boolean) => void; disabled?: boolean }) {
  return (
    <View style={[s.row, s.settingRow]}>
      <View style={{ flex: 1, gap: 2 }}>
        <T>{label}</T>
        {hint ? <T v="small">{hint}</T> : null}
      </View>
      <Switch
        accessibilityLabel={label}
        value={value}
        onValueChange={onChange}
        disabled={disabled}
        trackColor={{ true: colors.accent, false: colors.border }}
        thumbColor={colors.text}
      />
    </View>
  );
}

/** Discrete stepper — safer than a slider for limits (no accidental drags to 100%). */
export function Stepper({
  label,
  hint,
  value,
  onChange,
  step,
  min,
  max,
  format = String,
}: {
  label: string;
  hint?: string;
  value: number;
  onChange: (v: number) => void;
  step: number;
  min: number;
  max: number;
  format?: (v: number) => string;
}) {
  const set = (v: number) => onChange(Math.min(max, Math.max(min, Math.round(v / step) * step)));
  return (
    <View style={[s.row, s.settingRow]}>
      <View style={{ flex: 1, gap: 2 }}>
        <T>{label}</T>
        {hint ? <T v="small">{hint}</T> : null}
      </View>
      <View style={[s.row, { gap: space(2) }]}>
        <StepBtn label="−" onPress={() => set(value - step)} disabled={value <= min} a11y={`Decrease ${label}`} />
        <T v="heading" style={{ minWidth: 56, textAlign: 'center' }}>
          {format(value)}
        </T>
        <StepBtn label="+" onPress={() => set(value + step)} disabled={value >= max} a11y={`Increase ${label}`} />
      </View>
    </View>
  );
}

function StepBtn({ label, onPress, disabled, a11y }: { label: string; onPress: () => void; disabled: boolean; a11y: string }) {
  return (
    <Pressable accessibilityLabel={a11y} onPress={onPress} disabled={disabled} style={[s.step, disabled && { opacity: 0.3 }]}>
      <Text style={[type.title, { lineHeight: 24 }]}>{label}</Text>
    </Pressable>
  );
}

export function Pill({ label, tone = 'muted' }: { label: string; tone?: 'muted' | 'accent' | 'positive' | 'warn' | 'danger' }) {
  const c = tone === 'muted' ? colors.muted : colors[tone];
  return (
    <View style={[s.pill, { borderColor: c }]}>
      <Text style={[type.small, { color: c, fontWeight: '600' }]}>{label}</Text>
    </View>
  );
}

export function Progress({ value }: { value: number }) {
  return (
    <View style={s.track} accessibilityRole="progressbar" accessibilityValue={{ min: 0, max: 100, now: Math.round(value * 100) }}>
      <View style={[s.fill, { width: `${Math.round(Math.min(1, Math.max(0, value)) * 100)}%` }]} />
    </View>
  );
}

export function Stat({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <View style={{ flex: 1, gap: 2 }}>
      <T v="small">{label}</T>
      <T v="title">{value}</T>
      {sub ? <T v="small">{sub}</T> : null}
    </View>
  );
}

export function Banner({ text, tone = 'warn', action }: { text: string; tone?: 'warn' | 'danger' | 'muted'; action?: { label: string; onPress: () => void } }) {
  const c = tone === 'muted' ? colors.muted : colors[tone];
  return (
    <View style={[s.banner, { borderColor: c }]} accessibilityRole="alert">
      <T style={{ flex: 1, color: c }}>{text}</T>
      {action && (
        <Pressable onPress={action.onPress} hitSlop={8}>
          <T v="heading" style={{ color: c }}>
            {action.label}
          </T>
        </Pressable>
      )}
    </View>
  );
}

export const Row = ({ children, style }: { children: ReactNode; style?: ViewStyle }) => <View style={[s.row, style]}>{children}</View>;

export const s = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  scroll: { padding: space(5), gap: space(5), paddingBottom: space(12) },
  card: { backgroundColor: colors.surface, borderRadius: radius.lg, borderWidth: StyleSheet.hairlineWidth, padding: space(4), gap: space(3) },
  row: { flexDirection: 'row', alignItems: 'center' },
  settingRow: { paddingVertical: space(2), gap: space(3) },
  button: { height: 52, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center', paddingHorizontal: space(5) },
  ghost: { borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border },
  step: { width: 36, height: 36, borderRadius: 18, backgroundColor: colors.surfaceAlt, alignItems: 'center', justifyContent: 'center' },
  pill: { borderWidth: 1, borderRadius: 999, paddingHorizontal: space(2.5), paddingVertical: 2, alignSelf: 'flex-start' },
  track: { height: 6, backgroundColor: colors.surfaceAlt, borderRadius: 3, overflow: 'hidden' },
  fill: { height: 6, backgroundColor: colors.accent, borderRadius: 3 },
  banner: { flexDirection: 'row', alignItems: 'center', gap: space(3), borderWidth: 1, borderRadius: radius.md, padding: space(3) },
});
