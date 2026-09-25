// Stand-in subject drawings for mockups. They show composition and scale only;
// the final thumbnail swaps in one generated photo (see `finalImage` in the spec).
// All viewBoxes are 1000x1100 so presets are interchangeable.

const defs = `<defs>
  <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6b6b70"/><stop offset=".45" stop-color="#2c2c30"/>
    <stop offset="1" stop-color="#111113"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#3a3a3e"/><stop offset=".35" stop-color="#050506"/>
    <stop offset="1" stop-color="#18181a"/></linearGradient>
  <radialGradient id="floor" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#000" stop-opacity=".7"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>`;

const shadow = (cx, cy, rx, ry) =>
  `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="url(#floor)"/>`;

const svg = (body) => `<svg viewBox="0 0 1000 1100" xmlns="http://www.w3.org/2000/svg">${defs}${body}</svg>`;

const glasses = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})">
  <path d="M40 60 L620 60 Q650 60 650 90 L650 230 Q650 260 620 260 L380 260 Q345 260 330 225
    Q322 205 300 205 Q278 205 270 225 Q255 260 220 260 L40 260 Q10 260 10 230 L10 90 Q10 60 40 60Z"
    fill="url(#metal)" stroke="#8d8d92" stroke-width="3"/>
  <path d="M40 82 L618 82 Q628 82 628 92 L628 228 Q628 240 616 240 L385 240 Q360 240 348 212
    Q334 185 300 185 Q266 185 252 212 Q240 240 215 240 L44 240 Q32 240 32 228 L32 92 Q32 82 40 82Z"
    fill="url(#glass)"/>
  <path d="M60 95 L300 95 L200 150 Z" fill="#fff" opacity=".07"/>
  <circle cx="45" cy="98" r="15" fill="#050506" stroke="#9a9aa0" stroke-width="3"/>
  <circle cx="615" cy="98" r="15" fill="#050506" stroke="#9a9aa0" stroke-width="3"/>
  <path d="M650 80 L900 30 Q925 26 928 48 L930 70 L660 130 Z" fill="url(#metal)" stroke="#8d8d92" stroke-width="3"/>
  <circle cx="790" cy="78" r="8" fill="#050506" stroke="#9a9aa0" stroke-width="2"/>
</g>`;

const cable = (d) => `<path d="${d}" fill="none" stroke="#1a1a1c" stroke-width="10" stroke-linecap="round"/>
  <path d="${d}" fill="none" stroke="#55555a" stroke-width="2" stroke-linecap="round" opacity=".6"/>`;

const puck = (x, y) => `<g transform="translate(${x} ${y})">
  ${shadow(130, 95, 170, 30)}
  <rect x="0" y="0" width="260" height="90" rx="26" fill="url(#metal)" stroke="#6a6a70" stroke-width="3"/>
  <rect x="14" y="10" width="232" height="20" rx="10" fill="#fff" opacity=".06"/></g>`;

const headset = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})">
  ${shadow(330, 420, 360, 50)}
  <path d="M40 140 Q40 60 140 60 L520 60 Q620 60 620 140 L620 330 Q620 400 540 400 L120 400 Q40 400 40 330Z"
    fill="url(#metal)" stroke="#77777c" stroke-width="4"/>
  <rect x="80" y="100" width="500" height="250" rx="60" fill="url(#glass)"/>
  <path d="M40 180 Q-40 200 -30 320 M620 180 Q700 200 690 320" stroke="#2a2a2e" stroke-width="40" fill="none" stroke-linecap="round"/>
  <path d="M120 60 Q330 -70 540 60" stroke="#2a2a2e" stroke-width="44" fill="none"/></g>`;

const crack = `<path d="M470 520 L500 600 L455 660 L510 740 L480 820" stroke="#d7141e" stroke-width="10" fill="none" stroke-linejoin="bevel"/>`;

export const SUBJECTS = {
  none: '',
  // Slim VR glasses tethered to a compute puck (Meta VR Glasses shape, unbranded).
  'vr-glasses': svg(`<g transform="translate(-110 -120) scale(1.22)">${shadow(500, 640, 360, 40)}${glasses(165, 420)}
    ${cable('M820 485 Q930 600 820 760 Q760 850 640 880')}${puck(380, 850)}</g>`),
  // Bulky headset alone.
  headset: svg(headset(170, 380)),
  // Bulky headset cracked (red fracture), slim glasses floating above it.
  'headset-vs-glasses': svg(`${glasses(170, 170, .95)}${headset(170, 560, .95)}${crack}`),
  // Glasses on a scale reading a value.
  'glasses-on-scale': svg(`${shadow(500, 930, 420, 40)}
    <rect x="130" y="700" width="740" height="210" rx="30" fill="url(#metal)" stroke="#77777c" stroke-width="4"/>
    <rect x="360" y="780" width="280" height="95" rx="10" fill="#050506" stroke="#444" stroke-width="3"/>
    <text x="500" y="855" text-anchor="middle" font-family="Anton" font-size="78" fill="#f4f4f2">100g</text>
    ${glasses(170, 470, .95)}`),
  // Big red loss bar crashing through the floor next to a small bar.
  'chart-drop': svg(`<line x1="100" y1="700" x2="900" y2="700" stroke="#f4f4f2" stroke-width="6"/>
    <rect x="220" y="560" width="200" height="140" fill="#f4f4f2"/>
    <rect x="560" y="700" width="220" height="360" fill="#d7141e"/>
    <path d="M560 700 L600 740 L640 705 L690 750 L730 710 L780 745" stroke="#0b0b0c" stroke-width="10" fill="none"/>`),
};
