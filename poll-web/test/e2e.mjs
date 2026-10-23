// Voter journey against the emulators: open a poll link, vote, see results, change vote.
import { readFileSync } from "node:fs";
import { initializeTestEnvironment } from "@firebase/rules-unit-testing";
import { doc, setDoc } from "firebase/firestore";
const { chromium } = await import("/opt/node22/lib/node_modules/playwright/index.mjs");

const env = await initializeTestEnvironment({ projectId: "demo-meticulous-poll", firestore: { rules: readFileSync("firestore.rules", "utf8"), host: "127.0.0.1", port: 8080 } });
await env.clearFirestore();
await env.withSecurityRulesDisabled(async (ctx) => {
  const db = ctx.firestore();
  await setDoc(doc(db, "polls/dca-title"), {
    question: "Which title should the NVDA vs QQQ video use?", context: "6-minute explainer: $500 a month into Nvidia and QQQ for 10 years.",
    options: [{ id: "o1", label: "Dollar Cost Averaging NVDA vs QQQ: $500 a Month for 10 Years" }, { id: "o2", label: "$500 a Month Into Nvidia and QQQ for 10 Years: The Real Math (and the Catch)" }, { id: "o3", label: "Dollar Cost Averaging Nvidia and QQQ: Real 10-Year Returns (and the Catch)" }],
    optionIds: ["o1", "o2", "o3"], status: "open", createdAt: new Date() });
  for (const [id, o] of [["seed1", "o2"], ["seed2", "o2"], ["seed3", "o3"]]) await setDoc(doc(db, "polls/dca-title/votes/" + id), { option: o, at: new Date() });
});

const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await b.newPage({ viewport: { width: 420, height: 900 } });
const errors = []; page.on("pageerror", (e) => errors.push(e.message));
const check = (c, m) => { if (!c) throw new Error("FAIL: " + m); console.log("ok - " + m); };

await page.goto("http://127.0.0.1:5000/?p=dca-title");
await page.waitForSelector(".opt:not([disabled])", { timeout: 20000 });
check(await page.locator(".opt").count() === 3, "poll loads with 3 options");
check(await page.locator(".results").count() === 0, "results stay hidden before voting");
await page.locator(".opt").nth(1).click();
await page.waitForSelector(".results .row", { timeout: 20000 });
await page.waitForFunction(() => document.querySelector(".results .row.lead .num small")?.textContent === "3 votes", null, { timeout: 20000 });
check(true, "after voting, results show and the leader has 3 votes (2 seeded + mine)");
check(await page.locator('.opt[aria-pressed="true"] .mine').textContent() === "Your vote", "my option is marked 'Your vote'");
await page.screenshot({ path: "/tmp/claude-0/-home-user-helloabyss/f2a025c9-1076-5048-a768-d12233befd5a/scratchpad/poll-web-voted.png" });

await page.locator(".opt").nth(2).click();
await page.waitForFunction(() => [...document.querySelectorAll(".results .row")].some(r => r.textContent.includes("Real 10-Year") && r.querySelector(".num small").textContent === "2 votes"), null, { timeout: 20000 });
check(true, "changing my vote moves it (option C now 2 votes, no double count)");

await page.reload();
await page.waitForSelector('.opt[aria-pressed="true"]', { timeout: 20000 });
check((await page.locator('.opt[aria-pressed="true"] .lbl').textContent()).includes("Real 10-Year"), "my vote is remembered after reload");

await page.goto("http://127.0.0.1:5000/");
await page.waitForSelector(".plist a", { timeout: 20000 });
check(await page.locator(".plist a").count() === 1, "home page lists the open poll");
check(errors.length === 0, "no page errors" + (errors.length ? ": " + errors.join(" | ") : ""));
await b.close(); await env.cleanup();
