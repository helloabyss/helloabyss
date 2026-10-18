# Turo fleet tracker

Spreadsheet for running a Turo fleet toward a $300k/yr net-profit goal. Not a video — kept
here as a working tool. Educational only, not financial, tax or legal advice.

- `Turo_Fleet_Tracker.xlsx` — the tracker. Open the **How to use** tab first. Yellow cells are
  inputs; everything else is a formula. Delete rows marked `EXAMPLE – delete` before use.
- `build_tracker.py` — regenerates the workbook from scratch (`python3 build_tracker.py`,
  needs `openpyxl`). Formulas have no cached values until opened in Excel/Sheets or recalculated.

| Tab | What it does |
|---|---|
| Dashboard | 12-month P&L up to the Report month, run-rate, cars needed for goal, reserve |
| Assumptions | Goal, start month, Report month, host share, targets |
| Fleet | One row per car + fixed monthly costs |
| Trips | Trip log from the Turo earnings export |
| Expenses | Variable costs (car ID or `FLEET`) |
| Car Scorecard | Per-car net, utilization, payback, sell-review flag |
| Buy Box | BUY/PASS test for a candidate car |

Host-share default (70/80/90% US earnings plans) is from Turo's help centre as of Jan 2026 —
re-check, Turo changes terms often.
