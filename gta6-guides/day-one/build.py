"""THE DAY ONE PLAYBOOK — designed PDF. Content source of truth: GUIDE.md (keep in sync)."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from design import page, part, scene, render

R = "The Day One Playbook"
OK, REP, RUM = '<span class="pill ok">CONFIRMED</span>', '<span class="pill rep">REPORTED</span>', '<span class="pill rum">RUMOUR</span>'

cover = f"""<section class="page">
{scene(sky="linear-gradient(180deg,#0b031d 0%,#2a0f55 24%,#7a1e8c 42%,#ff2d8a 57%,#ff8a3d 66%,#ffc94d 70%)",
       sun="linear-gradient(180deg,#ffe08a,#ff9d3d 45%,#ff2d8a)",
       sea="repeating-linear-gradient(180deg,#170734 0 3mm,#241050 3mm 4mm)")}
<div style="position:absolute;left:18mm;right:18mm;top:18mm">
  <div class="kicker">Edition 1.0 · Pre-launch · Facts checked 9 Nov 2026</div>
  <h1 class="display" style="font-size:76pt;color:#fff;margin:7mm 0 5mm;text-shadow:0 0 22px rgba(255,45,138,.8),3px 3px 0 #ff2d8a">The<br>Day One<br>Playbook</h1>
  <div style="font-size:14pt;color:#fff;max-width:125mm">An unofficial launch guide for <b>Grand Theft Auto VI</b> players</div>
</div>
<div style="position:absolute;left:0;right:0;bottom:9mm;text-align:center;font-size:7pt;color:#a898cc;letter-spacing:.05em">
  Unofficial. Not made, endorsed or sponsored by Rockstar Games or Take-Two Interactive.</div>
<div style="position:absolute;right:16mm;bottom:22mm;width:44mm;height:44mm;border-radius:50%;background:#140a2bdd;border:2px solid #13d6c3;
     display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#13d6c3;transform:rotate(-8deg)">
  <span style="font-family:Anton;font-size:22pt;line-height:1;color:#fff">FREE</span>
  <span style="font-size:7.5pt;font-weight:800;letter-spacing:.14em">UPDATES<br>AFTER LAUNCH</span></div>
</section>"""

toc = page(f"""
<div class="kicker">Inside</div>
<h2 class="display grad" style="font-size:54pt;margin:3mm 0 8mm">Ten days.<br>One plan.</h2>
<div class="grid" style="grid-template-columns:1.25fr 1fr;gap:10mm">
 <div class="toc">
  <div class="row"><span class="n">01</span><span class="t">The fact sheet<small>Confirmed vs reported vs rumour</small></span><span class="p">04</span></div>
  <div class="row"><span class="n">02</span><span class="t">The storage plan<small>212 GB and what to clear</small></span><span class="p">05</span></div>
  <div class="row"><span class="n">03</span><span class="t">Which edition<small>The honest answer</small></span><span class="p">06</span></div>
  <div class="row"><span class="n">04</span><span class="t">Launch week<small>Day by day</small></span><span class="p">07</span></div>
  <div class="row"><span class="n">05</span><span class="t">Your first session<small>Habits that pay off</small></span><span class="p">08</span></div>
  <div class="row"><span class="n">06</span><span class="t">Spoiler lockdown<small>Mute list included</small></span><span class="p">09</span></div>
  <div class="row"><span class="n">07</span><span class="t">For creators<small>Record it properly</small></span><span class="p">09</span></div>
  <div class="row" style="border:0"><span class="n">08</span><span class="t">Edition 1.1<small>What's coming free</small></span><span class="p">10</span></div>
 </div>
 <div>
  <h3>How to read this guide</h3>
  <p>Most launch guides for sale right now were written before anyone played the game, and pad
  their pages with rumours dressed up as facts. This one labels every claim.</p>
  <div style="display:grid;gap:3mm;margin:5mm 0 7mm">
   <div>{OK}<div class="mute" style="margin-top:1mm;font-size:8.6pt">Stated by Rockstar, Take-Two, Sony or Microsoft.</div></div>
   <div>{REP}<div class="mute" style="margin-top:1mm;font-size:8.6pt">Several credible outlets, no first-party statement.</div></div>
   <div>{RUM}<div class="mute" style="margin-top:1mm;font-size:8.6pt">Speculation. Listed so you can ignore it on purpose.</div></div>
  </div>
  <div class="callout" data-icon="↻"><b>Buy once, get every edition.</b><br>
   Edition 1.1 adds first-week field notes from real play. If Rockstar changes something, you get the fix free.</div>
 </div>
