"""THE FIRST-TIMER'S PLAYBOOK — GTA VI for grown-ups who have never played a video game.

Large print (13pt+ body, Atkinson Hyperlegible: a typeface designed for low-vision readers),
light high-contrast pages, one idea per page. Facts checked 9 Nov 2026 — see SOURCES.md.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from design import page, part, scene, render

R = "The First-Timer's Playbook"

cover = f"""<section class="page">
{scene(sky="linear-gradient(180deg,#3b1a78 0%,#8a2a9a 22%,#ff4f8b 44%,#ff8a3d 60%,#ffc94d 70%)",
       sun="linear-gradient(180deg,#fff2b0,#ffc04d 50%,#ff7a3d)",
       sea="repeating-linear-gradient(180deg,#2a0f5c 0 3mm,#3a1878 3mm 4mm)", palm_color="#24083f")}
<div style="position:absolute;left:18mm;right:18mm;top:18mm;color:#fff">
  <div class="kicker" style="color:#fff;font-size:9pt">For grown-ups new to video games</div>
  <h1 class="display" style="font-size:70pt;margin:7mm 0 6mm;text-shadow:0 0 20px rgba(122,43,209,.7),3px 3px 0 #7a2bd1">The<br>First-Timer's<br>Playbook</h1>
  <div style="font-family:'Atkinson Hyperlegible';font-size:17pt;line-height:1.35;max-width:140mm;text-shadow:0 1px 8px rgba(40,8,70,.85),0 0 2px rgba(40,8,70,.9)">
    Never held a controller? Start here.<br>A plain-English guide to <b>Grand Theft Auto VI</b>.</div>
</div>
<div style="position:absolute;right:16mm;bottom:24mm;width:46mm;height:46mm;border-radius:50%;background:#fff7ec;color:#1b1238;
     display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;transform:rotate(-8deg);box-shadow:0 0 0 2.5mm #ff2d8a">
  <span style="font-family:Anton;font-size:24pt;line-height:1">LARGE</span><span style="font-family:Anton;font-size:24pt;line-height:1;color:#ff2d8a">PRINT</span>
  <span style="font-size:7pt;font-weight:800;letter-spacing:.14em;margin-top:1mm">NO JARGON</span></div>
<div style="position:absolute;left:0;right:0;bottom:9mm;text-align:center;font-size:7.5pt;color:#d9cdf2;letter-spacing:.04em">
  Unofficial. Not made, endorsed or sponsored by Rockstar Games or Take-Two Interactive.</div>
</section>"""

welcome = page("""
<div class="kicker">Welcome</div>
<h2 class="display grad" style="font-size:48pt;margin:3mm 0 6mm">You don't have to<br>be good at games.</h2>
<div class="grid" style="grid-template-columns:1.1fr 1fr;gap:10mm">
 <div>
  <p class="lede">Maybe the grandkids won't stop talking about it. Maybe you've seen the trailer and thought:
  <i>that looks like a film I'd watch.</i> Either way, this guide assumes you have never played a video game. Not once.</p>
  <p>We'll go slowly. One idea per page. Every word that sounds like jargon is explained on page 10.</p>
  <p>We'll also be straight with you, including about whether this game is right for you at all.</p>
  <div class="callout" data-icon="✓" style="margin-top:6mm"><b>Every fact was checked</b> on 9 November 2026. Where something isn't confirmed yet, we say so.</div>
 </div>
 <div class="toc">
  <div class="row"><span class="n">01</span><span class="t">Is it for you?<small>An honest look</small></span><span class="p">03</span></div>
  <div class="row"><span class="n">02</span><span class="t">Shopping list<small>What you need, what it costs</small></span><span class="p">04</span></div>
  <div class="row"><span class="n">03</span><span class="t">Which console<small>The simple choice</small></span><span class="p">05</span></div>
  <div class="row"><span class="n">04</span><span class="t">Setting up<small>Eight steps</small></span><span class="p">06</span></div>
  <div class="row"><span class="n">05</span><span class="t">The controller<small>What each part does</small></span><span class="p">07</span></div>
  <div class="row"><span class="n">06</span><span class="t">Get comfortable<small>Eyes, ears, hands</small></span><span class="p">08</span></div>
  <div class="row"><span class="n">07</span><span class="t">Your first hour<small>Six golden rules</small></span><span class="p">09</span></div>
  <div class="row"><span class="n">08</span><span class="t">Words you'll hear<small>Plain-English glossary</small></span><span class="p">10</span></div>
  <div class="row"><span class="n">09</span><span class="t">Money &amp; safety<small>Avoid launch scams</small></span><span class="p">11</span></div>
  <div class="row" style="border:0"><span class="n">★</span><span class="t">Cheat sheet<small>Keep it by the TV</small></span><span class="p">12</span></div>
 </div>
