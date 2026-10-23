# Meticulous Poll — public voting site

A public poll site for The Meticulous Investor. Anyone with the link can vote with no sign-up.
You manage polls from `/admin` by signing in with Google. It runs on Firebase's free Spark plan
and can be added to a phone's home screen like an app.

## What's tested

- `npm test` runs 12 security-rule tests against the Firestore emulator. It proves votes can't be
  cast as someone else, on closed polls, for options that don't exist, or while signed out, and
  that only the admin account can create, change or delete polls.
- `test/e2e.mjs` runs the voter journey in a real browser against the emulators: open link, vote,
  see results, change vote, reload.

Both pass. The one thing not tested here is the Google sign-in popup on `/admin`, because it needs
your real Google account. You'll confirm it in step 8 below.

## One-time setup (about 15 minutes, on your computer)

You need a free Google account and [Node.js 20+](https://nodejs.org).

1. **Create a project** at [console.firebase.google.com](https://console.firebase.google.com):
   *Add project*, give it a name (e.g. `meticulous-poll`), and skip Google Analytics. It starts on the
   free Spark plan with no card needed.
2. **Register the web app:** Project settings → *Your apps* → the `</>` icon → any nickname →
   *Register*. Copy the `firebaseConfig` values into `poll-web/src/firebase-config.js`. They are public
   identifiers, not secrets.
3. **Turn on sign-in:** Build → Authentication → *Get started* → Sign-in method → enable
   **Anonymous** and **Google**.
4. **Create the database:** Build → Firestore Database → *Create database* → **Production mode** →
   a US region (e.g. `nam5`).
5. **Get the code ready:**
   ```
   git clone <this repo> && cd helloabyss/poll-web
   npm install
   ```
6. **Connect the CLI to your project:**
   ```
   npx firebase login
   npx firebase use --add        # pick the project from step 1
   ```
7. **Deploy**, with the Google account that should manage polls:
   ```
   ADMIN_EMAIL=you@gmail.com npm run deploy
   ```
   Your address goes only into the generated `firestore.rules`, which git ignores, so it never
   lands in the repo.
8. **Make your first poll:** open `https://<project-id>.web.app/admin`, sign in with Google, create a
   poll and press **Copy link**. Put the link in your video description, pinned comment or community
   post.

After changing anything: `ADMIN_EMAIL=you@gmail.com npm run deploy` again.

## Free-plan limits (Spark)

| Resource | Free allowance | What it means here |
|---|---|---|
| Firestore reads | 50,000 / day | About 12 reads per voter, so several thousand voters a day |
| Firestore writes | 20,000 / day | One write per vote or vote change |
| Hosting transfer | 10 GB / month | A first visit downloads about 170 KB, so tens of thousands of first-time voters a month; repeat visits come from the phone's cache |

Check current limits on [Firebase pricing](https://firebase.google.com/pricing) before a big launch.
If a poll goes viral, the free plan stops serving for the rest of the day rather than charging you.
Upgrading to Blaze (pay as you go) removes that ceiling.

## Limits to know

- **One vote per browser, not per human.** Voting uses an invisible anonymous account per browser.
  The rules stop anyone voting twice from the same account or scripting votes as other people, but
  someone determined can vote again from a private window. That's fine for picking titles. For
  anything higher-stakes, enable Firebase App Check (reCAPTCHA) or require Google sign-in to vote.
- **Results show after voting.** Voters see results only after they vote, so early results don't
  sway later votes. Once a poll closes, everyone sees the final results.
- **No AI panel.** The five-voter Claude panel stays in the claude.ai Poll Booth. Running it from a
  public site would need a server holding a paid Claude API key.

## Developing locally

```
npm run dev        # builds, then serves the site against the emulators at http://127.0.0.1:5000
npm test           # rule tests
```
On `localhost` the app talks to the emulators under a demo project and never touches real data.
