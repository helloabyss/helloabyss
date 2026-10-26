import { View } from 'react-native';
import Svg, { Rect, Text as SvgText } from 'react-native-svg';
import { colors } from '../theme';

export function BarChart({ data, height = 120, width = 320 }: { data: { label: string; value: number }[]; height?: number; width?: number }) {
  const max = Math.max(1, ...data.map((d) => d.value));
  const gap = 6;
  const bw = (width - gap * (data.length - 1)) / Math.max(1, data.length);
  const chartH = height - 18;
  return (
    <View accessible accessibilityLabel={`Bar chart: ${data.map((d) => `${d.label} ${d.value}`).join(', ')}`}>
      <Svg width={width} height={height}>
        {data.map((d, i) => {
          const h = Math.max(d.value > 0 ? 3 : 1, (d.value / max) * chartH);
          const x = i * (bw + gap);
          return (
            <Rect key={d.label} x={x} y={chartH - h} width={bw} height={h} rx={3} fill={d.value > 0 ? colors.accent : colors.border} />
          );
        })}
        {data.map((d, i) => (
          <SvgText key={`l${d.label}`} x={i * (bw + gap) + bw / 2} y={height - 4} fontSize={10} fill={colors.faint} textAnchor="middle">
            {d.label}
          </SvgText>
        ))}
      </Svg>
    </View>
  );
}