</div>""", R, "Welcome", 2)

warnings = ["Blood and Gore", "Intense Violence", "Strong Language", "Strong Sexual Content", "Nudity", "Use of Drugs and Alcohol", "Mature Humor"]
foryou = page(f"""
{part(1, "Part one", "Is it for you?")}
<div class="grid g2" style="gap:7mm">
 <div>
  <h3>What it actually is</h3>
  <p>Think of a crime drama on TV, except <b>you</b> steer the main characters. The story follows
  <b>Jason Duval</b> and <b>Lucia Caminos</b> in <b>Leonida</b>, a made-up state based on Florida, centred on Vice City, a version of Miami.</p>
  <p>Between story chapters you can wander freely: drive the coast, explore towns and swamps, or just watch the sunset.</p>
 </div>
 <div class="card hot">
  <h3>The honest part</h3>
  <div style="display:flex;align-items:center;gap:4mm;margin-bottom:3mm">
   <div style="font-family:Anton;font-size:46pt;line-height:1;color:#ff2d8a">M</div>
   <div style="font-size:12pt;line-height:1.3"><b>Rated Mature 17+</b><br>by the ESRB, the US age-rating board</div></div>
  <p style="font-size:12pt;margin:0">If you'd switch off an R-rated crime film, you'll probably want to skip this one.</p>
 </div>
</div>
<h3 style="margin-top:6mm">The official content warnings</h3>
<div style="margin-bottom:5mm">{"".join(f'<span class="chip" style="background:#fff;color:#1b1238;border:1.5px solid #ff2d8a;font-family:Atkinson Hyperlegible;font-size:11.5pt">{w}</span>' for w in warnings)}</div>
<div class="grid g2" style="gap:6mm">
 <div class="callout" data-icon="$"><b>"In-Game Purchases"</b> is on the rating too. The game sells optional extras. You never need them for the story. See page 11.</div>
 <div class="callout" data-icon="♥"><b>Not sure?</b> Watch a family member play for an evening first. Plenty of people enjoy the story that way, and it costs nothing.</div>
</div>""", R, "01 · Is it for you?", 3)

shopping = page("""
{part}
<div class="grid g2" style="gap:5mm;margin-bottom:6mm">
 <div class="card"><h4>1 · A console</h4><p style="margin:0">A PlayStation 5 or an Xbox Series X or S. <b>Not</b> a PC, phone or older console yet.</p></div>
 <div class="card"><h4>2 · A TV</h4><p style="margin:0">Any TV with an <b>HDMI</b> socket. Most TVs from the last 15 years have one.</p></div>
 <div class="card"><h4>3 · Internet</h4><p style="margin:0">The game is a <b>212 GB</b> download. If your plan has a monthly data limit, check it first.</p></div>
 <div class="card"><h4>4 · A free account</h4><p style="margin:0">PlayStation or Microsoft. Free to create during setup. Just an email and password.</p></div>
