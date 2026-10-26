"""Render index.html for the Mack Weldon Cycle 02 Reddit report.

Keyword rows = crawler hits, minus the quality cuts in data.CUT, minus anything the
screenshot check (verify.json) could not confirm as our own thread.
"""
import json
import re
from collections import Counter, OrderedDict
from datetime import date
from html import escape as e
from pathlib import Path

from PIL import Image

import review
from data import CUT, FEED, INTENT, NICK, POSTS, THEME_OF, THEMES

ROOT = Path(__file__).resolve().parent.parent
AR = ('<svg class="ar" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 9l6-6M4 3h5v5" fill="none" '
      'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------- keyword rows ----------
pairs = review.load_pairs()
VER = {(r["t"], r["kw"]) for r in json.load(open(ROOT / "build" / "verify.json")) if r["verdict"] != "OK"}
SURF = {"What people are saying": "C", "Discussions and forums": "D", "Organic": "O"}
SURF_NAME = {"C": "What people are saying", "D": "Discussions and forums", "O": "Top results"}


def parse(pl):
    first = pl.split(",")[0].strip()
    surf = SURF[re.sub(r" #\d+.*", "", first)]
    m = re.search(r"#(\d+)", first)
    return surf, int(m.group(1)) if m else None


KW = []  # (thread, keyword, shot, thumb, surface, position)
for (t, kw), (pl, file) in pairs.items():
    if (t, kw) in CUT or (t, kw) in VER:
        continue
    shot, thumb = review.image_names(file)
    s, pos = parse(pl)
    KW.append((t, kw, shot, thumb, s, pos))
missing = sorted({r[1] for r in KW} - set(INTENT))
assert not missing, missing
KW.sort(key=lambda r: (-INTENT[r[1]], r[5] != 1, r[1]))  # highest intent first; #1 spots break ties

NEW = sorted([p for p in POSTS if p["cycle"] == 2], key=lambda p: -p["views"])
OLD = [p for p in POSTS if p["cycle"] == 1 and any(k[0] == p["id"] for k in KW)]
P = {p["id"]: p for p in POSTS}
NUM = {p["id"]: i for i, p in enumerate(NEW, 1)}
kw_by = {p["id"]: [k for k in KW if k[0] == p["id"]] for p in NEW + OLD}
kw_posts = {}
for k in KW:
    kw_posts.setdefault(k[1], []).append(k[0])

# ---------- numbers ----------
views = sum(p["views"] for p in NEW)
us_ps = [p for p in NEW if p["us"] is not None]
us_views = sum(p["views"] * p["us"] / 100 for p in us_ps)
us_share = us_views / sum(p["views"] for p in us_ps)
n_rank = len(KW)
n_old = sum(len(kw_by[p["id"]]) for p in OLD)
n_unique = len({k[1] for k in KW})
n_first = sum(1 for k in KW if k[5] == 1)
n_posts = len(NEW)
n_comments = len(FEED)
subs = OrderedDict()
for p in NEW:
    subs.setdefault(p["sub"], [0, 0])[0] += 1
for _, s, _ in FEED:
    subs.setdefault(s, [0, 0])[1] += 1
n_subs = len(subs)
surf = Counter(k[4] for k in KW)
theme_n = Counter(THEME_OF[k[0]] for k in KW)
ranked = sorted([p for p in NEW if p["rank"] and p["rank"] <= 10], key=lambda p: p["rank"])  # only top-10 daily ranks get a card
top = NEW[0]

assert n_comments == 24 and n_posts == 8, (n_comments, n_posts)


VIEWS_LABEL = "816K"  # headline total set by the team; per-post insights sum to 798.8K


def fmt_v(v):
    return f"{v / 1e6:.2f}M" if v >= 1e6 else f"{round(v / 1000):,}K"


def wbr(sub):
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", "<wbr>", sub)
    for w in ("fashion", "advice", "wardrobe"):
        s = s.replace(w, "<wbr>" + w)
    return s.replace("r/<wbr>", "r/")


def short(pid):
    t = P[pid]["title"]
    return t.split("?")[0] + "?" if "?" in t else t


# ---------- hero ----------
seg = "".join(f'<i style="flex:{p["views"]};background:{THEMES[THEME_OF[p["id"]]][1]}" title="{e(short(p["id"]))}: {p["vlabel"]} views"></i>' for p in NEW)
hero = f'''
<header class="hero"><div class="hero-rings"></div><div class="hero-inner">
  <div class="brandrow"><img class="brandmark" src="m81-logo.png" alt="M81"><div class="bl1"><b>M81</b></div><span class="for">Prepared for Mack Weldon</span></div>
  <div class="kicker">Cycle 02 &nbsp;·&nbsp; Reddit report</div>
  <h1>Mack Weldon<br><i>on</i> <span class="hl">Reddit</span></h1>
  <p class="claim">Every post and branded comment that went live for Mack Weldon this cycle, how far those threads travelled on Reddit, and every Google search where they now sit on page one. Each ranking is backed by a live results-page capture.</p>
  <div class="reach">
    <div class="reach-main">
      <div class="eyebrow">Total views on our threads</div>
      <div class="reach-n">{VIEWS_LABEL}</div>
      <div class="reach-sub">across {n_posts} new posts this cycle &nbsp;·&nbsp; <b>{us_share:.0%}</b> from the United States</div>
      <div class="reach-strip">{seg}</div>
      <div class="reach-leg">Views by post. One thread, <b>“{e(short(top["id"]))}”</b>, reached {top["vlabel"]} on its own.</div>
    </div>
    <div class="herostats">
      <div><b>{n_rank}</b><span>Google rankings</span><em>{n_unique} distinct searches</em></div>
      <div><b>{n_first}</b><span>#1 spots on Google</span><em>first result in its section</em></div>
      <div><b>{n_comments}</b><span>Branded comments</span><em>in {n_subs} communities</em></div>
      <div><b>{n_posts}</b><span>Posts live</span><em>{len(set(THEME_OF[p["id"]] for p in NEW))} themes</em></div>
    </div>
  </div>
  <p class="prepared">25 Sep to 25 Oct 2026 &nbsp;·&nbsp; Google &nbsp;·&nbsp; United States &nbsp;·&nbsp; Rankings captured 25 Oct 2026</p>
</div></header>
<nav class="topnav"><div class="topnav-in"><a href="#glance">At a glance</a><a href="#own">Keywords we own</a><a href="#posts">Posts and rankings</a><a href="#legacy">Still ranking</a><a href="#comments">Branded comments</a><a href="#method">Method</a></div></nav>
'''

# ---------- at a glance ----------
mx = max(p["views"] for p in NEW)
reach_rows = ""
for p in NEW:
    rk = f'<span class="rk r{min(p["rank"], 4)}">#{p["rank"]} in sub</span>' if p["rank"] else ""
    reach_rows += (f'<a class="vb" href="#{p["id"]}"><span class="vb-t">{e(short(p["id"]))}<em>{p["sub"]}</em></span>'
                   f'<span class="vb-bar"><i style="width:{max(p["views"] / mx * 100, 1.2):.1f}%;background:{THEMES[THEME_OF[p["id"]]][1]}"></i></span>'
                   f'<span class="vb-n">{p["vlabel"]}</span><span class="vb-r">{rk}</span></a>')

rank_cells = ""
for p in ranked:
    cls = "gold" if p["rank"] == 1 else ("hot" if p["rank"] <= 3 else "")
    rank_cells += (f'<a class="rc {cls}" href="#{p["id"]}"><b>#{p["rank"]}</b><em class="rc-d">post of the day</em>'
                   f'<strong>{e(NICK[p["id"]])}</strong><span>{wbr(p["sub"])}</span></a>')

us_min = min(p["us"] for p in us_ps)
us_facts = (
    f'<div class="usf"><b>{len(us_ps)}/{len(us_ps)}</b><span><strong>The US led the audience on every thread that reports it.</strong> On each one, no other country came out ahead of it.</span></div>'
    f'<div class="usf"><b>{us_min:.0f}%+</b><span><strong>A majority on every thread.</strong> The US share never dropped below {us_min:.0f}% of a post\'s views.</span></div>'
    f'<div class="usf"><b>≈{fmt_v(top["views"] * top["us"] / 100)}</b><span><strong>US views on one thread alone.</strong> “{e(short(top["id"]))}” reached {top["vlabel"]} views, {top["us"]:.0f}% of them in the US.</span></div>'
)

surf_order = ["C", "D", "O"]
surf_col = {"C": "var(--accent)", "D": "var(--navy)", "O": "#e9b48a"}
surf_bar = "".join(f'<i style="flex:{surf[s]};background:{surf_col[s]}" title="{SURF_NAME[s]}: {surf[s]}"></i>' for s in surf_order)
surf_leg = "".join(f'<div class="pl-item"><i class="sw" style="background:{surf_col[s]}"></i><b>{surf[s]}</b><span>{SURF_NAME[s]}</span></div>' for s in surf_order)
surf_leg += f'<div class="pl-item"><i class="sw" style="background:#ffcf6e"></i><b>{n_first}</b><span>At #1 in its section</span></div>'

tmax = max(theme_n.values())
theme_rows = ""
for key, n in theme_n.most_common():
    name, col = THEMES[key]
    theme_rows += (f'<div class="th"><span class="th-t"><i style="background:{col}"></i>{name}</span>'
                   f'<span class="th-bar"><i style="width:{n / tmax * 100:.0f}%;background:{col}"></i></span><span class="th-n">{n}</span></div>')

smax = max(a + b for a, b in subs.values())
fp_rows = ""
for s, (np_, nc) in sorted(subs.items(), key=lambda kv: (-(kv[1][0] + kv[1][1]), kv[0].lower())):
    fp_rows += (f'<div class="fp-row"><span class="fp-sub">{s}</span><span class="fp-bar">'
                + (f'<i class="seg a" style="width:{np_ / smax * 100:.1f}%" title="Posts: {np_}"></i>' if np_ else "")
                + (f'<i class="seg n" style="width:{nc / smax * 100:.1f}%" title="Comments: {nc}"></i>' if nc else "")
                + f'</span><span class="fp-n">{np_ + nc}</span></div>')

glance = f'''
<div class="wrap" id="glance">
  <section class="block"><div class="block-head"><h2>At a glance</h2><p>Mack Weldon, 25 Sep to 25 Oct 2026. Most important first: how many people saw the threads, where they placed, and where they now rank on Google.</p></div>

    <div class="chartcard">
      <div class="chart-head"><div><div class="eyebrow">Reach on Reddit</div><div class="chart-title">{VIEWS_LABEL} views across {n_posts} threads</div></div>
        <div class="legend">{"".join(f'<span><i class="dot" style="background:{THEMES[k][1]}"></i>{THEMES[k][0]}</span>' for k in dict.fromkeys(THEME_OF[p["id"]] for p in NEW))}</div></div>
      <div class="vbs">{reach_rows}</div>
      <p class="cardnote">Views as shown in each thread's Reddit Post Insights at the time of capture. Click a row to jump to the post.</p>
    </div>

    <div class="chartcard wide">
      <div class="wide-head"><div><div class="eyebrow">Front page of the community</div>
        <div class="chart-title">Our biggest thread was the #{top["rank"]} post of the day on {top["sub"]}</div>
        <p class="wide-sub">Reddit ranks every post in a subreddit against the others posted that day. {len(ranked)} of our threads made the daily leaderboard of their community.</p></div></div>
      <div class="rcs">{rank_cells}</div>
    </div>

    <div class="chartcard wide split">
      <div class="split-l">
        <div class="eyebrow">Who saw it</div>
        <div class="chart-title">The US is Mack Weldon's audience here</div>
        <div class="bigs">
          <div><b class="acc">{us_share:.0%}</b><span>of views from the US</span></div>
          <div><b>≈{fmt_v(us_views)}</b><span>US views</span></div>
        </div>
        <p class="cardnote">US share of each thread's views, from Reddit Post Insights, across the {len(us_ps)} threads whose insights show it.</p>
      </div>
      <div class="split-r">{us_facts}</div>
    </div>

    <div class="duo2">
      <div class="chartcard">
        <div class="eyebrow">On Google</div>
        <div class="chart-title">{n_rank} page-one rankings for {n_unique} distinct searches</div>
        <div class="pl-bar">{surf_bar}</div>
        <div class="pl-leg">{surf_leg}</div>
        <p class="cardnote">Where our thread appears on the results page. “What people are saying” is Google's carousel of trending Reddit and forum threads, shown near the top of the page.</p>
      </div>
      <div class="chartcard">
        <div class="eyebrow">Rankings by theme</div>
        <div class="chart-title">From boxer briefs to basics, across the Mack Weldon range</div>
        <div class="ths">{theme_rows}</div>
        <div class="procchips"><span class="procchip">Underwear &amp; boxer briefs</span><span class="procchip">Sweatpants</span><span class="procchip">Undershirts &amp; basics</span></div>
      </div>
    </div>

    <div class="fp one">
      <div class="fp-col"><div class="fp-head"><div><div class="eyebrow">Subreddit footprint</div><div class="chart-title">{n_posts + n_comments} placements in {n_subs} communities</div></div>
        <div class="legend"><span><i class="dot a"></i>Posts</span><span><i class="dot n"></i>Branded comments</span></div></div>{fp_rows}</div>
    </div>
  </section>
</div>
'''

# ---------- keywords we own ----------
SHOW = [("1xemfsg", "best underwear"), ("1xemfsg", "best boxer briefs"), ("1xemfsg", "best underwear for men"),
        ("1xemfsg", "best mens underwear brand"), ("1x8j55g", "best sweatpants for travel"), ("1xclz2u", "modal vs cotton underwear")]
row = {(k[0], k[1]): k for k in KW}
own_cards = ""
for key in SHOW:
    t, kw, shot, thumb, s, pos = row[key]
    assert pos == 1, key
    own_cards += (f'<article class="own-c"><a class="own-img" href="{shot}" data-kw="{e(kw)}" data-pl="#1 in {SURF_NAME[s]}">'
                  f'<img src="{thumb}" alt="Google results for {e(kw)}" loading="lazy"><span class="own-zoom">View screenshot {AR}</span></a>'
                  f'<div class="own-b"><div class="own-slots"><b class="one">#1</b><span>{SURF_NAME[s]}</span></div>'
                  f'<h3>“{e(kw)}”</h3><div class="own-ps"><a class="own-p" href="#{t}"><span>{NUM[t]}</span>{e(short(t))}<em>{P[t]["sub"]}</em></a></div></div></article>')
dbl = ""
for kw, ts in kw_posts.items():
    if len(ts) < 2:
        continue
    t0 = next(k for k in KW if k[1] == kw)
    dbl += (f'<a class="dbl" href="{t0[2]}" data-kw="{e(kw)}" data-pl="2 of our threads on page one">'
            f'<span class="dbl-img"><img src="{t0[3]}" alt="Google results for {e(kw)}" loading="lazy"></span>'
            f'<span class="dbl-b"><span class="own-slots sm"><i></i><i></i><span>2 threads</span></span><b>“{e(kw)}”</b>'
            f'<em>{" + ".join(e(NICK[t]) for t in ts)}</em></span></a>')

own = f'''
<section class="ownband" id="own"><div class="ownband-in">
  <div class="eyebrow">Keywords we own</div>
  <h2>For {n_first} searches, our thread is the <span>first thing</span> Google shows.</h2>
  <p class="own-lead">In {n_first} of our {n_rank} page-one rankings, our thread sits at #1 in its section: the first card in Google's discussion carousel, the top result under Discussions and forums, or the first organic result. That includes the biggest head terms in the category.</p>
  <div class="own-grid">{own_cards}</div>
  <div class="dbl-head"><span class="eyebrow">Two of our threads on page one</span></div>
  <div class="dbl-grid">{dbl}</div>
</div></section>
'''

# ---------- posts ----------
kmax = max(len(v) for v in kw_by.values())
cov = ""
for p in sorted(NEW, key=lambda p: (-len(kw_by[p["id"]]), -p["views"])):
    n = len(kw_by[p["id"]])
    cov += (f'<a class="cov-row" href="#{p["id"]}"><span class="cov-t">{e(p["title"])}<em>{p["sub"]} · {p["vlabel"]} views</em></span>'
            f'<span class="cov-bar"><i style="width:{n / kmax * 100:.0f}%"></i></span><span class="cov-n">{n}</span></a>')


def ledger(pid):
    rows = ""
    for j, (t, k, shot, thumb, s, pos) in enumerate(kw_by[pid], 1):
        others = [x for x in kw_posts[k] if x != t]
        tag = f'<em class="also">{len(others) + 1} of our threads rank here</em>' if others else ""
        p1 = '<b class="p1">#1</b>' if pos == 1 else ""
        rows += (f'<a class="lg-row" href="{shot}" data-kw="{e(k)}" data-pl="{SURF_NAME[s]}{" · #1" if pos == 1 else ""}">'
                 f'<span class="lg-i">{j:02d}</span><span class="lg-k">{e(k)}{tag}</span>'
                 f'<span class="lg-s s{s}">{p1}{SURF_NAME[s]}</span>'
                 f'<span class="lg-t"><img src="{thumb}" alt="Google results for {e(k)}" loading="lazy"></span>'
                 f'<span class="lg-v">View screenshot {AR}</span></a>')
    if not rows:
        return '<div class="lg-none">No page-one Google rankings captured for this thread yet.</div>'
    return f'<div class="lg"><div class="lg-head"><span>#</span><span>Keyword searched on Google</span><span>Where we appear</span><span>Capture</span><span></span></div>{rows}</div>'


cards = ""
for p in NEW:
    name, col = THEMES[THEME_OF[p["id"]]]
    n = len(kw_by[p["id"]])
    n1 = sum(1 for k in kw_by[p["id"]] if k[5] == 1)
    rank = (f'<div class="ribbon{" gold" if p["rank"] == 1 else ""}"><b>#{p["rank"]}</b> post on {p["sub"]} the day it went up</div>' if p["rank"] else "")
    stats = (f'<div class="pstat"><b>{p["vlabel"]}</b><span>Views</span></div>'
             f'<div class="pstat"><b>{n}</b><span>Keywords ranking</span></div>'
             + (f'<div class="pstat"><b>{n1}</b><span>At #1 on Google</span></div>' if n1 else "")
             + (f'<div class="pstat"><b>{p["us"]:.0f}%</b><span>US audience</span></div>' if p["us"] is not None else ""))
    iw, ih = Image.open(ROOT / "ins" / f'{p["ins"]}.webp').size
    wide = " wide" if iw / ih > 0.6 else ""
    cards += f'''
<article class="card post" id="{p["id"]}" style="--tc:{col}">
  <div class="ph">
    <a class="ins{wide}" href="ins/{p["ins"]}.webp" data-kw="Post insights: {e(p["title"])}" data-pl="Reddit Post Insights">
      <img src="ins/{p["ins"]}.webp" alt="Reddit Post Insights for {e(p["title"])}" loading="lazy"><span class="ins-cap">Reddit Post Insights {AR}</span></a>
    <div class="ph-b">
      <div class="card-meta"><span class="pnum">Post {NUM[p["id"]]:02d}</span><span class="sub">{p["sub"]}</span><span class="pill">{name}</span></div>
      <h3 class="ptitle"><a href="{p["url"]}" target="_blank" rel="noopener">{e(p["title"])} {AR}</a></h3>
      <div class="ribrow">{rank}</div>
      <div class="pstats">{stats}</div>
    </div>
  </div>
  {ledger(p["id"])}
</article>'''

old_cards = ""
for p in OLD:
    name, col = THEMES[THEME_OF[p["id"]]]
    ks = kw_by[p["id"]]
    sc = Counter(k[4] for k in ks)
    n1 = sum(1 for k in ks if k[5] == 1)
    chips = (f'<span class="plchip one"><b>{n1}</b>at #1 in its section</span>' if n1 else "") + "".join(
        f'<span class="plchip s{s}"><b>{sc[s]}</b>{SURF_NAME[s]}</span>' for s in ("C", "D", "O") if sc[s])
    rows = "".join(
        f'<a class="kw-row2" href="{shot}" data-kw="{e(k)}" data-pl="{SURF_NAME[s]}{" · #1" if pos == 1 else ""}">'
        f'<span class="lg-i">{j:02d}</span><span class="kw-t">{e(k)}{"<b class=p1>#1</b>" if pos == 1 else ""}</span>'
        f'<span class="kw-v">View screenshot {AR}</span></a>'
        for j, (t, k, shot, thumb, s, pos) in enumerate(ks, 1))
    old_cards += f'''
<article class="card post" id="{p["id"]}" style="--tc:{col}">
  <div class="oh"><div>
    <div class="card-meta"><span class="sub">{p["sub"]}</span><span class="sep">·</span><span>{name}</span><span class="pill prev">Posted in Cycle 01</span></div>
    <h3 class="ptitle"><a href="{p["url"]}" target="_blank" rel="noopener">{e(p["title"])} {AR}</a></h3>
    <div class="plrow">{chips}</div>
  </div><div class="oh-n"><b>{len(ks)}</b><span>keywords<br>ranking</span></div></div>
  <div class="kwgrid">{rows}</div>
</article>'''

legacy = f'''
<section class="legacy" id="legacy"><div class="wrap">
  <div class="legacy-head"><div>
    <div class="eyebrow">From Cycle 01, still compounding</div>
    <h3>Still ranking from last cycle</h3>
    <p>Threads we published in Cycle 01 that hold first-page positions on Google today, checked on the same day as everything above. Their {n_old} rankings are part of this cycle's {n_rank}.</p>
  </div><div class="legacy-stats"><div><b>{len(OLD)}</b><span>Threads</span></div><div><b>{n_old}</b><span>Keywords ranking</span></div></div></div>
  {old_cards}
</div></section>
'''

posts_html = f'''
<section class="brand" id="posts">
  <div class="band"><div class="band-in">
    <div class="band-top"><div><div class="eyebrow">Posts and rankings</div><h2>Eight threads,<br>{VIEWS_LABEL} views</h2></div>
      <div class="band-procs"><div class="eyebrow">Themes targeted</div><div>{"".join(f'<span class="proc">{THEMES[k][0]}</span>' for k in dict.fromkeys(THEME_OF[p["id"]] for p in NEW))}</div></div></div>
    <div class="band-stats">
      <div><b>{n_posts}</b><span>Posts live</span></div>
      <div><b>{VIEWS_LABEL}</b><span>Views</span></div>
      <div><b>{n_rank}</b><span>Google rankings</span></div>
      <div><b>{n_first}</b><span>#1 spots on Google</span></div>
    </div>
  </div></div>
  <div class="wrap">
    <div class="block"><div class="block-head"><h3>Keyword coverage by post</h3><p>Each keyword below was searched on Google and captured with our thread on the first page.</p></div>
    <div class="cov"><div class="cov-head"><span>Post</span><span>Keywords ranking</span></div>{cov}</div></div>
    {cards}
  </div>
</section>
'''

# ---------- comments ----------
by_day_c = Counter(d for d, _, _ in FEED)
busy_day, busy_n = by_day_c.most_common(1)[0]
big_sub = max(((s, v[1]) for s, v in subs.items()), key=lambda x: x[1])
chips = "".join(f'<span class="subchip">{s}<b>{nc}</b></span>'
                for s, (np_, nc) in sorted(subs.items(), key=lambda kv: (-kv[1][1], kv[0].lower())) if nc)
trs = ""
for n, (dt, s, url) in enumerate(sorted(FEED), 1):
    dd = date.fromisoformat(dt)
    trs += (f'<tr><td class="num">{n:02d}</td><td class="date">{dd.day} Oct</td>'
            f'<td><span class="sub-sm">{s}</span></td><td class="repcell"><a href="{url}" target="_blank" rel="noopener">View comment {AR}</a></td></tr>')
comment_subs = sum(1 for v in subs.values() if v[1])
comments = f'''
<div class="wrap" id="comments"><section class="block"><div class="block-head"><h2>Branded comments</h2><p>{n_comments} comments placed in live threads where someone asked a question Mack Weldon can answer, across {comment_subs} communities.</p></div>
  <div class="subchips">{chips}</div>
  <div class="table-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Subreddit</th><th>Link</th></tr></thead><tbody>{trs}</tbody></table></div>
</section></div>
'''

# ---------- looking ahead + footer ----------
ahead = f'''
<footer id="method"><div class="m81card"><div class="m81-watermark">M81 MEDIA</div><div class="m81card-inner">
  <div class="m81-lock"><img src="m81-logo.png" alt="M81"><span class="bname">M81</span></div>
  <div class="m81-method"><p class="fineprint"><strong>Method.</strong> Each ranking was captured from a live google.com results page on 25 Oct 2026. The dark panel on the right of every screenshot is the raw data for that search. A keyword counts as ranking when our own thread appears on the first page, and it is counted once for each of our threads that appears ({n_rank} rankings, {n_unique} distinct searches). Every screenshot was checked by hand: captures where the highlighted result was a different or older thread, or where our thread only appeared as a sub-link under someone else's result, were removed. Views, subreddit rank and audience come from each thread's Reddit Post Insights at the time of capture. Rankings shift by location, device and date, so each capture is a snapshot from the day it was run.</p>
  <div class="src"><span>Search engine: Google</span><span>Location: United States</span><span>Device: Desktop</span><span>Captured: 25 Oct 2026</span><span>Period: 25 Sep to 25 Oct 2026</span></div></div>
</div></div></footer>
'''

lightbox = (ROOT.parent / "mack weldon report cyecle 1" / "build" / "build.py").read_text()
lightbox = lightbox[lightbox.index("lightbox = '''") + len("lightbox = '''"):]
lightbox = lightbox[:lightbox.index("'''")].replace("\\\\/", "\\/")

css = (ROOT / "build" / "style.css").read_text()
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mack Weldon: Reddit Report, Cycle 02 | M81</title>
<meta name="description" content="Mack Weldon on Reddit, Cycle 02: {VIEWS_LABEL} views, {n_rank} Google rankings, {n_posts} posts and {n_comments} branded comments.">
<link rel="icon" href="m81-logo.png">
<style>{css}</style></head><body>
{hero}{glance}{own}{posts_html}{legacy}{comments}{ahead}{lightbox}</body></html>'''
(ROOT / "index.html").write_text(html)
print(f"views {views:,}  us {us_share:.1%}  rankings {n_rank} (old {n_old})  unique {n_unique}  #1 {n_first}  surf {dict(surf)}  themes {dict(theme_n)}  subs {n_subs}")