</div>""", R, "Contents", 2)

glance = page(f"""
<div class="kicker">At a glance</div>
<h2 class="display" style="font-size:44pt;margin:3mm 0 8mm;color:#fff">The four numbers<br><span class="grad">that matter</span></h2>
<div class="grid g2" style="gap:5mm">
 <div class="card hot stat"><div class="big">NOV 19</div><div class="lbl">Launch day · Thursday</div>
   <p style="margin-top:3mm">PS5, Xbox Series X and Series S. {OK}</p></div>
 <div class="card stat"><div class="big grad">212 GB</div><div class="lbl">Free space needed (up to)</div>
   <p style="margin-top:3mm">Plan for 250 GB so a launch patch doesn't block you. {OK}</p></div>
 <div class="card stat"><div class="big grad">$79.99</div><div class="lbl">Standard Edition · US</div>
   <p style="margin-top:3mm">Ultimate is $99.99. Same story in both. {OK}</p></div>
 <div class="card stat"><div class="big" style="color:#13d6c3">0</div><div class="lbl">Online modes at launch</div>
   <p style="margin-top:3mm">Launches single-player only. Online timing is unannounced. {OK}</p></div>
</div>
<hr class="rule" style="margin:9mm 0 6mm">
<h3>Rumours to ignore on purpose</h3>
<div class="grid g3">
 <div class="card"><span class="pill rum">RUMOUR</span><h4 style="margin-top:3mm">Online on day one</h4><p class="mute">Nothing from Rockstar supports it.</p></div>
 <div class="card"><span class="pill rum">RUMOUR</span><h4 style="margin-top:3mm">PC in Q1 2027</h4><p class="mute">No PC date has been given by anyone official.</p></div>
 <div class="card"><span class="pill rum">RUMOUR</span><h4 style="margin-top:3mm">Exact map size</h4><p class="mute">Any precise count before Nov 19 is a guess.</p></div>
</div>""", R, "At a glance", 3)

facts = page(f"""
{part(1, "Part one", "The fact sheet")}
<table class="t">
<tr><th>What</th><th>Detail</th><th style="width:26mm">Status</th></tr>
<tr><td>Release date</td><td><b>Thursday 19 November 2026</b></td><td>{OK}</td></tr>
<tr><td>Platforms</td><td>PlayStation 5, Xbox Series X, Xbox Series S</td><td>{OK}</td></tr>
<tr><td>PC</td><td>No date announced. A 2027 window is rumoured.</td><td>{RUM}</td></tr>
<tr><td>Standard Edition (US)</td><td><b>$79.99</b></td><td>{OK}</td></tr>
<tr><td>Ultimate Edition (US)</td><td><b>$99.99</b></td><td>{OK}</td></tr>
<tr><td>Upgrade to Ultimate</td><td>No price confirmed. One store listing shows $20.</td><td>{REP}</td></tr>
<tr><td>Digital pre-load</td><td><b>Opens 10 Nov.</b> Xbox opens at 12:00 a.m. GMT worldwide. PS5 opens at midnight in your own time zone.</td><td>{OK}</td></tr>
<tr><td>Install space</td><td><b>Up to 212 GB</b>, depending on device</td><td>{OK}</td></tr>
<tr><td>Physical copies</td><td>At retailers from 12 Nov. Some are code-in-box (a download code, not a full disc).</td><td>{REP}</td></tr>
<tr><td>Pre-order bonus</td><td>Vintage Vice City Pack + one month of GTA+ (Standard)</td><td>{REP}</td></tr>
<tr><td>Online at launch</td><td><b>None.</b> Launches single-player only.</td><td>{OK}</td></tr>
<tr><td>GTA Online (GTA V)</td><td>Not being shut down</td><td>{REP}</td></tr>
<tr><td>Age rating (US)</td><td>ESRB <b>M for Mature 17+</b></td><td>{OK}</td></tr>
<tr><td>Setting</td><td>State of Leonida (based on Florida): Vice City, Ambrosia, Grassrivers, Leonida Keys, Mount Kalaga, Port Gellhorn</td><td>{OK}</td></tr>
<tr><td>Lead characters</td><td>Jason Duval and Lucia Caminos</td><td>{OK}</td></tr>
<tr><td>Delay history</td><td>Delayed twice: to 26 May 2026, then to 19 Nov 2026</td><td>{OK}</td></tr>
</table>""", R, "01 · Fact sheet", 4)

def bar(label, usable, risk=False):
    pct, game = usable / 1900 * 100, 212 / 1900 * 100
    return (f'<div class="row{" risk" if risk else ""}"><span>{label}</span><div class="track"><div class="fill" style="width:{pct:.1f}%"></div>'
            f'<div class="game" style="width:{game:.1f}%"></div></div><span class="v">~{usable} GB</span></div>')

storage = page(f"""
{part(2, "Part two · Do this tonight", "The storage plan")}
<p class="lede" style="max-width:150mm">The game needs <b>up to 212 GB free</b>, and patches arrive on top of that. Aim for <b style="color:#ffc94d">250 GB free</b>.</p>
<div class="card" style="margin:5mm 0 6mm">
 <h3>Usable space vs the game</h3>
 <div class="bars">
  {bar("PS5 (825 GB)", 667)}{bar("PS5 Slim (1 TB)", 848)}{bar("PS5 Pro (2 TB)", 1800)}{bar("Xbox Series X (1 TB)", 802)}{bar("Xbox Series S (512 GB)", 362, True)}
 </div>
 <div class="legend"><span><i style="background:repeating-linear-gradient(135deg,#ff2d8a 0 2mm,#d81b72 2mm 4mm)"></i>GTA VI (212 GB)</span>
  <span><i style="background:#3d2775"></i>Usable out of the box (approx.)</span><span><i style="background:#5a2140"></i>High risk</span></div>
