# Footage — The Daily Reset

Licensed Adobe Stock video. The files themselves are gitignored: the licence
covers use in a work, not redistribution, and this repo may be public. Asset
IDs and the exact ingest settings are here so the set can be re-sourced.

Ingested with `engine/getplate.sh <outdir> <NAME> <url> [trim] [brightness] [saturation]`.

| Plate | Asset | What it is | Ingest |
|---|---|---|---|
| `WATCH` | 326949375 | Vintage watch movement, macro, native B&W. **The hero.** The daily reset made literal — a mechanism that returns to the same place every cycle | `6 0.02` |
| `HAND` | 991749818 | Watch second hand sweeping. The reset ticking over | `6 0.15` |
| `CANDLE` | 806079575 | Candlestick chart, **native 1080×1920** so no crop loss | `6 0.12`, then forced monochrome |
| `FALL` | 642051546 | Declining chart on an LED screen, macro | `6 0.17`, then forced monochrome |

## Two grading notes worth keeping

**Trading-screen footage needs a brightness LIFT, not a cut.** Three of these four were
rejected by `checkplate.py` on the first pass at mean luma 2.6–4.7. Chart UI is black
background with thin bright strokes, so the house −0.13 brightness crushes it to nothing.
They ingest at **+0.12 to +0.17**. The archive and data-centre plates on the other short
needed the opposite.

**Chart footage arrives coloured and it has to be taken out.** `CANDLE` came in with green
and purple series, `FALL` with pink. `STYLE-GUIDE.md`: *"Red is reserved for graphics and
type. Footage must never turn the piece into a colourful stock reel."* Both are forced to
`hue=s=0.05` so they read near-monochrome and the only colour on screen is our own red,
carried by the panels and type. Measured saturation spread after: 4.7 and 5.4, against
2.9 for the natively black-and-white watch plate.
