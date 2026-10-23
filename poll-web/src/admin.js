import { GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from "firebase/auth";
import { doc, collection, query, orderBy, onSnapshot, setDoc, updateDoc, deleteDoc, getDocs, writeBatch, serverTimestamp } from "firebase/firestore";
import { auth, db, $, el, CONFIGURED, countVotes, friendly } from "./shared.js";

const S = { user: null, polls: [], counts: {}, armed: null };
let unsub = null;

function slug(q) {
  const base = q.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "poll";
  const r = crypto.getRandomValues(new Uint8Array(3));
  return base + "-" + Array.from(r, (b) => (b % 36).toString(36)).join("");
}

function status(t, err) { const s = $("#formStatus"); s.textContent = t || ""; s.classList.toggle("err", !!err); }
function rowStatus(t) { const s = $("#listStatus"); s.textContent = t || ""; }

function renderAuth() {
  const box = $("#auth"); box.replaceChildren();
  if (S.user) {
    box.append(el("span", "who", S.user.email || "Signed in"));
    const b = el("button", "btn ghost", "Sign out"); b.type = "button"; b.onclick = () => signOut(auth); box.append(b);
  } else {
    const b = el("button", "btn", "Sign in with Google"); b.type = "button";
    b.onclick = async () => { try { await signInWithPopup(auth, new GoogleAuthProvider()); } catch (e) { rowStatus("Sign-in didn't finish. Try again."); } };
    box.append(b);
  }
  $("#panel").hidden = !S.user;
}

function renderList() {
  const ul = $("#adminList"); ul.replaceChildren();
  if (!S.polls.length) { ul.append(el("li", "empty", "No polls yet. Create one above.")); return; }
  for (const p of S.polls) {
    const li = el("li", "arow");
    const info = el("div", "ainfo");
    const c = S.counts[p.id];
    info.append(el("span", "q", p.question), el("span", "meta", `${p.status === "closed" ? "Closed" : "Open"} · ${c ? c.total + " votes" : "…"}`));
    const acts = el("div", "aacts");
    const link = new URL("./?p=" + encodeURIComponent(p.id), location.href.replace(/admin(\.html)?$/, "")).href;
    const cp = el("button", "btn ghost", "Copy link"); cp.type = "button";
    cp.onclick = async () => { try { await navigator.clipboard.writeText(link); rowStatus("Link copied."); } catch (e) { rowStatus(link); } };
    const tg = el("button", "btn ghost", p.status === "closed" ? "Reopen" : "Close"); tg.type = "button";
    tg.onclick = async () => { try { await updateDoc(doc(db, "polls", p.id), { status: p.status === "closed" ? "open" : "closed" }); } catch (e) { rowStatus(friendly(e)); } };
    const del = el("button", "btn danger", S.armed === p.id ? "Confirm delete" : "Delete"); del.type = "button";
    del.onclick = () => (S.armed === p.id ? removePoll(p) : ((S.armed = p.id), renderList()));
    acts.append(cp, tg, del);
    if (S.armed === p.id) { const k = el("button", "btn ghost", "Keep"); k.type = "button"; k.onclick = () => { S.armed = null; renderList(); }; acts.append(k); }
    li.append(info, acts); ul.append(li);
  }
}

async function removePoll(p) {
  S.armed = null; rowStatus("Deleting…");
  try {
    const votes = await getDocs(collection(db, "polls", p.id, "votes"));
    for (let i = 0; i < votes.docs.length; i += 450) {
      const b = writeBatch(db); votes.docs.slice(i, i + 450).forEach((d) => b.delete(d.ref)); await b.commit();
    }
    await deleteDoc(doc(db, "polls", p.id)); rowStatus("Deleted.");
  } catch (e) { rowStatus(e.code === "permission-denied" ? "This account can't manage polls." : friendly(e)); }
}

async function createPoll() {
  const q = $("#fQ").value.trim(), ctx = $("#fCtx").value.trim();
  const labels = [...new Set($("#fOpts").value.split("\n").map((s) => s.trim()).filter(Boolean))];
  if (!q) return status("Add a question.", true);
  if (q.length > 160) return status("Keep the question under 160 characters.", true);
  if (labels.length < 2 || labels.length > 8) return status("Add between 2 and 8 different options, one per line.", true);
  const options = labels.map((label, i) => ({ id: "o" + (i + 1), label: label.slice(0, 200) }));
  const id = slug(q);
  $("#createBtn").disabled = true; status("Creating…");
  try {
    await setDoc(doc(db, "polls", id), { question: q, context: ctx.slice(0, 400), options, optionIds: options.map((o) => o.id), status: "open", createdAt: serverTimestamp() });
    $("#fQ").value = ""; $("#fCtx").value = ""; $("#fOpts").value = "";
    status("Created. Copy its link from the list below.");
  } catch (e) { status(e.code === "permission-denied" ? "This account can't create polls. Sign in with the admin Google account." : friendly(e), true); }
  finally { $("#createBtn").disabled = false; }
}

$("#createBtn").onclick = createPoll;
if (!CONFIGURED) { $("#auth").replaceChildren(el("p", "empty", "This site isn't connected to its database yet. See SETUP.md.")); }
else onAuthStateChanged(auth, (user) => {
  S.user = user && !user.isAnonymous ? user : null;
  renderAuth();
  if (unsub) { unsub(); unsub = null; }
  if (!S.user) return;
  unsub = onSnapshot(query(collection(db, "polls"), orderBy("createdAt", "desc")), async (snap) => {
    S.polls = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    renderList();
    await Promise.all(S.polls.map(async (p) => { try { S.counts[p.id] = await countVotes(p.id, p.options); } catch (e) {} }));
    renderList();
  }, (e) => rowStatus(friendly(e)));
});