</div>
<h3>What it costs (US list prices, November 2026)</h3>
<table class="t">
<tr><th>Item</th><th>Price</th></tr>
<tr><td>The game, Standard Edition</td><td><b>$79.99</b> (all you need)</td></tr>
<tr><td>Xbox Series S, 512 GB</td><td>$499.99 (tight on space, see page 5)</td></tr>
<tr><td>Xbox Series S, 1 TB</td><td>$599.99</td></tr>
<tr><td>Xbox Series X</td><td>$749.99 (no disc drive) · $799.99 (with disc drive)</td></tr>
<tr><td>PlayStation 5</td><td>About $500 to $900 depending on model. Prices moved several times in 2026, so check on the day.</td></tr>
</table>
<div class="callout" data-icon="✓" style="margin-top:6mm"><b>Good news: no subscription needed.</b> You do <i>not</i> need PlayStation Plus, Game Pass or GTA+ to play the story. Shops may offer them. You can say no.</div>
""".replace("{part}", part(2, "Part two", "Your shopping list")), R, "02 · Shopping list", 4)

console = page(f"""
{part(3, "Part three", "Which console?")}
<div class="card hot" style="margin-bottom:6mm;padding:7mm">
 <span class="kicker">Rule number one</span>
 <h4 style="font-size:26pt;margin:2mm 0 2mm">Buy what the family already has.</h4>
 <p style="margin:0;font-size:14pt">If the grandkids play on PlayStation, get a PlayStation. You'll have built-in help on speed dial.</p>
</div>
<div class="grid g3" style="gap:4mm">
 <div class="card"><h4>PlayStation 5</h4><p style="margin:0">Popular, plenty of space for the game. A good default.</p></div>
 <div class="card"><h4>Xbox Series X</h4><p style="margin:0">Just as capable. Roughly 800 GB usable, so plenty of space.</p></div>
 <div class="card" style="border-color:#ff2d8a"><h4 style="color:#ff2d8a">Xbox Series S</h4><p style="margin:0">Cheapest, but the 512 GB model fills up fast. The game takes over half.</p></div>
</div>
<h3 style="margin-top:8mm">Two traps to avoid</h3>
<div class="steps">
 <div class="step"><div><b>"Digital Edition" means no disc slot.</b>That's fine, but then buy the game from the console's own store, not a box from a shop.</div></div>
 <div class="step"><div><b>Don't buy an older console.</b>A PS4 or Xbox One <i>cannot</i> play this game. Check the box says <strong>PS5</strong> or <strong>Xbox Series</strong>.</div></div>
</div>""", R, "03 · Which console", 5)

setup = page(f"""
{part(4, "Part four", "Setting up")}
<p class="lede" style="margin-bottom:6mm">Set aside an afternoon. Most of it is waiting for downloads, so put the kettle on.</p>
<div class="grid g2" style="gap:6mm">
 <div class="steps">
  <div class="step"><div><b>Plug in</b>Power cable to the wall, HDMI cable to your TV.</div></div>
  <div class="step"><div><b>Pick the TV input</b>Press "Input" or "Source" on your TV remote until the console appears.</div></div>
  <div class="step"><div><b>Charge the controller</b>Connect it to the console with the USB cable in the box.</div></div>
  <div class="step"><div><b>Follow the screen</b>Choose language and Wi-Fi. A cable to your router is faster if it reaches.</div></div>
 </div>
 <div class="steps" style="counter-reset:s 4">
  <div class="step"><div><b>Create your account</b>Write the email and password on the cheat sheet (page 12).</div></div>
  <div class="step"><div><b>Let it update</b>The console will update itself. Normal. Don't switch it off.</div></div>
  <div class="step"><div><b>Buy the game</b>From the console's own store: PlayStation Store or Microsoft Store.</div></div>
  <div class="step"><div><b>Let it download</b>This can take hours. Leave it overnight in rest/sleep mode.</div></div>
 </div>
</div>
<div class="callout warn" data-icon="!" style="margin-top:7mm"><b>Release day is Thursday 19 November 2026.</b> You can buy and download from 10 November, but it won't start until release day.</div>""", R, "04 · Setting up", 6)

