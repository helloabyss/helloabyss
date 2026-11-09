"""THE CREATOR PLAYBOOK — making money from GTA VI content, with honest numbers.
Facts checked 9 Nov 2026. Third-party figures are labelled as reported or estimates.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from design import page, part, scene, render

R = "The Creator Playbook"
OK, REP, EST = ('<span class="pill ok">CONFIRMED</span>', '<span class="pill rep">REPORTED</span>',
                '<span class="pill rum">ESTIMATE</span>')

cover = f"""<section class="page">
{scene(sky="linear-gradient(180deg,#05020f 0%,#0d0a3a 30%,#1b1f6b 48%,#13d6c3 64%,#ff2d8a 70%)",
       sun="linear-gradient(180deg,#9ffcf1,#13d6c3 40%,#ff2d8a)",
       sea="repeating-linear-gradient(180deg,#07051d 0 3mm,#110d3a 3mm 4mm)", horizon=70, sun_size=110, palm_color="#05020f")}
<div style="position:absolute;left:18mm;right:18mm;top:18mm">
  <div class="kicker">Edition 1.0 · Facts checked 9 Nov 2026</div>
  <h1 class="display" style="font-size:76pt;color:#fff;margin:7mm 0 5mm;text-shadow:0 0 22px rgba(19,214,195,.7),3px 3px 0 #ff2d8a">The<br>Creator<br>Playbook</h1>
  <div style="font-size:14pt;color:#fff;max-width:135mm;text-shadow:0 1px 8px #05020f,0 0 2px #05020f">How to make money from <b>Grand Theft Auto VI</b> content, with honest numbers and the rules that protect your income.</div>
</div>
<div style="position:absolute;right:16mm;bottom:22mm;width:46mm;height:46mm;border-radius:50%;background:#140a2bdd;border:2px solid #ffc94d;
     display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#ffc94d;transform:rotate(-8deg)">
  <span style="font-family:Anton;font-size:20pt;line-height:1;color:#fff">90-DAY</span>
  <span style="font-size:7.5pt;font-weight:800;letter-spacing:.14em">PLAN<br>INSIDE</span></div>
<div style="position:absolute;left:0;right:0;bottom:9mm;text-align:center;font-size:7pt;color:#a898cc;letter-spacing:.05em">
  Unofficial. Not affiliated with Rockstar Games, Take-Two Interactive, YouTube or Twitch. Educational only. Not financial advice.</div>
</section>"""

reality = page(f"""
<div class="kicker">Read this first</div>
<h2 class="display" style="font-size:40pt;margin:2mm 0 5mm;color:#fff">Views are cheap.<br><span class="grad">Trust is the money.</span></h2>
<div class="grid g3" style="gap:4mm;margin-bottom:5mm">
 <div class="card stat"><div class="big grad" style="font-size:28pt">$0.02–0.05</div><div class="lbl">Gaming Shorts · per 1,000 views</div><p style="margin-top:2mm">{EST}</p></div>
 <div class="card stat"><div class="big grad" style="font-size:28pt">~$1.50–3.50</div><div class="lbl">Gaming long-form · per 1,000 views</div><p style="margin-top:2mm">{EST}</p></div>
 <div class="card hot stat"><div class="big" style="font-size:28pt">~$4.30</div><div class="lbl">You keep from one $4.99 guide sale</div><p style="margin-top:2mm">Payhip free plan, after fees</p></div>
</div>
<p class="lede">One million GTA Shorts views might earn <b>$20 to $50</b> in ad revenue. A hundred people buying a $4.99 guide earns about <b>$430</b>.
That's the whole strategy in two sentences: <b>use Shorts for reach, long-form for ad revenue, and your own products for income.</b></p>
<div class="grid g2" style="gap:5mm;margin-top:5mm">
 <div class="callout warn" data-icon="!"><b>The disconfirming data.</b> Most creators earn little or nothing. GTA VI will be one of the most crowded niches on YouTube. Nothing here is an income promise.</div>
 <div class="callout" data-icon="i">RPM figures are third-party estimates from creator-analytics firms. They vary widely by country, season and audience. Your own YouTube Studio numbers beat any estimate.</div>
</div>
<div class="toc" style="margin-top:4mm">
<style>.toc .row{{padding:1.6mm 0}}</style>
 <div class="row"><span class="n">01</span><span class="t">The money map<small>Seven income streams, ranked</small></span><span class="p">03</span></div>
 <div class="row"><span class="n">02</span><span class="t">Getting monetized<small>The February 2027 deadline</small></span><span class="p">04</span></div>
 <div class="row"><span class="n">03</span><span class="t">Rules that protect income<small>Rockstar + YouTube's 7-second rule</small></span><span class="p">05</span></div>
 <div class="row"><span class="n">04</span><span class="t">What to make, when<small>The launch-window calendar</small></span><span class="p">06</span></div>
 <div class="row"><span class="n">05+</span><span class="t">Products · sponsors · faceless · 90 days<small>Turning views into income</small></span><span class="p">07</span></div>
