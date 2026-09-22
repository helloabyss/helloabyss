# The Faceless Channel Playbook — sellable PDF

A finished, sellable 80-page PDF product built from this repo's own production record:
`STYLE-GUIDE.md`, `CLAUDE.md`, and the three video directories. Everything specific in it —
the scrapped renders, the 404 incident, the caption defect, the credit walls, the runtimes —
comes from work that actually happened here. That specificity is the product; there is
nothing in it that a generic "AI video course" could contain.

**Deliverable:** `dist/The-Faceless-Channel-Playbook.pdf` (80pp, US Letter, ~470 KB).

## Layout

```
playbook/
  src/book.html    the entire book — content and design in one file
  src/fonts.css    Oswald / Source Serif 4 / IBM Plex Mono, base64-embedded (SIL OFL)
  build.mjs        renders the HTML to PDF with headless Chromium
  stamp.py         stamps running feet, skipping full-bleed pages
  build.sh         runs both
  dist/            the built PDF
```

## Rebuilding

```bash
npm install playwright-core          # once
pip install pymupdf                  # once
./build.sh
```

Chromium is found at `/opt/pw-browsers/chromium`; override with `CHROMIUM_PATH`.
`build.mjs` warns about any table or code block that overflows its page width.

Why the two steps: Chromium reserves a band at the foot of every sheet when its own
header/footer is enabled, which clips the full-bleed cover and part dividers. So the feet
are stamped afterwards, and skipped on any page whose top-left pixel is dark.

## Before you sell it — change these

All in `src/book.html`, then rebuild:

| What | Where |
|---|---|
| Imprint name (`helloabyss`) | cover, title page, licence, colophon — 5 occurrences |
| Edition and date | cover `.foot`, title page, licence, colophon |
| Contact for team licences | Appendix G |
| Refund promise | Appendix G — delete it if you will not honour it |

## The one editorial decision left to you

The book teaches the *method* of locking a visual identity and uses this channel's identity
as the worked example. It deliberately does **not** hand over this channel's HeyGen style ID
or voice ID — the brief template has `[ID]` placeholders, since buyers use their own
accounts anyway.

If you would rather the product not expose this channel's look at all, the imagery-by-beat
tables in Chapters 3, 4 and 25 are the pages to generalise. The counter-argument, and the
reason it is written this way: a playbook with real shot lists in it is worth paying for,
and one with placeholders is not.

## Pricing and where to sell

Gumroad, Payhip and Lemon Squeezy all handle a single PDF with no setup cost; Lemon Squeezy
and Payhip act as merchant of record, which handles EU/UK VAT for you. Check each one's
current fees before choosing — they change.

On price: this is a specialist operations manual, not a mass-market ebook. Comparable
production playbooks sit in the $29–$79 range. Below about $20 you are competing with free
blog posts; above about $100 buyers expect video and support. The honest constraint is that
**a product's revenue is a function of audience**, and this channel has three videos — so
treat the first months as evidence-gathering, not as the launch.

What lifts conversion on a product like this, in rough order: a sample (the first chapter
plus Appendix C is the natural free extract), the honesty of the sources appendix, and a
visible refund promise.

## Standards the document is held to

It follows this repo's own rules, which is the point:

- Every external claim carries a source and a confidence level (Appendix F), including two
  rows marked **Medium** because YouTube's help centre and blog were unreachable from the
  build environment. They are flagged in the text, not rounded up.
- No income claims anywhere. Chapter 23 is deliberately discouraging about Shorts revenue.
- "Not financial advice" on the title page and in the licence; the market and regulatory
  figures are labelled as worked examples of a method, not current data.
- The FINRA/PDT facts used in the Chapter 25 teardown were re-verified on 22 Sept 2026.

## Re-verify before each new edition

The two Medium rows in Appendix F concern monetization thresholds, which changed twice in
the period the book covers. Check them at YouTube's help centre and update Chapters 1 and 23
before you sell a new edition.
