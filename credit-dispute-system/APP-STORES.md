# Publishing to the App Store and Google Play

The phone apps are in `mobile/`. They open your live website inside a native app and add three
phone-only features: **camera capture** of documents, **deadline reminders** as notifications, and an
icon on the home screen. Because they load the website, **every website update reaches the apps
instantly**, with no app-store resubmission needed (except for changes to the native parts).

**Do [DEPLOY.md](DEPLOY.md) first.** The apps need the live website address.

## 0. Before you start

| Need | Cost | Notes |
|---|---|---|
| An LLC (or other company) | varies | Enroll in both stores **as an organization**, not an individual. Apps handling financial and identity data get extra review. |
| D-U-N-S number | free | Apple requires it for organizations. Request it through Apple's enrollment page; it can take a week or two. |
| Apple Developer Program | $99 / year | developer.apple.com/programs |
| Google Play Console | $25 once | play.google.com/console |
| A Mac with Xcode | – | Needed to upload the iPhone app. No Mac? Use a cloud Mac service (e.g. MacinCloud), or a build service such as Codemagic or Ionic Appflow. |
| Privacy policy URL | – | `https://app.yourbrand.com/privacy` (built in; have your lawyer review it) |

## 1. Point the apps at your website

On any computer with Node.js, in `credit-dispute-system/mobile`:
```
npm ci
node configure.js https://app.yourbrand.com com.yourbrand.disputes
npx cap sync
```
The app ID (`com.yourbrand.disputes`) is permanent once published. Use your own domain reversed.

## 2. Android → Google Play

**Test build (no setup):** every push to this branch builds a test APK on GitHub (repo → **Actions →
Android app** → latest run → **test-apk**). Download it to an Android phone and open it to install.

**Store build:**
1. Create an upload key once, on a computer with Java:
   `keytool -genkey -v -keystore release.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload`
   **Back up `release.jks` and its passwords.** Losing them is painful to recover from.
2. In GitHub: repo → **Settings → Secrets and variables → Actions**, add:
   `ANDROID_KEYSTORE_BASE64` (the output of `base64 -w0 release.jks`), `ANDROID_KEYSTORE_PASSWORD`,
   `ANDROID_KEY_ALIAS` (`upload`), `ANDROID_KEY_PASSWORD`.
3. Push or click **Run workflow**. The run now also produces **google-play-bundle** (an `.aab` file).
4. In Play Console: **Create app**, then fill in the store listing, **Data safety** (see section 4) and
   **Content rating**, and declare it a **financial services** app if asked. Upload the `.aab` to
   **Internal testing** first, try it, then promote to **Production**.

## 3. iPhone → App Store

1. On the Mac: `cd mobile && npm ci && npx cap sync ios && npx cap open ios` (opens Xcode).
2. In Xcode: select the **App** target → **Signing & Capabilities** → choose your team. Set the
   version and build numbers.
3. **Product → Archive**, then **Distribute App → App Store Connect → Upload**.
4. In App Store Connect: create the app with the same bundle ID, fill in the listing, privacy
   "nutrition label" (section 4), screenshots (6.7" and 6.5" iPhone), and **App Review notes**.

**App Review notes (copy, then fill in the brackets):**
> This app helps US consumers find errors in their credit reports and prepare dispute letters under
> the Fair Credit Reporting Act, which they sign and mail themselves. Native features: camera capture
> of identity and supporting documents, and local notifications when a credit bureau's legal response
> deadline passes. Demo account: [email] / [password], with a sample case already filled in.
> Purchases are completed on our website, not in the app.

**Availability:** set the apps to the **United States only**. The legal content is US-specific.

## 4. Privacy answers for both stores

Collected and **linked to the user**, not used for tracking, not sold or shared with third parties
for advertising:
- Contact info: name, email, physical address, phone (optional)
- Identifiers: user ID
- Sensitive / financial info: date of birth, last 4 digits of SSN, credit account details the user enters
- Photos and documents the user uploads (ID, bills, statements)

Encrypted in transit (HTTPS) and at rest. Users can delete their account and all data in the app
(**My cases → Delete my account and data**), which both stores require.

## 5. Payments in the apps

By default (`NATIVE_PAYMENT_MODE=none`) the apps **never show a price or a buy button**. When letters
are ready, they tell the user to finish on the website. That's the safest choice for review on both
stores. Since 2025, US court rulings let apps link out to website checkout without Apple's commission.
If you want a direct "Complete purchase" button that opens the browser, set `NATIVE_PAYMENT_MODE=link`
in Render, **after checking both stores' current rules**: Apple is still appealing, and Google's
rules differ.

## 6. If a store rejects the app

- **Apple 4.2 "minimum functionality"** (the "it's just a website" rejection): reply in Resolution
  Center pointing to the camera document capture and deadline notifications. If it's still rejected,
  the next step is adding Face ID login and an offline view of the user's deadline list. Ask me for both.
- **Apple 3.1.1 (in-app purchase)**: confirm `NATIVE_PAYMENT_MODE=none`, and say purchases happen on the web.
- **Google "Financial services" / "Deceptive behavior"**: point to the no-guarantee wording, the
  rights statement, and that the app never disputes information the user says is accurate.
