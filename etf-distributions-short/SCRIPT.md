# YouTube Short — "Paid Every Week… Still Losing Money?"

**Runtime target:** 70–78s · **Format:** 1080x1920 (9:16) · **Style:** faceless, imagery-first
**Voice:** Alex Wright – Informative · dry, confident, analytical newsroom

---

## VO SCRIPT (191 words)

**[HOOK]**
> Your ETF paid you a hundred dollars. You can still be poorer.

**[SET UP THE HYPOTHETICAL]**
> Start with a thousand dollars. Over the year the fund pays you a hundred. You feel
> paid. But the share price fell — your thousand is now worth eight hundred and fifty.

**[THE MATH]**
> Eight fifty in the fund, plus a hundred in your pocket, is nine hundred and fifty.
> You got paid, and you lost fifty dollars.

**[DEFINE THE TWO NUMBERS]**
> That gap has a name. The distribution rate is what the fund hands you. Total return is
> price change plus distributions — what you actually earned. Only one of those is your result.

**[THE EVIDENCE — the fund says it itself]**
> YieldMax says it in its own disclosure: the distribution rate does not represent its total
> return. And it publishes what's inside each payment. On September second, MSTY's
> distribution was disclosed as almost ninety-nine percent estimated return of capital —
> barely any of it income. Most of that money was already yours.

**[THE TAX MECHANISM]**
> Return of capital isn't taxed as income. It cuts your cost basis, so the bill waits for
> you at the sale.

**[THE HONEST COUNTER — mandatory beat]**
> The honest counter: a falling price isn't automatically a loss. When distributions outrun
> the decline, total return is still positive. Erosion alone doesn't prove you lost money.

**[CLOSE — actionable]**
> So don't read the yield. Read the total return, and the nineteen-a-one notice that says
> how much of your income was actually income.

---

## FACT TABLE

| # | Claim in script | Status | Confidence | Source |
|---|---|---|---|---|
| 1 | $1,000 → $850 value + $100 paid = $950 total; a $50 loss | **Arithmetic** — hypothetical, self-verifying | Certain | Stated on screen as hypothetical |
| 2 | "The Distribution Rate represents a single distribution from the ETF and does not represent its total return." | **Verified** — YieldMax's own product-page disclosure, appears across their ETF pages | High | yieldmaxetfs.com product pages (via search index; see egress note) |
| 3 | MSTY distribution dated 09/02/2026 = **98.90% estimated return of capital, 1.10% income** | **Verified** — issuer-published distribution composition | Medium-High | yieldmaxetfs.com/our-etfs/msty/ (page itself egress-blocked; figure read from search index, corroborated across two independent queries) |
| 4 | TSLY distribution dated 09/02/2026 = 36.23% est. ROC, 63.77% income | **Verified** — same source type. *Not in VO; held as backup anchor* | Medium-High | yieldmaxetfs.com/our-etfs/tsly/ |
| 5 | ROC is not taxed as income; it reduces cost basis, deferring tax to sale | **Verified** | High | Roundhill "ROC Distributions in ETFs"; NEOS Investments ROC explainer |
| 6 | A fund's NAV drops by the distribution amount on the ex-dividend date | **Verified** | High | Roundhill 0DTE covered-call FAQ |
| 7 | Repetitive distributions may significantly erode NAV and trading price over time | **Verified** — YieldMax prospectus risk language | High | Tidal Trust II Forms 485BPOS / 497 (SEC EDGAR) |
| 8 | 19a-1 notices disclose estimated NII / capital gains / ROC split; are **not** tax documents (1099-DIV is) | **Verified** | High | NEOS; Neuberger ETF 19a-1 notices page |
| 9 | Counter-beat: total return can be positive despite NAV decline when distributions exceed erosion | **Verified** | High | Roundhill; covered-call ETF NAV-erosion explainers |

### Estimates vs. prices — handled
No analyst price target, forecast or performance projection appears in the VO. Item 3 is
labelled by the issuer itself as **estimated** ROC, and the script says "disclosed as" to
carry that. Final classification only lands on Form 1099-DIV — stated in the pinned comment.

### Egress note affecting verification confidence
`yieldmaxetfs.com`, `stockanalysis.com`, `sec.gov` and `financecharts.com` are all blocked by
this environment's egress proxy. Items 2, 3, 4 and 7 were confirmed through search-index
snippets of those primary pages rather than by loading the documents. Each was corroborated by
at least two independent queries returning consistent figures. **Before publishing, open the
MSTY product page and re-read the 98.90% figure and its date.** If it has rolled to a newer
distribution, update the VO — the argument survives any ROC figure above ~80%, so the fix is a
number swap, not a rewrite.

---

## SHOT LIST — imagery-first three-layer stack

**BASE** cinematic photographic imagery, graded near-black and desaturated
**MID** motion graphics — counters, bars, the vessel rig
**TOP** hero type + burned-in word-by-word captions, current word highlighted