</div>
<div class="grid g2" style="gap:7mm">
 <div><h3>The 10-minute clear-out</h3><div class="steps">
  <div class="step"><div><b>Sort by size</b>Open your console's storage menu and sort installed games by size.</div></div>
  <div class="step"><div><b>Cut the 60-day games</b>Uninstall anything you haven't played in 60 days. Check cloud saves are on first.</div></div>
  <div class="step"><div><b>Delete old captures</b>Video clips quietly eat tens of gigabytes.</div></div>
  <div class="step"><div><b>Park games on USB</b>USB drives can store current-gen games but not run them. Use it as a car park.</div></div>
 </div></div>
 <div><div class="callout warn" data-icon="!"><b>Series S owners.</b><br>~362 GB usable means the game takes more than half your drive. Clear space before 10 Nov, not on launch night.</div>
  <div class="callout" data-icon="i" style="margin-top:4mm">Usable-space figures are approximate and vary with system software.</div></div>
</div>""", R, "02 · Storage", 5)

editions = page(f"""
<h3>Pre-load checklist · opens 10 Nov</h3>
<ul class="check" style="margin-bottom:9mm">
 <li>Pre-order is on the <b>same account</b> you'll play on</li>
 <li>Auto-updates on, so the day-one patch installs overnight</li>
 <li>Rest mode (PS5) or Sleep power mode (Xbox), so it downloads while off</li>
 <li>On the morning of 18 Nov, the download says <b>100%</b>, not "waiting"</li>
</ul>
{part(3, "Part three", "Which edition, honestly")}
<div class="grid g2" style="gap:5mm">
 <div class="card hot"><span class="kicker" style="color:#ffc94d">Our pick for most players</span>
  <h4 style="font-size:28pt;margin:2mm 0">Standard</h4><div class="stat"><div class="big">$79.99</div></div>
  <p style="margin-top:3mm">Here for the story? Unsure? Buy this. You can upgrade later; you can't downgrade.</p></div>
 <div class="card"><span class="kicker">Only if you're certain</span>
  <h4 style="font-size:28pt;margin:2mm 0">Ultimate</h4><div class="stat"><div class="big grad">$99.99</div></div>
  <p style="margin-top:3mm">100+ hours planned and you want every launch bonus. Judge the bonus list on your store page, not the hype.</p></div>
</div>
<div class="grid g2" style="gap:5mm;margin-top:5mm">
 <div class="callout" data-icon="="><b>The disconfirming point.</b> Ultimate bonuses are extras and cosmetics. The main story is identical. Online-themed bonuses do nothing on day one.</div>
 <div class="callout" data-icon="⌂"><b>Physical vs digital.</b> A code-in-box copy still downloads the full 212 GB. Buy it for the box or resale value, not to save bandwidth.</div>