CTRL = """<svg viewBox="0 0 900 430" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'Atkinson Hyperlegible'">
<g transform="translate(150,80)">
 <rect x="95" y="20" width="110" height="26" rx="12" fill="#ffd3e4" stroke="#1b1238" stroke-width="3"/>
 <rect x="395" y="20" width="110" height="26" rx="12" fill="#ffd3e4" stroke="#1b1238" stroke-width="3"/>
 <rect x="105" y="44" width="95" height="16" rx="7" fill="#e7d9ff" stroke="#1b1238" stroke-width="3"/>
 <rect x="400" y="44" width="95" height="16" rx="7" fill="#e7d9ff" stroke="#1b1238" stroke-width="3"/>
 <path d="M150 60 Q 300 45 450 60 Q 525 72 548 150 L 578 262 Q 590 312 548 318 Q 510 322 488 288 L 452 236 Q 300 220 148 236 L 112 288 Q 90 322 52 318 Q 10 312 22 262 L 52 150 Q 75 72 150 60 Z"
       fill="#fff" stroke="#1b1238" stroke-width="4"/>
 <g fill="#1b1238"><rect x="128" y="112" width="20" height="56" rx="4"/><rect x="110" y="130" width="56" height="20" rx="4"/></g>
 <g fill="#fff" stroke="#1b1238" stroke-width="3"><circle cx="452" cy="176" r="15"/><circle cx="416" cy="140" r="15"/><circle cx="488" cy="140" r="15"/></g>
 <circle cx="452" cy="104" r="15" fill="#13d6c3" stroke="#1b1238" stroke-width="3"/>
 <circle cx="230" cy="208" r="36" fill="#ff2d8a" stroke="#1b1238" stroke-width="4"/><circle cx="230" cy="208" r="20" fill="#ff7aae"/>
 <circle cx="370" cy="208" r="36" fill="#7a2bd1" stroke="#1b1238" stroke-width="4"/><circle cx="370" cy="208" r="20" fill="#a46bf0"/>
 <rect x="372" y="98" width="22" height="13" rx="6" fill="#ffc94d" stroke="#1b1238" stroke-width="2.5"/>
</g>
<g stroke="#1b1238" stroke-width="2" fill="none">
 <path d="M300 100 L 300 40 L 240 40"/>
 <path d="M533 178 L 533 40 L 690 40"/>
 <path d="M260 220 L 150 220"/>
 <path d="M654 220 L 745 220"/>
 <path d="M380 324 L 380 378"/><path d="M520 324 L 520 378"/>
</g>
<g fill="#1b1238" font-size="18">
 <text x="0" y="34" font-weight="700" fill="#ff2d8a">TRIGGERS</text><text x="0" y="56">Gas &amp; brake · aim</text>
 <text x="700" y="34" font-weight="700" fill="#ff2d8a">PAUSE / MENU</text><text x="700" y="56">Map · settings</text>
 <text x="0" y="214" font-weight="700" fill="#ff2d8a">D-PAD</text><text x="0" y="236">Shortcuts</text>
 <text x="755" y="214" font-weight="700" fill="#ff2d8a">ACTIONS</text><text x="755" y="236">Press what the</text><text x="755" y="256">screen shows</text>
 <text x="330" y="402" font-weight="700" fill="#ff2d8a">LEFT STICK</text><text x="330" y="424">Walk · steer</text>
 <text x="490" y="402" font-weight="700" fill="#7a2bd1">RIGHT STICK</text><text x="490" y="424">Look around</text>
</g></svg>"""

controller = page(f"""
{part(5, "Part five", "The controller")}
<p class="lede" style="margin-bottom:2mm">It looks complicated. It isn't. <b>Two thumbs do almost everything.</b></p>
{CTRL}
<div class="grid g2" style="gap:6mm;margin-top:4mm">
 <table class="t"><tr><th>On a PlayStation</th><th>On an Xbox</th></tr>
  <tr><td>L2 · R2 (triggers)</td><td>LT · RT</td></tr><tr><td>L1 · R1</td><td>LB · RB</td></tr>
  <tr><td>✕ ○ □ △</td><td>A B X Y</td></tr><tr><td>Options</td><td>Menu ≡</td></tr></table>
 <div class="callout" data-icon="i" style="font-size:12pt">Rockstar hasn't published the exact controls yet. This is what each part usually does in games like this. <b>The game shows you on screen</b> which button to press, every time it matters.</div>
</div>""", R, "05 · The controller", 7)

