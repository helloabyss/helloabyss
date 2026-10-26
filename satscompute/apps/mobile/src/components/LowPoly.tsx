import { memo, useMemo } from 'react';
import { useWindowDimensions, type ViewStyle } from 'react-native';
import Svg, { Polygon } from 'react-native-svg';
import { colors } from '../theme';

/** Deterministic low-poly backdrop: a jittered triangle grid in near-black tones. Static, zero animation cost. */
function LowPolyImpl({ style, intensity = 1 }: { style?: ViewStyle; intensity?: number }) {
  const { width, height } = useWindowDimensions();
  const tris = useMemo(() => {
    const cols = 6;
    const rows = Math.ceil((height / width) * cols) + 1;
    const cw = width / cols;
    const rh = height / (rows - 1);
    let seed = 7;
    const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const pts: [number, number][][] = [];
    for (let r = 0; r < rows; r++) {
      pts.push([]);
      for (let c = 0; c <= cols; c++) {
        const edge = r === 0 || r === rows - 1 || c === 0 || c === cols;
        pts[r]!.push([c * cw + (edge ? 0 : (rnd() - 0.5) * cw * 0.7), r * rh + (edge ? 0 : (rnd() - 0.5) * rh * 0.7)]);
      }
    }
    const out: { points: string; opacity: number; warm: boolean }[] = [];
    for (let r = 0; r < rows - 1; r++) {
      for (let c = 0; c < cols; c++) {
        const a = pts[r]![c]!;
        const b = pts[r]![c + 1]!;
        const d = pts[r + 1]![c]!;
        const e = pts[r + 1]![c + 1]!;
        const fmt = (...p: [number, number][]) => p.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(' ');
        // Fade out towards the bottom so content stays readable.
        const fade = 1 - r / rows;
        out.push({ points: fmt(a, b, e), opacity: (0.04 + rnd() * 0.08) * fade * intensity, warm: rnd() > 0.93 });
        out.push({ points: fmt(a, e, d), opacity: (0.04 + rnd() * 0.08) * fade * intensity, warm: false });
      }
    }
    return out;
  }, [width, height, intensity]);

  return (
    <Svg width={width} height={height} style={style} pointerEvents="none">
      {tris.map((t, i) => (
        <Polygon key={i} points={t.points} fill={t.warm ? colors.accent : '#9FB3C8'} fillOpacity={t.warm ? t.opacity * 0.8 : t.opacity} />
      ))}
    </Svg>
  );
}

export const LowPoly = memo(LowPolyImpl);
