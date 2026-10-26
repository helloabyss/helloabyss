/** Dark-first, minimal. One warm accent (sats orange); everything else is neutral. */
export const colors = {
  bg: '#0B0D10',
  surface: '#14181D',
  surfaceAlt: '#1B2027',
  border: '#262C35',
  text: '#E9EDF2',
  muted: '#8A94A3',
  faint: '#5B6472',
  accent: '#F7931A',
  accentDim: '#3A2610',
  positive: '#3DDC97',
  warn: '#F5B841',
  danger: '#FF5C5C',
} as const;

export const space = (n: number) => n * 4;

export const radius = { sm: 8, md: 14, lg: 20 } as const;

export const type = {
  display: { fontSize: 40, fontWeight: '700' as const, letterSpacing: -1, color: colors.text },
  title: { fontSize: 22, fontWeight: '700' as const, color: colors.text },
  heading: { fontSize: 16, fontWeight: '600' as const, color: colors.text },
  body: { fontSize: 15, color: colors.text, lineHeight: 21 },
  small: { fontSize: 13, color: colors.muted, lineHeight: 18 },
  mono: { fontSize: 12, color: colors.muted, fontFamily: 'Menlo' },
} as const;