comfort = page(f"""
{part(6, "Part six", "Get comfortable")}
<p class="lede" style="margin-bottom:6mm">Both consoles have an <b>Accessibility</b> menu in Settings. Ten minutes there makes everything easier.</p>
<div class="grid g2" style="gap:5mm">
 <div class="card"><h4>Your eyes</h4><p style="margin:0">Turn on <b>larger text</b>, <b>bold text</b> and <b>high contrast</b> in the console's Accessibility settings. Sit at your usual TV distance, with a lamp on.</p></div>
 <div class="card"><h4>Your ears</h4><p style="margin:0">Turn <b>subtitles on</b> in the game's settings. If dialogue is hard to hear, look for a separate volume for speech and music.</p></div>
 <div class="card"><h4>Your hands</h4><p style="margin:0">Both consoles let you <b>change which button does what</b>. Xbox's <b>Copilot</b> lets a helper's controller work alongside yours.</p></div>
 <div class="card"><h4>Your stomach</h4><p style="margin:0">Some people feel queasy at first. Sit further back, keep the lights on, and turn down any <b>camera shake</b> or <b>motion blur</b> option.</p></div>
</div>
<div class="callout warn" data-icon="!" style="margin-top:7mm"><b>Feeling dizzy? Stop and rest.</b> Motion sickness from games is common and usually fades with short sessions. Start with 20 to 30 minutes.</div>
<p class="mute" style="font-size:11pt;margin-top:4mm">Rockstar hasn't announced the game's own accessibility options yet. The console settings above are available today.</p>""", R, "06 · Comfort", 8)

rules = [("You can't break it", "Nothing you press will damage the console or ruin the game."),
         ("Pause any time", "Press Options/Menu. The world freezes until you come back."),
         ("Failing is normal", "Everyone fails missions. The game restarts you just before the tricky bit."),
         ("Follow the marker", "A small map in the corner shows where to go next. Head for the marker."),
         ("Read the hints", "Early on, the game pops up instructions. It teaches you as you go."),
         ("Little and often", "Thirty minutes a day beats a four-hour marathon. You'll learn faster too.")]
first = page(f"""
{part(7, "Part seven", "Your first hour")}
<p class="lede" style="margin-bottom:6mm">The opening is a guided tutorial. The game teaches you step by step, so you don't need to memorise anything.</p>
<div class="grid g2" style="gap:4.5mm">{"".join(f'<div class="card"><div style="font-family:Anton;font-size:28pt;line-height:1;color:#ff2d8a">{i+1}</div><h4 style="margin:1.5mm 0">{t}</h4><p style="margin:0">{d}</p></div>' for i,(t,d) in enumerate(rules))}</div>
<div class="callout" data-icon="♥" style="margin-top:6mm"><b>Driving is hard for everyone at first.</b> Find an empty road and practise gentle pushes on the stick. It clicks within an hour.</div>""", R, "07 · First hour", 9)

terms = [("Console", "The box under the TV that runs the game."), ("Controller", "The handheld pad you play with."),
         ("Save", "Stores your progress so you can switch off."), ("Autosave", "The game saving for you, shown by a small spinning icon."),
         ("Checkpoint", "A restart point partway through a mission."), ("Mission", "A story chapter with a goal."),
         ("Cutscene", "A short film scene. Just watch."), ("Open world", "A big map you can roam freely."),
         ("Mini-map", "The small map in the corner of the screen."), ("Waypoint", "A marker you set on the map to guide you."),
         ("HUD", "The info on the edges of the screen: map, money, health."), ("Wanted level", "Police attention. In past GTA games, shown as stars."),
         ("NPC", "Any character controlled by the game, not a person."), ("Patch", "A free update that fixes problems."),
         ("Pre-load", "Downloading the game before release day."), ("Respawn", "Coming back to life after failing.")]