**HERO SHOT:** a sealed tank feeding a drinking glass through a thin tube. The glass fills —
that reads as income. The tank behind it is draining by exactly the same volume. One frame
carries the whole thesis.

**BOOKEND:** the glass. Video opens on a tight macro of it filling, looking like a win. Video
closes on the same glass from the identical camera position, pulled wide to reveal the tube
and the emptied tank behind it.

| # | Beat | BASE imagery | MID graphics | Transition in |
|---|---|---|---|---|
| 1 | "paid you a hundred dollars" | Macro — dark liquid filling a glass, condensation, hard side light | `+$100` slams in, red | open on it |
| 2 | "You can still be poorer" | Whip to the same glass, wider — first hint of the tube | `TOTAL VALUE ▼` | whip + motion blur |
| 3 | "Start with a thousand" | Machined metal block on dark steel, cold light | `$1,000` counts up from 0 | match-cut, glass→block |
| 4 | "the fund pays you a hundred" | Same block, a slice cut away and slid aside | `$100` peels off the counter | punch-in 1.2x |
| 5 | "worth eight hundred and fifty" | The block visibly shorter, machined down, swarf falling | counter drops `$1,000 → $850` | speed ramp |
| 6 | **"is nine hundred and fifty"** | Two columns on a dark plinth, camera pushing between them | Bars draw themselves: `850` + `100`; ghost line at `1,000`; the stack **stops short of the line** and the line flares red | camera pushes THROUGH the gap |
| 7 | "You lost fifty dollars" | Debris settling on black | `−$50` impact frame, 1-frame white flash + shake | hard landing |
| 8 | "distribution rate" vs "total return" | Split frame — left, a cash tray; right, a balance scale | Two gauges, left pinned high, right below zero | type-as-mask wipe |
| 9 | "YieldMax says it in its own disclosure" | Macro — dark printed page, shallow focus, one line raking under a light sweep | Name-tag: plain text `YIELDMAX — FUND DISCLOSURE`. Pull-quote sets in red underline | roll transition |
| 10 | **"almost ninety-nine percent return of capital"** | **HERO** — the tank draining into the glass through the tube, slow-mo | Ratio bar fills to `98.9%` / `1.1%`; name-tag `MSTY · DIST. 09/02/2026` | slow push-in, ramp |
| 11 | "Most of that money was already yours" | The tank now near-empty, the glass full | `RETURN OF CAPITAL` letters arrive individually, overshoot, settle | light sweep |
| 12 | "isn't taxed as income" | A stamp striking dark paper, ink spreading | `COST BASIS ▼` | glitch cut |
| 13 | "the bill waits for you at the sale" | A dated envelope in a drawer sliding shut, frost creeping | `DEFERRED — NOT ERASED` | whip pan |
| 14 | "a falling price isn't automatically a loss" | The same two-column plinth, re-lit | Bars redraw — distributions now **overtop** the ghost line in white | match-cut to shot 6 setup |
| 15 | "Erosion alone doesn't prove you lost money" | Wide, cold, static-ish — the one near-rest frame in the video | `NAV ▼ ≠ LOSS` | slow reveal |
| 16 | "Read the total return, and the 19a-1 notice" | **BOOKEND** — the glass, identical camera position to shot 1, pulled wide: tube, empty tank | `TOTAL RETURN` / `FORM 19a-1` | pull-back |

**Match-cut chain:** glass → metal block → column bars → ratio bar → glass.
**Impact-frame words:** `$950`, `−$50`, `RETURN OF CAPITAL`, `NAV ▼ ≠ LOSS`.
**Beat rule:** cut or punch in every 1.2–1.8s. No shot past 2s.

### Name-tags — no logos
House style bans real corporate marks. Every brand reference is **plain heavy condensed text
on a dark plate**: `YIELDMAX — FUND DISCLOSURE`, `MSTY · DIST. 09/02/2026`, `FORM 19a-1`.
No YieldMax logo, no ticker badge, no exchange mark. This also keeps a video that criticises
a named product clear of trademark use.

---

## PACKAGING

**Titles**
1. Paid Every Week… Still Losing Money?
2. Your ETF Paid You $100. You Got Poorer.
3. The Yield Is Real. The Return Isn't.

**Description**
> A fund can pay you every week and still leave you down. Distribution rate and total
> return are two different numbers, and only one of them is your result. We walk a
> hypothetical $1,000 through a year — $100 paid, $850 left, $950 total — and then look
> at what YieldMax discloses is actually inside those payments.
>
> Educational only. Not financial advice.

**Hashtags:** #etf #dividendinvesting #yieldmax #totalreturn #investing

**Pinned comment**
> The 19a-1 notice is an estimate, not a tax document — the final split lands on your
> 1099-DIV. Worth checking both. And the reverse case is real: if distributions outrun the
> price decline, total return can be positive even while NAV falls.

---

## COMPLIANCE
On-screen card, 0:00–0:04, small but legible: **"Educational only. Not financial advice."**
No ticker is presented as a recommendation. The hypothetical is labelled on screen as
`HYPOTHETICAL` the first time the $1,000 appears.