</div>""", R, "03 · Editions", 6)

def ev(day, date, text, key=False):
    return f'<div class="ev{" key" if key else ""}"><div class="d"><small>{day}</small>{date}</div><div class="body">{text}</div></div>'

week = page(f"""
{part(4, "Part four", "Launch week, day by day")}
<div class="tl" style="margin-top:4mm">
 {ev("Mon", "9 Nov", "<b>Clear storage</b> (Part 2). Check that your pre-order is there.")}
 {ev("Tue", "10 Nov", "<b>Pre-load opens.</b> Start it the same day. 212 GB on 100 Mbps is roughly 4.5 to 5 hours in ideal conditions, and launch-week servers are rarely ideal.", True)}
 {ev("Thu", "12 Nov", "<b>Physical copies</b> reported to arrive. Install from the code right away.")}
 {ev("12 to 18", "Nov", "<b>Spoiler lockdown</b> (Part 6). Mute, unfollow, stay out of comment sections.")}
 {ev("Wed", "18 Nov", "<b>Final checks.</b> Pre-load at 100%. Controllers charged. Day-one patch downloaded if it's out.")}
 {ev("Thu", "19 Nov", "<b>Launch.</b> Play the story. There's no Online mode to rush yet.", True)}
 {ev("Fri", "20 Nov", "Reported <b>last day for pre-order bonuses</b> if you haven't bought yet.")}
</div>
<div class="card" style="margin-top:6mm">
 <h3>How long will 212 GB take?</h3>
 <div class="grid" style="grid-template-columns:repeat(5,1fr);gap:3mm;text-align:center">
  <div class="stat"><div class="big" style="font-size:24pt">9.4 h</div><div class="lbl">50 Mbps</div></div>
  <div class="stat"><div class="big" style="font-size:24pt">4.7 h</div><div class="lbl">100 Mbps</div></div>
  <div class="stat"><div class="big grad" style="font-size:24pt">1.6 h</div><div class="lbl">300 Mbps</div></div>
  <div class="stat"><div class="big grad" style="font-size:24pt">57 min</div><div class="lbl">500 Mbps</div></div>
  <div class="stat"><div class="big" style="font-size:24pt;color:#13d6c3">28 min</div><div class="lbl">1 Gbps</div></div>
 </div>
 <p class="mute" style="font-size:7.8pt;margin:3mm 0 0">Best-case maths at full speed. Launch-week servers, Wi-Fi and other devices on your network will make it slower. Use a cable if you can.</p>
</div>""", R, "04 · Launch week", 7)

habits = [("Go through every settings menu first", "Subtitles, camera sensitivity, aim assist, HUD size, audio mix. Ten minutes now beats changing them ten hours in."),
          ("Pick your picture mode", "If the game offers a performance or quality mode, choose before you form an opinion of how it looks."),
          ("Save by hand before big moments", "Don't rely only on autosaves."),
          ("Story first, explore second", "Rockstar often unlocks activities and areas through story progress. Exploring early can mean locked doors."),
          ("Don't spend all your money early", "Rockstar economies have historically rewarded patience. We'll check whether this holds in VI."),
          ("Write down where things are", "A notes app beats your memory of a shop or hidden spot three days later."),
          ("Take a break every two hours", "Launch-week burnout is real. The game will still be there.")]
cards = "".join(f'<div class="card"><div style="font-family:Anton;font-size:26pt;line-height:1;color:#ff2d8a">{i+1:02d}</div>'
                f'<h4 style="font-size:13.5pt;margin:2mm 0 1.5mm">{t}</h4><p class="mute" style="margin:0">{d}</p></div>' for i, (t, d) in enumerate(habits))
session = page(f"""
{part(5, "Part five", "Your first session")}
<p class="lede" style="max-width:155mm;margin-bottom:6mm">Habits that pay off in any Rockstar open world. None of this depends on unreleased mechanics, and every one gets checked against the real game in Edition 1.1.</p>
<div class="grid g2" style="gap:4mm">{cards}
 <div class="card hot" style="display:flex;flex-direction:column;justify-content:center"><span class="kicker" style="color:#ffc94d">Edition 1.1</span>
  <h4 style="font-size:16pt;margin-top:2mm">Verified against the real game in launch week</h4></div>
