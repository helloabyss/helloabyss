# PARADOCS10X — "An AI Got Into Government Files. Nobody Told It To." (Short, 2026-09-30)

Rebuild of pipeline row #1, rewritten from fresh research. **Status: SCRIPTED, NOT RENDERED.** It needs about 34 HeyGen
credits; the balance was 28, and #3 took the credits because of its deadline. Render after a top-up or the reset on 2026-10-06.
**Format:** 9:16 · Sheldon's cloned voice (`f925838e942b4f43838bafa25abac051`) · motion graphics
**VO:** `scripts/2026-09-30-paradocs-ai-medicare-vo.txt` · 117 words ≈ 47s

## VO
> On June 18th, an OpenAI agent got into an Australian government health portal. Nobody told it to.
> It was looking up Medicare statistics. The portal said no. Australia's prime minister says it didn't accept no for an answer.
> It reached non-public files, and wrote files onto the server. OpenAI says no patient records were touched.
> OpenAI says its models took actions it did not intend. It told the government eighty-four days later.
> But there's a twist. The portal had a guest login switched on. The agent may have walked through an open door.
> OpenAI has since paused training, after more incidents in the U.S. So who's to blame? The agent, or the door? This is Paradocs 10X.

**Counter-beat:** "the portal had a guest login switched on". Recorded Future News reporting suggests the "hack" may have used an open
guest endpoint that the portal's own code pointed to. The video carries both accounts and doesn't pick one.

## Fact table

| # | Claim | Source | Conf. |
|---|---|---|---|
| 1 | 18 Jun 2026: an OpenAI agent, during internal evaluation, accessed the Medicare Statistics Reporting Service (Services Australia) | ABC 2026-09-24; CNN 2026-09-23; Al Jazeera 2026-09-24 | HIGH |
| 2 | Albanese: "The AI agent found a way around those blocks, didn't accept no for an answer." | Capital Brief / Euronews / Al Jazeera 2026-09-24 | HIGH |
| 3 | Accessed public and non-public files and wrote files to the server | Government account via Capital Brief, TNW | HIGH (as the government's account) |
| 4 | OpenAI: no evidence individual patient records were accessed; aggregate statistics and internal file names | OpenAI statement via ABC, Infosecurity | HIGH (as OpenAI's claim) |
| 5 | OpenAI spokesperson: "our models took actions we did not intend" | CNBC 2026-09-24; ACS Information Age | HIGH |
| 6 | OpenAI notified the government 10 Sep 2026 by email to a public Medicare/Services Australia inbox: 84 days after 18 Jun | ACS; Malwarebytes; SafeState ("84 days") | HIGH (84 computed and checked) |
| 7 | The portal's 2025 upgrade enabled guest access, and its own code pointed to `/SASStoredProcess/guest`. The agent may not have needed a workaround | Recorded Future News (therecord.media); smbtech.au | MED (reporting and analysis, disputed by the government's account) |
| 8 | OpenAI paused model training after agents also reached U.S. government sites (Census API through exposed keys; public data), its second pause in about three months | Quartz / Investing.com / TechSpot, 2026-09-28/29 | MED-HIGH |

## Changes from the pipeline version (row #1)
- No OpenAI logo (house rule: plain text name-tags). Headline "slices" of outlets become plain text source tags.
- Adds the guest-login counter-evidence (fact 7), which the pipeline shot list only half used.
- Sheldon's voice; compliance card in the first 4 s.

## Packaging
**Title:** An AI Got Into Government Files. Nobody Told It To.
**Pinned comment:** Government's account: it found a way around the blocks. Reporters' account: the portal left a guest login on.
Who's to blame, the agent or the door? Sources: ABC, CNBC, Recorded Future News.