gloss = page(f"""
{part(8, "Part eight", "Words you'll hear")}
<div class="grid g2" style="gap:0 9mm">{"".join(f'<div style="padding:2.6mm 0;border-bottom:1px solid #e2d3c2"><b style="color:#ff2d8a;font-size:13.5pt">{t}</b><br><span style="font-size:12pt">{d}</span></div>' for t,d in terms)}</div>""", R, "08 · Glossary", 10)

money = page(f"""
{part(9, "Part nine", "Money & safety")}
<div class="callout warn" data-icon="!" style="margin-bottom:6mm;font-size:14pt"><b>Big launches attract scams.</b> There is no "free GTA 6 download", no "early access code", and no "PC version" right now. Anyone offering one is lying.</div>
<div class="grid g2" style="gap:5mm">
 <div class="card"><h4>Buy from the source</h4><p style="margin:0">Only the <b>PlayStation Store</b>, the <b>Microsoft Store</b>, or a shop you already trust.</p></div>
 <div class="card"><h4>Lock purchases</h4><p style="margin:0">Turn on <b>"password at checkout"</b> in your account settings. Both consoles offer it, so nothing is bought by accident.</p></div>
 <div class="card"><h4>Extras are optional</h4><p style="margin:0">The game sells add-ons and in-game currency. <b>You never need them</b> to enjoy the story.</p></div>
 <div class="card"><h4>Guard your login</h4><p style="margin:0">Rockstar, Sony and Microsoft will <b>never</b> ask for your password by email, text or phone call.</p></div>
</div>
<div class="callout" data-icon="i" style="margin-top:6mm">There's <b>no online mode at launch</b>. The game is single-player, so you won't be playing with strangers.</div>""", R, "09 · Money & safety", 11)

cheat = page(f"""
<div style="border:3px dashed #ff2d8a;border-radius:6mm;padding:8mm;height:185mm;position:relative;background:#fff">
 <div style="position:absolute;top:-4.5mm;left:10mm;background:#fff7ec;padding:0 3mm;font-family:Inter;font-weight:800;font-size:8pt;letter-spacing:.2em;color:#ff2d8a">✂ CUT OUT · KEEP BY THE TV</div>
 <h2 class="display grad" style="font-size:40pt;margin:0 0 5mm">Cheat sheet</h2>
 <div class="grid" style="grid-template-columns:1.25fr 1fr;gap:7mm">
  <div><table class="t">
   <tr><td>Walk / steer</td><td>Left stick</td></tr><tr><td>Look around</td><td>Right stick</td></tr>
   <tr><td>Pause &amp; map</td><td>Options / Menu</td></tr><tr><td>What to press</td><td>Watch the screen</td></tr>
   <tr><td>Feeling queasy</td><td>Pause. Rest.</td></tr></table></div>
  <div>
   <h3>My account</h3>
   <div style="font-size:12pt;line-height:2.4">Console: ______________________<br>Email: ________________________<br>Password hint: _________________<br>Helper's number: _______________</div>
  </div>
 </div>
 <div class="callout" data-icon="★" style="margin-top:6mm;font-size:13pt"><b>Release day: Thursday 19 November 2026.</b> You can't break it. Failing is normal. Little and often.</div>
</div>
<p class="mute" style="font-size:8.5pt;line-height:1.45;margin-top:6mm"><b>Sources, checked 9 Nov 2026:</b> Rockstar Support Pre-Load FAQ (date, 212 GB) · ESRB rating and descriptors as reported by Vice and CheatCC ·
Xbox prices as reported by Variety and Windows Central (Aug 2026 increase) · PS5 pricing as reported by GamesRadar and TechRadar (sources disagree, hence the range) ·
single-player launch scope as reported by OpenCritic · no confirmed GTA VI accessibility or difficulty options as of publication.
<i>Grand Theft Auto</i> and <i>GTA</i> are trademarks of Take-Two Interactive, used only to identify the game. No game art or logos are used.</p>""", R, "Cheat sheet", 12)

render([cover, welcome, foryou, shopping, console, setup, controller, comfort, first, gloss, money, cheat],
       pathlib.Path(__file__).with_name("First-Timers-Playbook.pdf"), "day")
