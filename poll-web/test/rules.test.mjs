// Security-rule tests against the Firestore emulator (npm test).
import { test, before, after, beforeEach } from "node:test";
import { readFileSync } from "node:fs";
import { initializeTestEnvironment, assertSucceeds, assertFails } from "@firebase/rules-unit-testing";
import { doc, setDoc, getDoc, updateDoc, deleteDoc, collection, query, where, getCountFromServer, serverTimestamp } from "firebase/firestore";

let env;
const ADMIN = { email: "admin@example.com", email_verified: true };
const poll = (over = {}) => ({ question: "Which title?", context: "", options: [{ id: "o1", label: "A" }, { id: "o2", label: "B" }], optionIds: ["o1", "o2"], status: "open", createdAt: new Date(), ...over });

before(async () => {
  env = await initializeTestEnvironment({ projectId: "demo-meticulous-poll", firestore: { rules: readFileSync("firestore.rules", "utf8"), host: "127.0.0.1", port: 8080 } });
});
after(async () => { await env.cleanup(); });
beforeEach(async () => {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async (ctx) => {
    await setDoc(doc(ctx.firestore(), "polls/p1"), poll());
    await setDoc(doc(ctx.firestore(), "polls/closed1"), poll({ status: "closed" }));
  });
});

const anon = (uid = "voter1") => env.authenticatedContext(uid, { firebase: { sign_in_provider: "anonymous" } }).firestore();
const admin = () => env.authenticatedContext("adminuid", ADMIN).firestore();

test("anyone can read polls, signed out included", async () => {
  await assertSucceeds(getDoc(doc(env.unauthenticatedContext().firestore(), "polls/p1")));
});

test("a voter cannot create, edit or delete polls", async () => {
  await assertFails(setDoc(doc(anon(), "polls/p2"), poll()));
  await assertFails(updateDoc(doc(anon(), "polls/p1"), { status: "closed" }));
  await assertFails(deleteDoc(doc(anon(), "polls/p1")));
});

test("an unverified email matching the admin address is not admin", async () => {
  const fake = env.authenticatedContext("x", { email: "admin@example.com", email_verified: false }).firestore();
  await assertFails(setDoc(doc(fake, "polls/p2"), poll()));
});

test("the admin can create, close and delete a valid poll", async () => {
  await assertSucceeds(setDoc(doc(admin(), "polls/p2"), poll()));
  await assertSucceeds(updateDoc(doc(admin(), "polls/p2"), { status: "closed" }));
  await assertSucceeds(deleteDoc(doc(admin(), "polls/p2")));
});

test("even the admin cannot save a malformed poll", async () => {
  await assertFails(setDoc(doc(admin(), "polls/p3"), poll({ options: [{ id: "o1", label: "only one" }], optionIds: ["o1"] })));
  await assertFails(setDoc(doc(admin(), "polls/p3"), poll({ status: "maybe" })));
  await assertFails(setDoc(doc(admin(), "polls/p3"), { ...poll(), extra: true }));
});

test("a voter can cast and change their own vote", async () => {
  const db = anon("v1");
  await assertSucceeds(setDoc(doc(db, "polls/p1/votes/v1"), { option: "o1", at: serverTimestamp() }));
  await assertSucceeds(setDoc(doc(db, "polls/p1/votes/v1"), { option: "o2", at: serverTimestamp() }));
});

test("a voter cannot vote as someone else (no ballot stuffing)", async () => {
  await assertFails(setDoc(doc(anon("v1"), "polls/p1/votes/v2"), { option: "o1", at: serverTimestamp() }));
});

test("signed-out visitors cannot vote", async () => {
  await assertFails(setDoc(doc(env.unauthenticatedContext().firestore(), "polls/p1/votes/v1"), { option: "o1", at: serverTimestamp() }));
});

test("votes must name a real option, a server time, and nothing else", async () => {
  const db = anon("v1");
  await assertFails(setDoc(doc(db, "polls/p1/votes/v1"), { option: "o9", at: serverTimestamp() }));
  await assertFails(setDoc(doc(db, "polls/p1/votes/v1"), { option: "o1", at: new Date(0) }));
  await assertFails(setDoc(doc(db, "polls/p1/votes/v1"), { option: "o1", at: serverTimestamp(), weight: 100 }));
});

test("nobody can vote on a closed poll", async () => {
  await assertFails(setDoc(doc(anon("v1"), "polls/closed1/votes/v1"), { option: "o1", at: serverTimestamp() }));
});

test("a voter can remove their own vote but not someone else's", async () => {
  await env.withSecurityRulesDisabled(async (ctx) => {
    await setDoc(doc(ctx.firestore(), "polls/p1/votes/v1"), { option: "o1", at: new Date() });
    await setDoc(doc(ctx.firestore(), "polls/p1/votes/v2"), { option: "o1", at: new Date() });
  });
  await assertSucceeds(deleteDoc(doc(anon("v1"), "polls/p1/votes/v1")));
  await assertFails(deleteDoc(doc(anon("v1"), "polls/p1/votes/v2")));
  await assertSucceeds(deleteDoc(doc(admin(), "polls/p1/votes/v2")));
});

test("anyone can count votes, and the count is right", async () => {
  await env.withSecurityRulesDisabled(async (ctx) => {
    for (const [id, o] of [["a", "o1"], ["b", "o1"], ["c", "o2"]]) await setDoc(doc(ctx.firestore(), "polls/p1/votes/" + id), { option: o, at: new Date() });
  });
  const db = env.unauthenticatedContext().firestore();
  const snap = await assertSucceeds(getCountFromServer(query(collection(db, "polls/p1/votes"), where("option", "==", "o1"))));
  if (snap.data().count !== 2) throw new Error("expected 2 votes for o1, got " + snap.data().count);
});
