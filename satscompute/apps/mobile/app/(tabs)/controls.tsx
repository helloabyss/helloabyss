import { KIND_EXPLAINER, KIND_LABEL, parseHm, type TaskKind } from '@satscompute/core';
import { router } from 'expo-router';
import { Alert, Pressable } from 'react-native';
import { Banner, Card, Pill, Row, Screen, Section, Stepper, T, ToggleRow } from '../../src/components/ui';
import { hasNativeThermal } from '../../modules/thermal-state';
import { useApp } from '../../src/state/store';
import { space } from '../../src/theme';

const KINDS: TaskKind[] = ['embedding', 'classification', 'filter', 'verification'];
const hhmm = (min: number) => `${String(Math.floor(min / 60)).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;

export default function Controls() {
  const policy = useApp((s) => s.policy);
  const setPolicy = useApp((s) => s.setPolicy);
  const premium = useApp((s) => s.entitlements.premiumTasks);

  const toggleMaster = (on: boolean) => {
    if (!on) return setPolicy({ enabled: false });
    Alert.alert(
      'Share idle compute?',
      `Your device will run small AI tasks for paying customers within the limits below. Task data is processed on-device and the result is sent back to the SatsCompute coordinator. You can turn this off at any time.`,
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Turn on', onPress: () => setPolicy({ enabled: true }) },
      ],
    );
  };

  const toggleKind = (k: TaskKind, on: boolean) =>
    setPolicy({ allowedKinds: on ? [...new Set([...policy.allowedKinds, k])] : policy.allowedKinds.filter((x) => x !== k) });

  return (
    <Screen>
      <T v="title">Contribution controls</T>
      <Card tone={policy.enabled ? 'accent' : undefined}>
        <ToggleRow label="Share idle compute" hint="Master switch. Nothing runs while this is off." value={policy.enabled} onChange={toggleMaster} />
      </Card>

      <Section title="When">
        <Card>
          <ToggleRow
            label="Only while charging"
            hint={policy.onlyWhenCharging ? 'Recommended for phones.' : 'Work runs at half speed on battery and stops at your minimum.'}
            value={policy.onlyWhenCharging}
            onChange={(v) => setPolicy({ onlyWhenCharging: v })}
          />
          <ToggleRow label="Only on Wi-Fi" hint="Tasks are small (KBs), but this avoids any mobile data use." value={policy.onlyOnWifi} onChange={(v) => setPolicy({ onlyOnWifi: v })} />
          {!policy.onlyOnWifi && (
            <Stepper label="Mobile data cap" hint="Per month" value={policy.cellularDataCapMb} step={25} min={0} max={500} format={(v) => `${v} MB`} onChange={(v) => setPolicy({ cellularDataCapMb: v })} />
          )}
          <ToggleRow
            label="Quiet hours"
            hint="Pause during these hours (e.g. while you use the phone at work)."
            value={policy.quietHours.enabled}
            onChange={(v) => setPolicy({ quietHours: { ...policy.quietHours, enabled: v } })}
          />
          {policy.quietHours.enabled && (
            <>
              <Stepper
                label="From"
                value={parseHm(policy.quietHours.start)}
                step={30}
                min={0}
                max={1410}
                format={hhmm}
                onChange={(v) => setPolicy({ quietHours: { ...policy.quietHours, start: hhmm(v) } })}
              />
              <Stepper
                label="Until"
                value={parseHm(policy.quietHours.end)}
                step={30}
                min={0}
                max={1410}
                format={hhmm}
                onChange={(v) => setPolicy({ quietHours: { ...policy.quietHours, end: hhmm(v) } })}
              />
            </>
          )}
        </Card>
      </Section>

      <Section title="Limits">
        <Card>
          <Stepper
            label="Max CPU use"
            hint="Share of time the worker may be busy. It rests in between."
            value={policy.maxCpuPercent}
            step={10}
            min={10}
            max={100}
            format={(v) => `${v}%`}
            onChange={(v) => setPolicy({ maxCpuPercent: v })}
          />
          <Stepper
            label="Minimum battery"
            value={Math.round(policy.minBatteryLevel * 100)}
            step={5}
            min={20}
            max={100}
            format={(v) => `${v}%`}
            onChange={(v) => setPolicy({ minBatteryLevel: v / 100 })}
          />
          <Stepper
            label="Battery temperature limit"
            hint="Android only — iOS doesn't expose battery temperature."
            value={policy.maxBatteryTempC}
            step={1}
            min={30}
            max={42}
            format={(v) => `${v}°C`}
            onChange={(v) => setPolicy({ maxBatteryTempC: v })}
          />
          <T>Stop when the device is</T>
          <Row style={{ gap: space(2) }}>
            {(['nominal', 'fair'] as const).map((t) => (
              <Pressable key={t} onPress={() => setPolicy({ maxThermal: t })} accessibilityRole="radio" accessibilityState={{ selected: policy.maxThermal === t }}>
                <Pill label={t === 'nominal' ? 'Slightly warm (strict)' : 'Warm (default)'} tone={policy.maxThermal === t ? 'accent' : 'muted'} />
              </Pressable>
            ))}
          </Row>
          {!hasNativeThermal && <Banner tone="muted" text="Thermal sensor unavailable in this build (Expo Go). Work runs at half speed as a precaution." />}
        </Card>
      </Section>

      <Section title="Task types">
        <Card>
          {KINDS.map((k) => (
            <ToggleRow key={k} label={KIND_LABEL[k]} hint={KIND_EXPLAINER[k]} value={policy.allowedKinds.includes(k)} onChange={(v) => toggleKind(k, v)} />
          ))}
          <ToggleRow
            label={KIND_LABEL['llm-small']}
            hint={premium ? KIND_EXPLAINER['llm-small'] : 'Premium task type. Requires an on-device model runtime (coming with the desktop agent first).'}
            value={policy.allowedKinds.includes('llm-small')}
            disabled={!premium}
            onChange={(v) => toggleKind('llm-small', v)}
          />
        </Card>
      </Section>

      <Section title="Support Bitcoin">
        <Card>
          <T>Bitcoin mode verifies recent block headers yourself instead of trusting an API. It does not mine and does not earn sats.</T>
          <Pressable onPress={() => router.push('/bitcoin')}>
            <T v="heading" style={{ color: '#F7931A' }}>
              Open Bitcoin mode →
            </T>
          </Pressable>
        </Card>
      </Section>
    </Screen>
  );
}
