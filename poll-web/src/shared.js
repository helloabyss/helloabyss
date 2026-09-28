import { initializeApp } from "firebase/app";
import { getAuth, connectAuthEmulator } from "firebase/auth";
import { getFirestore, connectFirestoreEmulator, collection, query, where, getCountFromServer } from "firebase/firestore";
import { firebaseConfig } from "./firebase-config.js";

// On localhost the app talks to the Firebase emulators under a demo project, so nothing
// real is touched while developing or testing.
export const LOCAL = ["localhost", "127.0.0.1"].includes(location.hostname);
export const CONFIGURED = LOCAL || !String(firebaseConfig.projectId).startsWith("REPLACE");

const app = initializeApp(LOCAL
  ? { apiKey: "demo-key", authDomain: "localhost", projectId: "demo-meticulous-poll", appId: "demo" }
  : firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
if (LOCAL) {
  connectAuthEmulator(auth, "http://127.0.0.1:9099", { disableWarnings: true });
  connectFirestoreEmulator(db, "127.0.0.1", 8080);
}

export const $ = (s) => document.querySelector(s);
export function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
}
export const KEYS = "ABCDEFGH";

/** Vote counts per option via server-side count queries (cheap at any audience size). */
export async function countVotes(pollId, options) {
  const votes = collection(db, "polls", pollId, "votes");
  const results = await Promise.all(options.map((o) =>
    getCountFromServer(query(votes, where("option", "==", o.id))).then((s) => s.data().count)));
  const counts = Object.fromEntries(options.map((o, i) => [o.id, results[i]]));
  return { counts, total: results.reduce((a, b) => a + b, 0) };
}

/** Bar rows sorted by votes; the leader gets the accent. */
export function resultRows(options, counts, total) {
  const box = el("div", "results");
  const top = Math.max(0, ...Object.values(counts));
  const order = options.map((o, i) => ({ o, i })).sort((a, b) => counts[b.o.id] - counts[a.o.id] || a.i - b.i);
  for (const { o, i } of order) {
    const v = counts[o.id];
    const row = el("div", "row" + (v > 0 && v === top ? " lead" : ""));
    const body = el("div", "body"), track = el("div", "track"), fill = el("div", "fill");
    fill.style.width = (total ? (100 * v) / total : 0) + "%";
    track.append(fill);
    body.append(el("span", "lbl", o.label), track);
    const num = el("div", "num", total ? Math.round((100 * v) / total) + "%" : "0%");
    num.append(el("small", null, `${v} vote${v === 1 ? "" : "s"}`));
    row.append(el("span", "key", KEYS[i]), body, num);
    box.append(row);
  }
  return box;
}

export function friendly(e) {
  const code = e && e.code;
  if (code === "permission-denied") return "That wasn't allowed. The poll may have closed.";
  if (code === "unavailable") return "You're offline. Check your connection and try again.";
  return "Something went wrong. Try again in a moment.";
}
