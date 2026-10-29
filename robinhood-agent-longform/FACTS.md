# Fact base — Robinhood agentic trading

**Verified 2026-10-21 by WebSearch corroboration across independent outlets.**

**A limit you must read before trusting any row.** No primary source could be opened this
session: the agent proxy returns `connect_rejected` (403 on CONNECT) for every external
host, so `robinhood.com/us/en/support/articles/trading-with-your-agent/` and the
`sec.gov` Form 10-Q — both of which appeared in results — could **not** be read directly.
Every row below is corroborated secondary reporting. Nothing here is CONFIRMED to the
standard of a primary document.

| # | Claim | Detail | Confidence |
|---|---|---|---|
| 1 | Feature exists | Robinhood lets AI agents place trades for customers; launched beta, US | **HIGH** — TechCrunch, Yahoo Finance, CoinDesk, Finovate, KuCoin all report it |
| 2 | Setup is three steps | Name the agent → open a dedicated agentic trading account → connect an AI model | **HIGH** — consistent across setup write-ups |
| 3 | External agents use MCP | Third-party agents connect via Robinhood's Trading MCP server | **HIGH** — multiple sources |
| 4 | The dedicated account is the boundary | An agent can **read all** your Robinhood accounts but can **only place orders in the dedicated agentic account** | **HIGH** — stated consistently; this is the core safety model |
| 5 | Trade approvals setting | ON = the agent proposes, you place the order yourself in the app | **HIGH** |
| 6 | Approvals still rolling out | Robinhood support says trade approvals are still rolling out for MCP accounts; not all customers have access | **MEDIUM** — attributed to Robinhood support, not read directly |
| 7 | **Default state is disputed** | One source says approvals are **off by default** for external agents; another says confirmation is optional. **Sources conflict** | **DISPUTED — do not assert a default on screen** |
| 8 | Robinhood disclaims supervision | Customers assume all risk; Robinhood "does not control, supervise, monitor, recommend or audit" third-party agents | **HIGH** — reported as Robinhood's own wording |
| 9 | Asset scope | Beta launched stock-only; later sources list long equities, options and supported crypto | **MEDIUM** — sources describe different points in the rollout |
| 10 | Margin | Margin borrowing **not currently enabled** for agentic accounts | **MEDIUM** — single clear source |

## Claims from earlier repo material that did NOT survive re-checking

The Higgsfield narration drafts in this repo's history asserted several things about
Robinhood agentic trading. **They are not carried into this script:**

| Earlier claim | Status now |
|---|---|
| "Loops" — a named feature that places/modifies/cancels trades while you sleep | **NOT FOUND.** No result mentions Loops. Unsupported |
| 4× intraday buying power for agentic accounts | **CONTRADICTED.** Margin borrowing reported as not currently enabled |
| "Trade approvals ON by default for Robinhood Agents, OFF by default for MCP accounts" | **DISPUTED** (row 7). Stated as a conflict on screen, never as a fact |

A tutorial that tells people to switch on automated trading is the worst possible place
to carry an unverified leverage figure. These were dropped deliberately.

## Unusable / out of scope

- Any claim about returns, performance or profitability of agent trading — none found, none scripted.
- Any instruction that depends on a UI element I could not see. The video recreates
  interface *concepts* described in reporting, and says so on screen.
