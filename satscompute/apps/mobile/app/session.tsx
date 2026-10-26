import { KIND_LABEL, REASON_COPY } from '@satscompute/core';
import { useKeepAwake } from 'expo-keep-awake';
import { router } from 'expo-router';
import { useEffect, useRef } from 'react';
import { Animated, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LowPoly } from '../src/components/LowPoly';
import { phaseCopy } from '../src/components/phase';
import { Button, Progress, T } from '../src/components/ui';
import { setNightstandActive } from '../src/device/sensor';
import { useEngine } from '../src/engine/useEngine';
import { colors, space } from '../src/theme';

/**
 * Nightstand session: the primary way a phone contributes. The user starts it, plugs in and
 * puts the phone down. Screen stays on but nearly black (OLED ≈ no power), content dims after
 * a few seconds. Guardrails keep running every couple of seconds; leaving the screen stops work.
 */
export default function Session() {
  useKeepAwake();
  const { runtime, snap } = useEngine();
  const dim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (!runtime) return;
    setNightstandActive(true);
    void runtime.engine.start();
    return () => {
      setNightstandActive(false);
      void runtime.engine.stop();
      void runtime.refresh();
    };
  }, [runtime]);

  const wake = () => {
    dim.setValue(1);
    Animated.timing(dim, { toValue: 0.25, duration: 800, delay: 6000, useNativeDriver: true }).start();
  };
  useEffect(wake, [dim]);

  const phase = phaseCopy(snap);
  const sats = Math.floor((snap?.session.creditedMsat ?? 0) / 1000);
  const pending = Math.floor((snap?.session.pendingMsat ?? 0) / 1000);

  return (
    <View style={styles.root} onTouchStart={wake}>
      <LowPoly style={StyleSheet.absoluteFill} intensity={0.5} />
      <SafeAreaView style={styles.safe}>
        <Animated.View style={[styles.center, { opacity: dim }]}>
          <T v="small" style={{ color: phase.tone === 'warn' ? colors.warn : colors.muted }}>
            {phase.label}
          </T>
          <T v="display" style={{ fontSize: 64 }}>
            {sats.toLocaleString('en-US')}
          </T>
          <T v="small">sats this session{pending ? ` · +${pending} pending` : ''}</T>

          <View style={styles.status}>
            {snap?.current ? (
              <>
                <T v="heading">{KIND_LABEL[snap.current.task.kind]}</T>
                <T v="small" style={{ textAlign: 'center' }}>
                  {snap.current.task.explainer}
                </T>
                <Progress value={snap.current.progress} />
              </>
            ) : snap?.phase === 'blocked' ? (
              snap.reasons.map((r) => (
                <T key={r} v="small" style={{ textAlign: 'center' }}>
                  {REASON_COPY[r]}
                </T>
              ))
            ) : snap?.phase === 'waiting-for-work' ? (
              <T v="small">Waiting for a task…</T>
            ) : snap?.lastError ? (
              <T v="small" style={{ color: colors.warn }}>
                {snap.lastError}
              </T>
            ) : null}
          </View>

          <T v="small" style={{ color: colors.faint }}>
            {snap?.session.tasksCompleted ?? 0} tasks · stops automatically if the phone gets warm or unplugged
          </T>
        </Animated.View>
        <Button title="Stop" kind="ghost" onPress={() => router.back()} />
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#000' },
  safe: { flex: 1, padding: space(6), justifyContent: 'space-between' },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: space(3) },
  status: { width: '100%', gap: space(2), alignItems: 'center', minHeight: 90, marginTop: space(6) },
});