</div>""", R, "Reality check", 2)

streams = [("Your own guides", "Day 1", "~90%", "You", True),
           ("Affiliate links", "Day 1", "Small %", "Retailer", False),
           ("Services for creators", "Day 1", "100%", "You", False),
           ("Fan funding (Super Thanks, memberships)", "500 subs", "Majority", "YouTube", False),
           ("YouTube ad revenue", "1,000 subs + hours/views", "55% long · 45% Shorts", "YouTube", False),
           ("Twitch subs and bits", "Affiliate", "Varies", "Twitch", False),
           ("Sponsorships", "Proven audience", "100% of the fee", "Brand", False)]
rows = "".join(f'<tr><td>{"<span style=color:#ffc94d>★ </span>" if star else ""}{n}</td><td>{w}</td><td>{k}</td><td>{c}</td></tr>' for n, w, k, c, star in streams)
money_map = page(f"""
{part(1, "Part one", "The money map")}
<p class="lede" style="margin-bottom:5mm">Seven ways GTA VI creators get paid. Three of them work from your <b>first day</b>, before YouTube pays you a cent.</p>
<table class="t"><tr><th>Stream</th><th>Available from</th><th>What you keep</th><th>Who controls it</th></tr>{rows}</table>
<div class="grid g3" style="gap:4mm;margin-top:7mm">
 <div class="card hot"><h4>Start here</h4><p style="margin:0">Your own guides. Highest margin, and nobody can demonetize them.</p></div>
 <div class="card"><h4>Build toward</h4><p style="margin:0">YouTube Partner Program. Slow, but it compounds on evergreen guide videos.</p></div>
 <div class="card"><h4>Later</h4><p style="margin:0">Sponsors want proof. A steady view count and a clean channel come first.</p></div>
</div>
<p class="mute" style="font-size:7.8pt;margin-top:4mm">The 55% / 45% ad-revenue split is from YouTube's Partner Program terms. "Services" means editing, thumbnails or voiceover for other GTA creators.</p>""", R, "01 · Money map", 3)

ypp = page(f"""
{part(2, "Part two", "Getting monetized")}
<table class="t" style="margin-bottom:6mm">
<tr><th>YouTube tier</th><th>Requirement</th><th>Unlocks</th></tr>
<tr><td>Lower tier</td><td>500 subscribers + 3 uploads in 90 days + either 3,000 watch hours in 12 months <i>or</i> 3M Shorts views in 90 days</td><td>Memberships, Super Thanks, Shopping</td></tr>
<tr><td>Full YPP (until 31 Jan 2027)</td><td>1,000 subscribers + either <b>4,000</b> watch hours in 12 months <i>or</i> <b>10M</b> Shorts views in 90 days</td><td>Ad revenue</td></tr>
<tr><td>Full YPP (from 1 Feb 2027)</td><td>1,000 subscribers + either <b>8,000</b> watch hours <i>or</i> <b>20M</b> Shorts views</td><td>Ad revenue</td></tr>
</table>
<div class="card hot" style="padding:7mm;margin-bottom:6mm">
 <span class="kicker" style="color:#ffc94d">The deadline nobody's talking about {REP}</span>
 <h4 style="font-size:24pt;margin:2mm 0">Qualify before 1 February 2027</h4>
 <p style="margin:0;font-size:11pt">YouTube reportedly doubles the entry bar for <i>new</i> applicants from that date, and existing partners keep their status. GTA VI's launch window falls neatly before it. Treat the next 12 weeks as your best shot at the lower bar.</p>
</div>
<div class="grid g2" style="gap:5mm">
 <div class="card"><h4>Watch-hours path</h4><p style="margin:0">Long-form guides of 8 to 15 minutes. 4,000 hours is about 24,000 viewers watching 10 minutes each. Shorts watch time <b>doesn't count</b>.</p></div>
 <div class="card"><h4>Shorts path</h4><p style="margin:0">10M Shorts views in 90 days is roughly 111,000 a day. Possible in a launch window, hard afterwards. The two paths don't combine.</p></div>
</div>
<p class="mute" style="font-size:7.8pt;margin-top:4mm">Only public videos count. Ad-campaign views don't count. Thresholds are as reported by vidIQ and AIR Media-Tech; check the Earn tab in YouTube Studio.</p>""", R, "02 · Monetization", 4)