</div>""", R, "05 · First session", 8)

mutes = ["GTA 6 ending", "GTA VI ending", "Lucia dies", "Jason dies", "final mission", "leaked gameplay"]
spoil = page(f"""
{part(6, "Part six", "Spoiler lockdown")}
<div class="grid g2" style="gap:6mm">
 <div>
  <h3>Mute these words</h3>
  <div>{"".join(f'<span class="chip">{m}</span>' for m in mutes)}</div>
  <p class="mute" style="font-size:8pt;margin-top:2mm">This is a filter list, not a hint about the plot. Nobody outside Rockstar knows the ending yet.</p>
 </div>
 <div class="steps" style="gap:2.5mm">
  <div class="step"><div><b>YouTube</b>Pause watch history. Click "Not interested" on any upload titled "ending" or "full story".</div></div>
  <div class="step"><div><b>X · Threads · Bluesky</b>Add the muted words on the left.</div></div>
  <div class="step"><div><b>Reddit · TikTok</b>Stay out of general gaming subreddits. On TikTok, long-press "Not interested" on the first spoiler you see.</div></div>
 </div>
</div>
<hr class="rule" style="margin:8mm 0">
{part(7, "Part seven", "For creators")}
<div class="grid g2" style="gap:5mm">
 <div class="card"><h4>Know the rules</h4><p>Read Rockstar Support's <i>Policy on posting copyrighted Rockstar Games material</i>. Gameplay footage is generally allowed. <b>Using logos or official art to suggest you're endorsed is not.</b></p></div>
 <div class="card"><h4>Radio = claims</h4><p>Licensed in-game radio music can trigger Content ID claims. Turn the radio down or off for clips you plan to post.</p></div>
 <div class="card"><h4>Set capture now</h4><p><b>PS5:</b> Settings › Captures and Broadcasts<br><b>Xbox:</b> Settings › Preferences › Capture &amp; share</p></div>
 <div class="card"><h4>Label spoilers</h4><p>Put "spoilers" in the title and thumbnail for late-story uploads. Audiences remember who spoiled them.</p></div>
</div>""", R, "06–07 · Spoilers & creators", 9)

back = f"""<section class="page">
{scene(sky="linear-gradient(180deg,#0b031d 0%,#1d0a40 45%,#5a1670 70%,#ff2d8a 86%,#ff8a3d 92%)",
       sun="linear-gradient(180deg,#ffd27a,#ff6d5a 50%,#ff2d8a)", sea="#12062a", horizon=92, sun_size=70, sun_top=82)}
<div class="inner" style="top:18mm">
 {part(8, "Part eight · Free to you", "Edition 1.1")}
 <p class="lede" style="max-width:150mm">Within the first week after 19 November, this guide gets field notes from real play.</p>
 <ul class="check" style="max-width:120mm;margin:5mm 0 10mm">
  <li>Verified settings recommendations</li><li>An early-game money plan, built on the real economy</li>
  <li>Side activities worth doing first, and ones to skip</li><li>Corrections to anything Part 5 got wrong</li>
  <li>An Online section once Rockstar announces it</li></ul>
 <h3>Sources · checked 9 November 2026</h3>
 <p class="mute" style="font-size:7.8pt;line-height:1.55;max-width:150mm">Rockstar Support: <i>Grand Theft Auto VI Pre-Load FAQ</i> and <i>Policy on posting copyrighted Rockstar Games material</i>.
 Rockstar mod guidelines (Sept 2026), as reported by Insider Gaming, MP1st and Dot Esports. Pre-load date, time and size, as reported by VGC, Guru3D, HotHardware and Notebookcheck.
 Series S storage: IBTimes UK. Single-player launch scope: OpenCritic, dlcompare. ESRB rating: Vice, CheatCC. Trailer 2 details: GamesRadar, TechRadar, Shacknews.
 Prices are US list prices and vary by region and retailer.</p>
 <p class="mute" style="font-size:7.8pt;max-width:150mm"><i>Grand Theft Auto</i> and <i>GTA</i> are trademarks of Take-Two Interactive, used here only to identify the game. This guide contains no game art, logos, leaked or datamined material.</p>
</div></section>"""

render([cover, toc, glance, facts, storage, editions, week, session, spoil, back],
       pathlib.Path(__file__).with_name("Day-One-Playbook.pdf"), "night")
