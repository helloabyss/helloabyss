import { signInAnonymously, onAuthStateChanged } from "firebase/auth";
import { doc, getDoc, setDoc, deleteDoc, onSnapshot, collection, query, orderBy, limit, getDocs, serverTimestamp } from "firebase/firestore";
import { auth, db, $, el, KEYS, CONFIGURED, countVotes, resultRows, friendly } from "./shared.js";

const pid = new URLSearchParams(location.search).get("p");
const S = { uid: null, poll: null, mine: null, counts: null, total: 0, busy: false, msg: "" };

function setMsg(text, err) { S.msg = text || ""; const m = $("#msg"); if (m) { m.textContent = S.msg; m.classList.toggle("err", !!err); } }

async function refreshCounts() {
  if (!S.poll) return;
  try { const r = await countVotes(pid, S.poll.options); S.counts = r.counts; S.total = r.total; render(); }
  catch (e) { /* keep last counts; a later refresh recovers */ }
}

function render() {
  const main = $("#main"); main.replaceChildren();
  const p = S.poll;
  if (!p) { main.append(el("p", "empty", "This poll doesn't exist or was removed.")); return; }
  const open = p.status !== "closed";
  const card = el("article", "card");
  const eb = el("div", "eyebrow"); eb.append(el("span", "chip " + (open ? "open" : "closed"), open ? "Open" : "Closed"));
  if (S.counts) eb.append(el("span", null, `${S.total} vote${S.total === 1 ? "" : "s"}`));
  card.append(eb, el("h1", null, p.question));
  if (p.context) card.append(el("p", "ctx", p.context));

  const showResults = !!S.mine || !open;
  const ballot = el("div", "ballot"); ballot.setAttribute("role", "group"); ballot.setAttribute("aria-label", "Your vote");
  p.options.forEach((o, i) => {
    const b = el("button", "opt"); b.type = "button";
    b.setAttribute("aria-pressed", String(S.mine === o.id));
    b.disabled = !open || !S.uid || S.busy;
    b.append(el("span", "key", KEYS[i]), el("span", "lbl", o.label), el("span", "mine", S.mine === o.id ? "Your vote" : ""));
    b.onclick = () => vote(o.id);
    ballot.append(b);
  });
  card.append(ballot);

  const line = el("div", "voteline");
  if (!S.uid) line.append(el("span", null, "Connecting…"));
  else if (!open) line.append(el("span", null, "Voting has closed. Final results below."));
  else if (S.mine) { line.append(el("span", null, "Thanks for voting. Tap another option to change it.")); const c = el("button", "linkbtn", "Remove my vote"); c.type = "button"; c.onclick = () => vote(null); line.append(c); }
  else line.append(el("span", null, "Pick one. Results appear after you vote."));
  const m = el("span", "status" + (S.msg && /n't|wrong|offline/.test(S.msg) ? " err" : ""), S.msg); m.id = "msg"; line.append(m);
  card.append(line);

  if (showResults) {
    card.append(el("h2", "sec-label", open ? "Live results" : "Final results"));
    card.append(S.counts ? resultRows(p.options, S.counts, S.total) : el("p", "empty", "Loading results…"));
    const rf = el("button", "linkbtn", "Refresh results"); rf.type = "button"; rf.onclick = () => refreshCounts(); card.append(rf);
  }

  const share = el("div", "share");
  const sb = el("button", "btn ghost", "Share this poll"); sb.type = "button";
  sb.onclick = async () => {
    const url = location.href;
    try { if (navigator.share) { await navigator.share({ title: p.question, url }); return; } } catch (e) { return; }
    try { await navigator.clipboard.writeText(url); setMsg("Link copied."); } catch (e) { setMsg(url); }
  };
  share.append(sb, el("a", "linkbtn", "All polls")); share.lastChild.href = "./";
  card.append(share);
  main.append(card);
}

async function vote(optionId) {
  if (!S.uid || S.busy || !S.poll || S.poll.status === "closed" || S.mine === optionId) return;
  const prev = S.mine; S.mine = optionId; S.busy = true; setMsg(""); render();
  try {
    const ref = doc(db, "polls", pid, "votes", S.uid);
    if (optionId) await setDoc(ref, { option: optionId, at: serverTimestamp() });
    else await deleteDoc(ref);
    await refreshCounts();
  } catch (e) { S.mine = prev; setMsg(friendly(e), true); }
  finally { S.busy = false; render(); }
}

async function listPolls() {
  const main = $("#main"); main.replaceChildren(el("p", "empty", "Loading polls…"));
  try {
    const snap = await getDocs(query(collection(db, "polls"), orderBy("createdAt", "desc"), limit(20)));
    const polls = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    main.replaceChildren();
    const open = polls.filter((p) => p.status !== "closed"), closed = polls.filter((p) => p.status === "closed");
    if (!polls.length) { main.append(el("p", "empty", "No polls yet. Check back soon.")); return; }
    for (const [label, list] of [["Open now", open], ["Closed", closed]]) {
      if (!list.length) continue;
      main.append(el("h2", "sec-label", label));
      const ul = el("ul", "plist");
      for (const p of list) {
        const li = el("li"), a = el("a"); a.href = "?p=" + encodeURIComponent(p.id);
        a.append(el("span", "q", p.question), el("span", "meta", `${p.options.length} options`));
        li.append(a); ul.append(li);
      }
      main.append(ul);
    }
  } catch (e) { main.replaceChildren(el("p", "empty", friendly(e))); }
}

function watchPoll() {
  onSnapshot(doc(db, "polls", pid), (snap) => {
    S.poll = snap.exists() ? snap.data() : null;
    render(); if (S.poll) refreshCounts();
  }, (e) => { setMsg(friendly(e), true); });
  // Counts refresh on vote, on returning to the tab (at most every 30s), or on request,
  // never on a timer: timers are what burn through the free tier's daily read quota.
  let last = 0;
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible" && Date.now() - last > 30000 && (S.mine || (S.poll && S.poll.status === "closed"))) { last = Date.now(); refreshCounts(); }
  });
}

if (!CONFIGURED) {
  $("#main").replaceChildren(el("p", "empty", "This site isn't connected to its database yet. See SETUP.md."));
} else {
  onAuthStateChanged(auth, async (user) => {
    if (!user) { try { await signInAnonymously(auth); } catch (e) { setMsg(friendly(e), true); } return; }
    S.uid = user.uid;
    if (pid) {
      try { const mv = await getDoc(doc(db, "polls", pid, "votes", S.uid)); S.mine = mv.exists() ? mv.data().option : null; } catch (e) {}
      render();
    }
  });
  if (pid) watchPoll(); else listPolls();
}

if ("serviceWorker" in navigator) navigator.serviceWorker.register("./sw.js").catch(() => {});