rules = page(f"""
{part(3, "Part three", "Rules that protect income")}
<div class="grid g2" style="gap:6mm">
 <div>
  <h3>Rockstar's video policy</h3>
  <div class="steps" style="gap:2.5mm">
   <div class="step"><div><b>Allowed:</b>Your own gameplay, Let's Plays, reviews, guides. Rockstar says it's happy for fans to upload gameplay.</div></div>
   <div class="step"><div><b>Removed:</b>Pre-release or leaked footage, early unboxings, videos of the ending, and cutscenes uploaded on their own.</div></div>
   <div class="step"><div><b>Grey area:</b>The policy is written for non-commercial fan use. For anything beyond normal ad revenue, email <span class="chip" style="margin:0">copyright@take2games.com</span> first.</div></div>
  </div>
 </div>
 <div>
  <h3>YouTube's gaming-violence rules {REP}</h3>
  <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:2mm;text-align:center;margin-bottom:3mm">
   <div class="card" style="padding:3mm;border-color:#ff2d8a"><div style="font-family:Anton;font-size:20pt;color:#ff2d8a">0–7s</div><div style="font-size:8pt">Graphic violence = <b>no ads</b></div></div>
   <div class="card" style="padding:3mm;border-color:#ffc94d"><div style="font-family:Anton;font-size:20pt;color:#ffc94d">8–15s</div><div style="font-size:8pt"><b>Limited</b> ads</div></div>
   <div class="card" style="padding:3mm;border-color:#13d6c3"><div style="font-family:Anton;font-size:20pt;color:#13d6c3">15s+</div><div style="font-size:8pt">Broader eligibility</div></div>
  </div>
  <p>Open every video on a calm hook (a car, a view, your narration), not a shootout. Keep gore out of thumbnails and titles. Gaming drug-use content became eligible for ads in the same September 2026 update.</p>
 </div>
</div>
<div class="grid g3" style="gap:4mm;margin-top:6mm">
 <div class="callout warn" data-icon="♪"><b>Radio = Content ID.</b> Licensed in-game music can send your revenue to the rights holder. Turn the radio off when recording.</div>
 <div class="callout warn" data-icon="✕"><b>No logos or key art</b> on thumbnails, products or channel art. Make your own.</div>
 <div class="callout" data-icon="!"><b>Inauthentic content.</b> YouTube can remove mass-produced, repetitive channels from YPP. Faceless is fine; low-effort isn't.</div>
</div>""", R, "03 · Rules", 5)

def ev(day, date, text, key=False):
    return f'<div class="ev{" key" if key else ""}"><div class="d"><small>{day}</small>{date}</div><div class="body">{text}</div></div>'

calendar = page(f"""
{part(4, "Part four", "What to make, when")}
<div class="tl">
 {ev("Pre-launch", "Now", "<b>Prep content.</b> Storage, editions, pre-load times, confirmed vs rumour. High search interest, low competition from people with footage.")}
 {ev("Week", "1", "<b>First impressions and settings.</b> \"Best settings\", \"things I wish I knew\", beginner tips. Fast Shorts plus one long video a day if you can.", True)}
 {ev("Weeks", "2–6", "<b>Search-driven guides.</b> Money methods, where to find things, side activities. These are the videos people search for and keep watching for months.", True)}
 {ev("Online", "TBA", "<b>Online mode.</b> No date yet. When Rockstar announces it, a second launch window opens. Be first with a starter guide.")}
 {ev("PC · rumour", "2027?", "<b>PC version.</b> Unconfirmed, but if it lands it brings a third spike: settings, performance, and later mods (official channels only).")}
</div>
<div class="grid g2" style="gap:5mm;margin-top:3mm">
 <div class="card"><h4>The long tail</h4><p style="margin:0">A guide that answers a real question ("how to make money fast in...") earns for months. A hot take earns for a day.</p></div>
 <div class="card"><h4>Spoiler discipline</h4><p style="margin:0">Label late-story videos in the title and thumbnail. Ending videos also risk removal under Rockstar's policy.</p></div>
</div>""", R, "04 · Calendar", 6)

