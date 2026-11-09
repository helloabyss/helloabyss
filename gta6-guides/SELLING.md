# Selling the Day One Playbook: launch plan

**Product:** *The Day One Playbook*, an unofficial launch guide for GTA VI players (`GUIDE.md`)
**Window:** today (9 Nov) to launch (19 Nov) is **10 days**. Pre-load opens tomorrow.
That's the moment of peak "how do I get ready" searches, so ship within 24 hours.

---

## 1. Why this product, and why it can stand out

- **Everyone else is selling guesses.** A pre-launch guide that labels every claim
  CONFIRMED, REPORTED or RUMOUR stands out from the crowd selling rumour as fact.
- **The real value comes after launch.** A pre-launch edition alone is thin, and buyers
  will see that. It sells because **buyers get every update free** (Edition 1.1 field
  notes, then the Online section). That turns a 10-day product into a living one.
- **Honest weakness:** nearly everything in the pre-launch edition can be found for free,
  spread across outlets. You're selling *curation, the checklist and the updates*, not
  secrets. Price it accordingly.

## 2. Price and where to sell

| Choice | Recommendation | Why |
|---|---|---|
| Launch price | **$4.99**, moving to $7.99 once Edition 1.1 ships | Low enough to buy on impulse. Rising later rewards early buyers. |
| Pay-what-you-want floor | Optional, $3 minimum | Good for goodwill early on |
| Storefront | **Gumroad, Payhip or Lemon Squeezy** | All three handle file delivery, emailing buyers about updates, and VAT/sales tax. |
| Delivery | PDF plus a link to a web version | Update the file and email "Edition 1.1 is live" to the buyer list |
| Refunds | 14 days, no questions asked | Makes it easier to buy and builds trust |

## 3. Legal guardrails (don't skip)

Based on Rockstar's own policy pages and its September 2026 mod guidelines:

- **"Unofficial" goes on the cover, the store page and the video description.**
- **No Rockstar logos, key art, trailer screenshots or the GTA VI wordmark** on the cover,
  thumbnail or store page. Use your own art in the guide's Vice City-at-dusk theme: sunset
  gradient, striped sun, palm silhouettes, neon pink and teal on night purple. The PDF
  cover is original CSS/SVG art, so you can reuse it for thumbnails. Don't imitate the
  official GTA VI logo, its "VI" lettering or its pink-and-orange wordmark style.
- **Use the game's name only to say what the guide is about** ("a guide *for* GTA VI
  players"), never as your product's brand. Don't name the product "GTA 6 Guide".
- **No leaked footage, datamined files or anything taken from pre-release builds.**
- **Footage in your videos:** gameplay footage is generally allowed under Rockstar's video
  policy. Selling a guide is a separate commercial product, so keep game assets *out of
  the product itself*.
- This is **not legal advice**. If the channel grows big, pay for an hour with an IP lawyer.

## 4. YouTube launch sequence (shorts plus one long video)

| Day | Video | Hook (no clickbait) | Call to action |
|---|---|---|---|
| 9 Nov | Short: "GTA VI needs 212 GB. Here's the 10-minute clear-out." | The storage plan | Full checklist in the guide (link in the pinned comment) |
| 10 Nov | Short: "Pre-load is open. Xbox and PS5 open at different times." | Xbox at 12 a.m. GMT, PS5 at local midnight | Same |
| 11 Nov | Short: "Series S owners: read this before the 19th." | ~362 GB usable | Same |
| 13 Nov | **Long video, 8–10 min:** "Everything confirmed about GTA VI's launch, and the rumours to ignore" | The fact sheet, honestly labelled | Guide plus subscribe |
| 15 Nov | Short: "Standard or Ultimate? The honest answer." | Part 3 | Same |
| 17 Nov | Short: "Mute these words before launch." | Spoiler lockdown | Same |
| 19 Nov | Live or short: first-hour impressions | Real gameplay | "Edition 1.1 is coming. Buyers get it free." |
| 20–26 Nov | Daily shorts from real play | Settings, money, side activities | Edition 1.1 launch |

**Description template:**
> The Day One Playbook: an unofficial, fact-checked launch guide for GTA VI players.
> Every claim labelled confirmed, reported or rumour. Free updates after launch. [link]
> Not affiliated with Rockstar Games or Take-Two Interactive.

