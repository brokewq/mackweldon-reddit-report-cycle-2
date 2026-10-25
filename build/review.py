"""Build review.html: every captured keyword with a keep/cut call, for the user to check
before the cycle 02 report is built. Also writes shots/ and thumbs/ used by the report."""
import glob
import json
from html import escape as e
from pathlib import Path

from PIL import Image

from data import CUT, DROP, OVERRIDE, POSTS, SERP_DIR

ROOT = Path(__file__).resolve().parent.parent
P = {p["id"]: p for p in POSTS}


def load_pairs():
    pairs = {}
    for f in sorted(glob.glob(f"{SERP_DIR}/data/b*.data.txt")):
        s = open(f).read()
        j = json.loads(s[s.index("=", s.index("SERP_PROFILES[")) + 1:].rstrip().rstrip(";"))
        for r in j["results"]:
            for h in r["hits"]:
                tid = h["url"].split("/comments/")[1].split("/")[0]
                pairs.setdefault((tid, r["kw"].strip().lower()), (h["placement"], h["file"]))
    for k in DROP:
        pairs.pop(k)
    pairs.update(OVERRIDE)
    return pairs


def red_box(im):
    w, h = im.size
    px = im.convert("RGB").load()
    xs, ys = [], []
    for y in range(0, h, 3):
        for x in range(0, int(w * 0.54), 3):
            r, g, b = px[x, y]
            if r > 190 and g < 80 and b < 80:
                xs.append(x); ys.append(y)
    if len(xs) < 40:
        return None
    xs.sort(); ys.sort()
    k = max(1, len(xs) // 200)
    return xs[k], ys[k], xs[-k - 1], ys[-k - 1]


def crop_16x10(im, box):
    w, h = im.size
    x0, y0, x1, y1 = box
    pad = int(w * 0.03)
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)
    bw, bh = x1 - x0, y1 - y0
    tw = max(bw, int(bh * 1.6)); th = int(tw / 1.6)
    if th < bh:
        th = bh; tw = int(th * 1.6)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    L = min(max(0, cx - tw // 2), max(0, w - tw)); T = min(max(0, cy - th // 2), max(0, h - th))
    return im.crop((L, T, min(w, L + tw), min(h, T + th)))


def save(im, path, width, q):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(path, "WEBP", quality=q, method=6)


def image_names(file):
    stem = file.replace("/", "__").rsplit(".", 1)[0]
    return f"shots/{stem}.webp", f"thumbs/{stem}.webp"


def build_images(pairs):
    for (tid, kw), (pl, file) in pairs.items():
        shot, thumb = image_names(file)
        if (ROOT / thumb).exists():
            continue
        src = ROOT / file if (ROOT / file).exists() else Path(SERP_DIR) / file
        im = Image.open(src)
        save(im, ROOT / shot, 2400, 84)
        box = red_box(im)
        t = crop_16x10(im, box) if box else im.crop((0, 0, int(im.width * .54), int(im.width * .54 / 1.6)))
        save(t, ROOT / thumb, 720, 80)


if __name__ == "__main__":
    pairs = load_pairs()
    unknown = {t for t, _ in pairs} - set(P)
    assert not unknown, unknown
    stale = set(CUT) - set(pairs)
    assert not stale, stale
    build_images(pairs)

    LABEL = {"WRONG": "Screenshot shows a different thread", "SITELINK": "Only a sub-link under an older thread",
             "UNCLEAR": "Screenshot can't confirm it"}
    VER = {}
    for r in json.load(open(ROOT / "build" / "verify.json")):
        if r["verdict"] != "OK":
            seen = ", ".join(x for x in (r.get("boxed_title"), r.get("boxed_sub"), r.get("boxed_age")) if x and x != "unknown")
            VER[(r["t"], r["kw"])] = f'{LABEL[r["verdict"]]}' + (f': {seen}' if seen and r["verdict"] != "UNCLEAR" else f': {r.get("note","")[:140]}' if r["verdict"] == "UNCLEAR" else "")
    CUTS = {**CUT, **VER}

    kw_threads = {}
    for tid, kw in pairs:
        if (tid, kw) not in VER:
            kw_threads.setdefault(kw, []).append(tid)

    order = [p for p in POSTS if p["cycle"] == 2] + [p for p in POSTS if p["cycle"] == 1]
    order = sorted([p for p in order if p["cycle"] == 2], key=lambda p: -p["views"]) + [p for p in order if p["cycle"] == 1]
    sections, total, kept = "", 0, 0
    for n, p in enumerate(order, 1):
        rows = sorted([(kw, v) for (tid, kw), v in pairs.items() if tid == p["id"]],
                      key=lambda x: ((p["id"], x[0]) in CUTS, x[0]))
        if not rows:
            continue
        k = sum(1 for kw, _ in rows if (p["id"], kw) not in CUTS)
        total += len(rows); kept += k
        trs = ""
        for kw, (pl, file) in rows:
            shot, thumb = image_names(file)
            reason = CUTS.get((p["id"], kw)); flag = (p["id"], kw) in VER
            others = [t for t in kw_threads.get(kw, []) if t != p["id"]]
            also = f'<em class="also">{len(others) + 1} of our threads rank here</em>' if others else ""
            trs += (f'<tr class="{"cut" if reason else "keep"}" data-t="{p["id"]}" data-kw="{e(kw)}" data-def="{0 if reason else 1}">'
                    f'<td><label class="tg"><input type="checkbox" {"" if reason else "checked"}><span></span></label></td>'
                    f'<td class="kw">{e(kw)}{also}<span class="why{" flag" if flag else ""}">{e(reason or "")}</span></td>'
                    f'<td class="pl">{e(pl)}</td>'
                    f'<td><a href="../{shot}" class="th" data-cap="{e(kw)}"><img loading="lazy" src="../{thumb}" alt=""></a></td></tr>')
        ins = (f'<a class="insb" href="../ins/{p["ins"]}.webp" data-cap="Post insights: {e(p["title"])}"><img src="../ins/{p["ins"]}.webp" alt=""></a>'
               if p["ins"] else '<div class="insb none">Cycle 01 thread<br>no new insights</div>')
        meta = (f'{p["vlabel"]} views' + (f' · #{p["rank"]} on {p["sub"]} that day' if p["rank"] else "")
                if p["views"] else "Cycle 01 thread, new rankings this cycle")
        sections += f'''
<section class="post" id="{p["id"]}">
  <div class="ph">{ins}<div>
    <div class="meta"><span class="num">{"Post %02d" % n if p["cycle"] == 2 else "Cycle 01"}</span><span class="sub">{p["sub"]}</span></div>
    <h2><a href="{p["url"]}" target="_blank" rel="noopener">{e(p["title"])}</a></h2>
    <div class="pm">{meta}</div>
    <div class="cnt"><b class="k">{k}</b> kept of <b>{len(rows)}</b> captured</div>
  </div></div>
  <table><thead><tr><th>Keep</th><th>Keyword</th><th>Where it ranks</th><th>Screenshot</th></tr></thead><tbody>{trs}</tbody></table>
</section>'''

    css = (ROOT / "build" / "review.css").read_text()
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Keyword Review, Cycle 02</title><style>{css}</style></head><body>
<header><div class="in">
  <div class="eyebrow">Mack Weldon · Cycle 02 · keyword review</div>
  <h1>Pick the keywords for the report</h1>
  <p>Every keyword the crawler found our threads ranking for on 25 Oct 2026. I pre-marked each one: <b>kept</b> if it reads like a real, buying-intent search, <b>cut</b> if it echoes the post title, is too contrived to be a real search, duplicates a kept keyword, or has no shopping intent. Flip any toggle, then press <b>Copy my changes</b> and paste the result back to me.</p>
  <div class="stats"><div><b id="sk">{kept}</b><span>Keyword rankings kept</span></div><div><b id="st">{total}</b><span>Captured in total</span></div><div><b id="su">0</b><span>Distinct searches kept</span></div><div><b id="sc">0</b><span>Your changes</span></div></div>
  <div class="bar"><div class="seg"><button data-f="all" class="on">All</button><button data-f="keep">Kept</button><button data-f="cut">Cut</button></div>
    <button id="copy" class="pri">Copy my changes</button><button id="reset">Reset to my picks</button><span id="msg"></span></div>
</div></header>
<main>{sections}</main>
<div class="lb" id="lb" hidden><figure><figcaption id="lbc"></figcaption><img id="lbi" alt=""></figure></div>
<script>
const KEY='mw-c2-review';
const rows=[...document.querySelectorAll('tbody tr')];
let saved={{}}; try{{saved=JSON.parse(localStorage.getItem(KEY)||'{{}}')}}catch(e){{}}
rows.forEach(r=>{{const id=r.dataset.t+'|'+r.dataset.kw; if(id in saved) r.querySelector('input').checked=saved[id];}});
function sync(){{
  let k=0,c=0,u=new Set(); const s={{}};
  rows.forEach(r=>{{const on=r.querySelector('input').checked, d=r.dataset.def==='1';
    r.className=on?'keep':'cut'; if(on){{k++;u.add(r.dataset.kw)}} if(on!==d){{c++; s[r.dataset.t+'|'+r.dataset.kw]=on}} r.classList.toggle('chg',on!==d);}});
  document.querySelectorAll('section.post').forEach(sec=>{{sec.querySelector('.k').textContent=sec.querySelectorAll('tr.keep').length}});
  sk.textContent=k; su.textContent=u.size; sc.textContent=c;
  try{{localStorage.setItem(KEY,JSON.stringify(s))}}catch(e){{}}
  filter();
}}
let F='all'; function filter(){{rows.forEach(r=>r.hidden=F!=='all'&&!r.classList.contains(F))}}
document.querySelectorAll('.seg button').forEach(b=>b.onclick=()=>{{F=b.dataset.f; document.querySelectorAll('.seg button').forEach(x=>x.classList.toggle('on',x===b)); filter()}});
rows.forEach(r=>r.querySelector('input').onchange=sync);
reset.onclick=()=>{{rows.forEach(r=>r.querySelector('input').checked=r.dataset.def==='1'); sync()}};
copy.onclick=async()=>{{
  const add=[],cut=[]; rows.forEach(r=>{{if(!r.classList.contains('chg'))return; const t=document.getElementById(r.dataset.t).querySelector('h2').textContent;
    (r.classList.contains('keep')?add:cut).push(`- ${{r.dataset.kw}}  [${{t}}]`)}});
  const txt=(add.length?'ADD BACK:\\n'+add.join('\\n')+'\\n':'')+(cut.length?'CUT:\\n'+cut.join('\\n'):'')||'No changes, use your picks as they are.';
  try{{await navigator.clipboard.writeText(txt); msg.textContent='Copied. Paste it in chat.'}}catch(e){{prompt('Copy this:',txt)}}
}};
document.querySelectorAll('a.th,a.insb').forEach(a=>a.onclick=ev=>{{ev.preventDefault(); lbi.src=a.getAttribute('href'); lbc.textContent=a.dataset.cap; lb.hidden=false}});
lb.onclick=()=>{{lb.hidden=true; lbi.removeAttribute('src')}};
document.onkeydown=ev=>{{if(ev.key==='Escape')lb.onclick()}};
sync();
</script></body></html>'''
    (ROOT / "review").mkdir(exist_ok=True)
    (ROOT / "review" / "index.html").write_text(html)
    print(f"captured {total}, kept {kept}")