products = page(f"""
{part(5, "Part five", "Sell your own products")}
<div class="grid" style="grid-template-columns:1.1fr 1fr;gap:7mm">
 <div>
  <h3>The product ladder</h3>
  <div class="steps">
   <div class="step"><div><b>$5 starter guide</b>A pre-launch or beginner guide. Gets your first buyers and your email list.</div></div>
   <div class="step"><div><b>$8 to $10 deep guide</b>Money, collectibles, side activities. Built from real play, updated free.</div></div>
   <div class="step"><div><b>$15 bundle</b>Everything, plus all future editions. Your best seller per hour of work.</div></div>
   <div class="step"><div><b>Services</b>Thumbnails, edits, voiceover for other GTA channels. Trades time for money, but it pays now.</div></div>
  </div>
 </div>
 <div>
  <div class="card hot" style="margin-bottom:4mm"><h3 style="color:#ffc94d">Ads vs one product</h3>
   <div style="display:grid;grid-template-columns:1fr auto;gap:2mm;font-size:10.5pt">
    <span>1M Shorts views (ads)</span><b style="font-family:Anton;font-size:16pt">$20–50</b>
    <span>100 guide sales at $4.99</span><b style="font-family:Anton;font-size:16pt;color:#ffc94d">~$430</b>
    <span>1,000 guide sales at $4.99</span><b style="font-family:Anton;font-size:16pt;color:#13d6c3">~$4,300</b></div>
   <p class="mute" style="font-size:7.5pt;margin:2mm 0 0">Payhip free plan: 5% + about 2.9% + $0.30 payment processing.</p></div>
  <div class="callout warn" data-icon="!"><b>Never sell Rockstar's work.</b> No game art, no traced official maps, no ripped audio or screenshots in paid products. Your words, your diagrams, your designs.</div>
 </div>
</div>
<hr class="rule">
<h3>Where to put the link</h3>
<p>Pinned comment · first line of every description · channel "Links" section · end screen of long videos · one line spoken in the video ("the full checklist is in the guide, linked below").</p>""", R, "05 · Products", 7)

sponsors = page(f"""
{part(6, "Part six", "Sponsors & affiliates")}
<div class="grid g2" style="gap:5mm;margin-bottom:6mm">
 <div class="card"><h4>Natural fits for GTA</h4><p style="margin:0">Storage drives (212 GB is a real problem), controllers, headsets, capture cards and gaming chairs. Recommend what you'd actually use.</p></div>
 <div class="card"><h4>Affiliate links</h4><p style="margin:0">Retailer programmes pay a small percentage of each sale. Small money, but it starts on day one and suits "best gear" videos.</p></div>
 <div class="card"><h4>Pitching a brand</h4><p style="margin:0">Send your average views per video over the last 30 days, audience countries and age, and two example videos. Ask for their budget before you name a price.</p></div>
 <div class="card"><h4>Twitch {REP}</h4><p style="margin:0">Affiliate bar lowered in June 2026: <b>25 followers, 4 hours, 4 days, 3 average viewers</b> within 30 days. Twitch reportedly opened sponsorships to Affiliates in Aug 2026.</p></div>
</div>
<div class="callout warn" data-icon="#"><b>Disclose every paid deal.</b> Tick YouTube's "includes paid promotion" box <i>and</i> say it out loud in the video. US FTC rules require clear disclosure of sponsorships and affiliate links, and other countries have similar rules.</div>
<div class="callout" data-icon="✕" style="margin-top:4mm"><b>Say no to:</b> gambling or "skins" sites, "free GTA" or "mod menu" offers, account-boosting, and anything promising money for nothing. They burn audience trust and can get your channel struck.</div>""", R, "06 · Sponsors", 8)

faceless = page(f"""
{part(7, "Part seven", "The faceless creator stack")}
<div class="grid g3" style="gap:4mm;margin-bottom:6mm">
 <div class="card"><h4>Capture</h4><p style="margin:0">Start with the console's built-in capture. <b>PS5:</b> Settings › Captures and Broadcasts. <b>Xbox:</b> Settings › Preferences › Capture &amp; share. Add a capture card later for longer recordings.</p></div>
 <div class="card"><h4>Voice</h4><p style="margin:0">Your own voice builds the most trust. A clean mic and a quiet room beat an expensive setup. If you use an AI voice, add real insight on top.</p></div>
 <div class="card"><h4>Edit</h4><p style="margin:0">Captions on every Short. A cut every 2 to 3 seconds in Shorts. Chapters in long videos, so people can jump straight to the answer.</p></div>
</div>
<h3>What makes faceless work</h3>
<div class="steps">
 <div class="step"><div><b>One promise per video</b>"The fastest money in the first hour, tested" beats "GTA VI tips #14".</div></div>
 <div class="step"><div><b>Proof on screen</b>Show the money counter, the map location, the setting. Viewers trust what they see.</div></div>
 <div class="step"><div><b>Original value</b>Your testing, your route, your verdict. That's what separates you from re-uploads and keeps you in YPP.</div></div>
 <div class="step"><div><b>Consistent look</b>Same thumbnail layout, colours and type, so returning viewers spot you instantly.</div></div>
</div>""", R, "07 · Faceless", 9)