## 5. Being first

1. **Ship today.** A guide that arrives on 20 November isn't first.
2. **Own the honesty position.** "The only GTA VI guide that tells you what's a rumour."
3. **Build the email list, not just sales.** Every buyer is someone you can tell about
   your next product: a money guide, a collectibles map, then an Online guide when it
   arrives. That list is worth more than the first $5.
4. **Next products to plan now** (built from real play only):
   - Early-game money and economy guide (week 2)
   - Collectibles and hidden spots checklist (weeks 2–4)
   - Online starter guide (when Rockstar announces it)

## 6. Before you hit publish

- [ ] Check the price, pre-load times and edition contents again on Rockstar's site on the
  day you publish
- [ ] Your own cover art, with no Rockstar assets
- [ ] "Unofficial" disclaimer on the cover, the store page and the descriptions
- [ ] The storefront's update-email feature is set up
- [ ] Refund policy written on the store page
- [ ] Note in your diary: write Edition 1.1 between 20 and 26 Nov

---

## 7. Product two: *The First-Timer's Playbook* (`first-timers/`)

A large-print, no-jargon guide for grown-ups who have never played a video game: whether the
game is right for them (ESRB M 17+, with content warnings shown up front), what to buy, setup,
the controller, comfort and accessibility settings, a glossary, and launch-scam safety.

- **Who buys it:** often not the player. It's adult children and grandkids buying it *for* a
  parent, and gift-buyers in the Black Friday and holiday window. Write the store page for them.
- **Price:** $4.99, or **bundle both for $7.99**.
- **Shorts angle:** "My mum has never played a video game. Here's how she's starting GTA VI."
  (Faceless works: show hands on a controller, the TV and the guide's pages.)
- **Honest weakness:** it shouldn't oversell the game to people who'd hate the content. Page 3
  tells them so, and that builds trust for everything else you sell.
- **Update after launch:** confirm the real control layout, subtitle and accessibility options,
  and tutorial length, then replace the hedged lines on pages 7–8.

## Rebuilding the PDFs

```
python3 gta6-guides/day-one/build.py
python3 gta6-guides/first-timers/build.py
```
The layouts live in each `build.py`, and the shared design system is in `design.py`. The build
prints a warning if any page overflows.

---

## 8. Product three: *The Creator Playbook* (`creator/`)

How to make money from GTA VI content: income streams, the YouTube Partner Program bar
(and the reported **1 Feb 2027** doubling), Rockstar's video policy, YouTube's Sept 2026
gaming-violence rules (no graphic violence in the first 7 seconds), products, sponsors, a
faceless workflow and a 90-day plan. **Price: $7.99.** It also works as a lead magnet for other
GTA creators.

**Line-up:** Day One $4.99 · First-Timer's $4.99 · Creator $7.99 · **all three $12.99**.

## 9. Where to host and sell the PDFs

| Platform | Fee on a $4.99 sale (approx.) | Handles sales tax/VAT? | Best for |
|---|---|---|---|
| **Payhip (free plan)** | 5% + card processing (~2.9% + $0.30) ≈ **$0.69** | EU/UK VAT | **Start here.** Cheapest per sale, no monthly fee, bundles and coupons. |
| Gumroad | 10% + $0.50 ≈ **$1.00** | Yes, worldwide (merchant of record) | Zero tax admin. Easiest to set up. |
| Lemon Squeezy | 5% + $0.50 ≈ **$0.75** (+1.5% international) | Yes (merchant of record) | Low fee plus tax handled. More software-oriented. |
| Stan Store | $29/month, 0% per sale | Check current terms | Once you're past roughly $250/month in sales. |
| Ko-fi | 5% on free plan (0% on Gold) | Check current terms | Tips plus a small shop in one place. |

Fees come from comparison sites (Nov 2026). Confirm on each pricing page before signing up.

**Recommendation:** open a **Payhip** store now, list all three PDFs plus the bundle, and put
the store link in your YouTube channel's Links section, every description and a pinned comment.
If you'd rather never think about sales tax, use **Gumroad** and accept the higher fee. Don't
host paid PDFs on Google Drive or Dropbox links: there's no checkout, no buyer list, and links
get shared freely.
