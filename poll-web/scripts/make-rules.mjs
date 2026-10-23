// Writes firestore.rules from the template with your admin email filled in.
import { readFileSync, writeFileSync } from "node:fs";
const email = (process.env.ADMIN_EMAIL || "").trim();
if (!/^[^@\s"]+@[^@\s"]+\.[^@\s"]+$/.test(email)) {
  console.error('Set ADMIN_EMAIL to the Google account that manages polls, e.g.\n  ADMIN_EMAIL=you@gmail.com npm run rules');
  process.exit(1);
}
writeFileSync("firestore.rules", readFileSync("firestore.rules.template", "utf8").replace("__ADMIN_EMAIL__", email));
console.log(`firestore.rules written for ${email}`);