weeks = [("Weeks 1–2", "Launch sprint", "1 long video + 2 Shorts a day. Starter guide live. Link in every description."),
         ("Weeks 3–4", "Find what works", "Check Studio: which videos hold viewers? Make three more like the best one."),
         ("Weeks 5–8", "Build the library", "Search-driven guides. Release the $8 to $10 deep guide. Start an email list."),
         ("Weeks 9–12", "Compound", "Bundle offer. Apply for lower-tier YPP when eligible. First brand pitches with real numbers.")]
plan = page(f"""
{part(8, "Part eight", "Your first 90 days")}
<div class="grid g2" style="gap:5mm;margin-bottom:6mm">
 {"".join(f'<div class="card{" hot" if i==0 else ""}"><span class="kicker">{w}</span><h4 style="margin:2mm 0">{t}</h4><p style="margin:0">{d}</p></div>' for i,(w,t,d) in enumerate(weeks))}
</div>
<h3>Track these four numbers weekly</h3>
<div class="grid g4" style="gap:3mm;text-align:center">
 <div class="card stat"><div class="big grad" style="font-size:22pt">AVD</div><div class="lbl">Avg view duration</div></div>
 <div class="card stat"><div class="big grad" style="font-size:22pt">CTR</div><div class="lbl">Thumbnail click rate</div></div>
 <div class="card stat"><div class="big grad" style="font-size:22pt">SUBS</div><div class="lbl">Per 1,000 views</div></div>
 <div class="card stat"><div class="big" style="font-size:22pt;color:#13d6c3">SALES</div><div class="lbl">Per 1,000 views</div></div>
</div>
<div class="callout" data-icon="$" style="margin-top:6mm"><b>Money admin.</b> Creator income is taxable. Keep a simple spreadsheet of every payment and expense, and set aside a share of each payout for tax. Speak to an accountant once it's real money.</div>""", R, "08 · 90 days", 10)

back = f"""<section class="page">
{scene(sky="linear-gradient(180deg,#05020f 0%,#0d0a3a 50%,#1b1f6b 75%,#13d6c3 88%,#ff2d8a 93%)",
       sun="linear-gradient(180deg,#9ffcf1,#13d6c3 40%,#ff2d8a)", sea="#07051d", horizon=92, sun_size=70, sun_top=82, palm_color="#05020f")}
<div class="inner" style="top:18mm">
 <div class="kicker">Sources · checked 9 November 2026</div>
 <h2 class="display grad" style="font-size:34pt;margin:3mm 0 6mm">Where the numbers come from</h2>
 <p class="mute" style="font-size:8.2pt;line-height:1.6;max-width:160mm">
 <b style="color:#fff">YouTube Partner Program</b>: requirements and the reported Feb 2027 change, via vidIQ, AIR Media-Tech and PPC Land. Revenue shares are from YouTube's YPP terms.<br>
 <b style="color:#fff">RPM estimates</b>: AIR Media-Tech (274-channel dataset) and creator-analytics blogs. These are estimates, not guarantees.<br>
 <b style="color:#fff">Rockstar video policy</b>: Rockstar Support, "Policy on posting copyrighted Rockstar Games material" (last updated 10 Jan 2025).<br>
 <b style="color:#fff">YouTube gaming-violence update (Sept 2026)</b>: as reported by Dexerto, Outlook Respawn and Northeast Times.<br>
 <b style="color:#fff">Twitch Affiliate</b>: thresholds as reported by creator guides citing Twitch's Help Center (Oct 2026).<br>
 <b style="color:#fff">Storefront fees</b>: platform comparisons by Sellfy and others. Check each platform's pricing page.</p>
 <div class="callout" data-icon="!" style="max-width:160mm;margin-top:6mm"><b>Educational only. Not financial or legal advice.</b> No income is promised or implied. Platform rules change. Check the official pages before you act.</div>
 <p class="mute" style="font-size:7.6pt;max-width:160mm;margin-top:5mm"><i>Grand Theft Auto</i> and <i>GTA</i> are trademarks of Take-Two Interactive, used only to identify the game. Not affiliated with Rockstar Games, Take-Two, YouTube, Google or Twitch.</p>
</div></section>"""

render([cover, reality, money_map, ypp, rules, calendar, products, sponsors, faceless, plan, back],
       pathlib.Path(__file__).with_name("Creator-Playbook.pdf"), "night")
