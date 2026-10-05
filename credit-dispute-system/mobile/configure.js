// Usage: node configure.js https://app.yourdomain.com com.yourcompany.creditdisputes
// Sets the live website address and the store app ID, then copies settings into the native projects.
const fs = require("fs");
const [url, appId] = process.argv.slice(2);
if (!url || !/^https:\/\//.test(url)) {
  console.error("Give the live https:// address of your website, e.g. node configure.js https://app.example.com com.example.disputes");
  process.exit(1);
}
const cfg = JSON.parse(fs.readFileSync("capacitor.config.json", "utf8"));
cfg.server.url = url.replace(/\/$/, "");
if (appId) cfg.appId = appId;
fs.writeFileSync("capacitor.config.json", JSON.stringify(cfg, null, 2) + "\n");
console.log(`Website: ${cfg.server.url}\nApp ID:  ${cfg.appId}\nNow run: npx cap sync`);
