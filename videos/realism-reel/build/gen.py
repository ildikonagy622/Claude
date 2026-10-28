"""Generates the shot-list scenes (hook, details, results) and the captions track.

Run from the project root: python3 build/gen.py
Edit the shot lists or word fixes here, then re-run; the hand-written scenes
(howto, step1, master, capture, layer, cta) are not touched.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = os.path.join(ROOT, "compositions")

W, H = 1080, 1920
CARD = dict(x=160, y=220, w=760, h=960)
IMG = {"kovacs": (964, 1247), "oltozo": (1068, 1433)}
# broll.mp4 is 1920x1080; shown full-bleed at 1920 px tall
BROLL_W = round(1920 * 1920 / 1080)

FONTS = """
    @font-face { font-family: "Inter Tight"; font-weight: 700; src: url("assets/fonts/InterTight-700.ttf"); }
    @font-face { font-family: "Inter Tight"; font-weight: 800; src: url("assets/fonts/InterTight-800.ttf"); }
"""

SHOT_CSS = """
    #root { position: absolute; inset: 0; overflow: hidden; background: #0b0910; }
    .shot { position: absolute; inset: 0; overflow: hidden; }
    .bg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .card { position: absolute; left: %(x)dpx; top: %(y)dpx; width: %(w)dpx; height: %(h)dpx;
      border-radius: 36px; overflow: hidden; background: #000;
      box-shadow: 0 40px 120px rgba(0,0,0,.65), 0 0 0 1px rgba(255,255,255,.08); }
    .cam { position: absolute; }
    .cam img { position: absolute; left: 0; top: 0; width: 100%%; height: 100%%; }
    .vwrap { position: absolute; inset: 0; overflow: hidden; }
    .vwrap video { position: absolute; top: 0; height: 1920px; width: %(bw)dpx; }
    .shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(11,9,16,.35) 0%%, rgba(11,9,16,0) 30%%, rgba(11,9,16,0) 55%%, rgba(11,9,16,.7) 100%%); }
    .chip { position: absolute; left: 0; right: 0; top: 1100px; text-align: center; }
    .chip span { display: inline-block; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 34px;
      color: #0b0910; background: var(--accent, #ee4bff); padding: 10px 22px; border-radius: 12px; }
    .tag { position: absolute; left: 0; right: 0; top: 1100px; text-align: center; }
    .tag span { display: inline-block; font-family: "Inter Tight", sans-serif; font-weight: 700; font-size: 30px;
      color: #fff; background: rgba(11,9,16,.72); padding: 10px 20px; border-radius: 999px;
      border: 1px solid rgba(255,255,255,.18); letter-spacing: .02em; }
""" % dict(CARD, bw=BROLL_W)


def cam_geom(name, z, fx, fy):
    """Cover the card with the image, scale by z, keep (fx, fy) as centred as the edges allow."""
    iw, ih = IMG[name]
    cw, ch = CARD["w"], CARD["h"]
    s = max(cw / iw, ch / ih)
    bw, bh = iw * s, ih * s
    offx, offy = (cw - bw) / 2, (ch - bh) / 2

    def pos(zz):
        x = cw / 2 - offx - fx * bw * zz
        y = ch / 2 - offy - fy * bh * zz
        x = min(-offx, max(cw - offx - bw * zz, x))
        y = min(-offy, max(ch - offy - bh * zz, y))
        return round(x, 1), round(y, 1)

    return dict(left=round(offx, 1), top=round(offy, 1), w=round(bw, 1), h=round(bh, 1), a=pos(z), b=pos(z * 1.05), z=z)


def scene(cid, dur, shots, extra_css="", extra_html="", extra_js=""):
    html, js = [], []
    for i, s in enumerate(shots):
        sid = f"{cid}-s{i + 1}"
        st, du = s["t"], s["d"]
        z = i + 1
        if s["kind"] == "card":
            g = cam_geom(s["img"], s.get("z", 1.0), s.get("fx", 0.5), s.get("fy", 0.5))
            label = ""
            if s.get("chip"):
                label = f'<div class="chip" id="{sid}-chip"><span>{s["chip"]}</span></div>'
            elif s.get("tag"):
                label = f'<div class="tag" id="{sid}-tag"><span>{s["tag"]}</span></div>'
            html.append(
                f'''    <div id="{sid}" class="clip shot" data-start="{st}" data-duration="{du}" data-track-index="1" style="z-index:{z}">
      <img class="bg" src="assets/img/{s["img"]}_bg.jpg" alt="" />
      <div class="card"><div class="cam" id="{sid}-cam" style="left:{g["left"]}px;top:{g["top"]}px;width:{g["w"]}px;height:{g["h"]}px"><img src="assets/img/{s["img"]}.png" alt="" /></div></div>
      {label}
    </div>''')
            js.append(
                f'tl.fromTo("#{sid}-cam", {{ transformOrigin: "0 0", scale: {g["z"]}, x: {g["a"][0]}, y: {g["a"][1]} }}, '
                f'{{ scale: {round(g["z"] * 1.05, 3)}, x: {g["b"][0]}, y: {g["b"][1]}, duration: {du}, ease: "none" }}, {st});')
            if i > 0 and s.get("pop", True):
                js.append(f'tl.fromTo("#{sid} .card", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.22, ease: "expo.out" }}, {st});')
            if label:
                sel = f"#{sid}-chip span" if s.get("chip") else f"#{sid}-tag span"
                js.append(f'tl.fromTo("{sel}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "expo.out" }}, {round(st + 0.06, 2)});')
        else:  # broll footage, full-bleed 9:16 window
            left = s.get("left", 900)
            sc = s.get("z", 1.0)
            html.append(
                f'''    <div class="vwrap" id="{sid}-wrap" style="z-index:{z}">
      <video id="{sid}" class="clip" src="assets/video/broll.mp4" muted playsinline data-start="{st}" data-duration="{du}" data-media-start="{s["src"]}" data-track-index="1" style="left:-{left}px"></video>
      <div class="shade"></div>
    </div>''')
            js.append(
                f'tl.fromTo("#{sid}-wrap", {{ transformOrigin: "50% 45%", scale: {sc} }}, {{ scale: {round(sc * 1.05, 3)}, duration: {du}, ease: "none" }}, {st});')
    doc = f'''<template>
  <style>
{FONTS}{SHOT_CSS}{extra_css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
{chr(10).join(html)}
{extra_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + j for j in js).strip()}
    {extra_js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''
    with open(os.path.join(COMP, f"{cid}.html"), "w") as f:
        f.write(doc)


# ---------- hook: 0 – 6.62 ----------
scene("hook", 6.62, [
    dict(kind="card", t=0, d=0.62, img="oltozo", z=1.0, fx=0.5, fy=0.5, pop=False),
    dict(kind="card", t=0.62, d=0.56, img="kovacs", z=1.45, fx=0.72, fy=0.30),
    dict(kind="broll", t=1.18, d=0.56, src=4.0, left=1100, z=1.0),
    dict(kind="card", t=1.74, d=0.56, img="oltozo", z=1.9, fx=0.57, fy=0.31),
    dict(kind="card", t=2.30, d=0.56, img="kovacs", z=1.5, fx=0.52, fy=0.86),
    dict(kind="broll", t=2.86, d=0.56, src=9.0, left=1300, z=1.35),
    dict(kind="card", t=3.42, d=1.08, img="kovacs", z=1.0),
    dict(kind="card", t=4.50, d=0.60, img="oltozo", z=1.6, fx=0.55, fy=0.36),
    dict(kind="broll", t=5.10, d=0.60, src=12.5, left=1150, z=1.0),
    dict(kind="card", t=5.70, d=0.92, img="oltozo", z=1.0),
])

# ---------- details: 33.00 – 45.00 (local) ----------
details_css = """
    .pcard { position: absolute; left: 70px; top: 300px; width: 940px; border-radius: 34px; padding: 52px 52px 56px;
      background: rgba(18,14,26,.94); border: 4px solid var(--accent, #ee4bff);
      box-shadow: 0 0 0 1px rgba(255,255,255,.06), 0 30px 120px rgba(0,0,0,.6), 0 0 80px rgba(238,75,255,.22); }
    .pgrid { position: absolute; inset: 0; background-image: linear-gradient(rgba(255,255,255,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.045) 1px, transparent 1px); background-size: 54px 54px; }
    .plabel { font-family: "Inter Tight", sans-serif; font-weight: 800; font-size: 34px; color: var(--accent, #ee4bff); letter-spacing: .06em; text-transform: uppercase; margin-bottom: 26px; }
    .ptext { font-family: "JetBrains Mono", monospace; font-weight: 500; font-size: 41px; line-height: 1.42; color: #f2eef8; }
"""
details_html = """    <div id="details-doc" class="clip shot" data-start="0" data-duration="1.92" data-track-index="1" style="z-index:30">
      <div class="pgrid"></div>
      <div class="pcard" id="details-pcard">
        <div class="plabel">3. Reality layer — valóság réteg</div>
        <div class="ptext">uneven skin tone and texture, visible pores across the nose and cheeks, a few small blemishes, subtle redness on the cheeks, fine lines, faint discoloration, real facial hair catching the light</div>
      </div>
    </div>"""
details_js = 'tl.fromTo("#details-pcard", { opacity: 0, scale: 0.94, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out" }, 0.02);'
scene("details", 12, [
    dict(kind="card", t=1.92, d=1.40, img="kovacs", z=1.35, fx=0.70, fy=0.36, chip="uneven skin texture"),
    dict(kind="card", t=3.32, d=1.10, img="oltozo", z=2.0, fx=0.56, fy=0.30, chip="visible pores"),
    dict(kind="card", t=4.42, d=0.98, img="kovacs", z=1.45, fx=0.73, fy=0.21, chip="age spots"),
    dict(kind="card", t=5.40, d=1.08, img="oltozo", z=1.6, fx=0.58, fy=0.33, chip="a few small blemishes"),
    dict(kind="card", t=6.48, d=1.16, img="oltozo", z=1.8, fx=0.53, fy=0.33, chip="subtle redness on the cheeks"),
    dict(kind="card", t=7.64, d=1.04, img="kovacs", z=1.5, fx=0.68, fy=0.27, chip="fine lines"),
    dict(kind="card", t=8.68, d=1.88, img="kovacs", z=1.3, fx=0.62, fy=0.48, chip="faint discoloration"),
    dict(kind="card", t=10.56, d=1.44, img="kovacs", z=1.4, fx=0.72, fy=0.42, chip="real facial hair"),
], extra_css=details_css, extra_html=details_html, extra_js=details_js)

# ---------- results: 45.00 – 51.80 (local) ----------
scene("results", 6.8, [
    dict(kind="card", t=0, d=3.3, img="oltozo", z=1.0, tag="Nano Banana Pro · Magnific · 2K", pop=False),
    dict(kind="card", t=3.3, d=3.5, img="kovacs", z=1.0, tag="Nano Banana Pro · Magnific · 2K"),
])

# ---------- captions ----------
words = json.load(open(os.path.join(ROOT, "build", "words_src.json")))
merged = []
for w in words:
    s = w["start"]
    if 24.15 <= s < 27.7:  # dropped flub "De a szokásos ... messz..."
        continue
    if w["text"].startswith("-") and merged:
        merged[-1]["text"] += w["text"]
        merged[-1]["end"] = w["end"]
        continue
    merged.append(dict(w))
FIX = {"Magnificat": "Magnificet", "Higgsfield-en": "Higgsfielden", "egyenletlen": "egyenetlen",
       "arcszörzet.": "arcszőrzet.", "Kommented,": "Kommenteld,", "éjjálj,": "„AI”,"}
for w in merged:
    w["text"] = FIX.get(w["text"].strip(), w["text"].strip())
    s = max(w["start"], 28.45) if w["start"] >= 27.7 else w["start"]
    e = w["end"]
    off = 11.28 if w["start"] >= 27.7 else 7.10
    w["s"], w["e"] = round(s - off, 3), round(e - off, 3)

ACCENT = {"mesterségesnek?", "hibás,", "promptod.", "promptod", "Magnificet", "Nano", "Banana", "Pro-val.",
          "mester", "prompt", "rendszert.", "iPhone-nal", "pórusok,", "májfoltok,", "bőrhibák,", "orcák,",
          "ráncok,", "arcszőrzet.", "igazivá", "hihetővé,", "viaszos", "egyenetlen", "elszíneződések",
          "fényekkel,", "Higgsfielden", "Leonardo", "AI-on."}
# big-title scenes carry their own words
EXCL = [(6.62, 8.42), (29.8, 33.0), (51.8, 64.2)]

FUNC = {"a", "az", "egy", "hogy", "és", "de", "ami", "le", "is", "én", "akár", "vagy", "túl"}
groups = []
cur = []
for i, w in enumerate(merged):
    if any(a <= w["s"] < b for a, b in EXCL):
        continue
    if cur:
        prev = cur[-1]
        txt = " ".join(x["text"] for x in cur + [w])
        content = [x for x in cur if x["text"].lower() not in FUNC]
        if prev["text"][-1] in ",.?!:" or w["s"] - prev["e"] > 0.15 or (
            prev["text"].lower() not in FUNC and (len(content) >= 2 or len(txt) > 18)
        ) or len(txt) > 24:
            groups.append(cur)
            cur = []
    cur.append(w)
if cur:
    groups.append(cur)

cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    start = round(max(0.12, g[0]["s"] - 0.04), 3)
    nxt = groups[gi + 1][0]["s"] - 0.04 if gi + 1 < len(groups) else 99
    end = round(min(nxt, g[-1]["e"] + 0.35), 3)
    for a, b in EXCL:  # never run into a big-title scene
        if start < a < end:
            end = a
    spans = []
    for w in g:
        t = w["text"].rstrip(",.:")
        cls = ' class="ac"' if w["text"] in ACCENT else ""
        spans.append(f"<span{cls}>{t}</span>")
    gid = f"cap-{gi + 1}"
    cap_html.append(f'    <div id="{gid}" class="clip grp" data-start="{start}" data-duration="{round(end - start, 3)}" data-track-index="0"><div class="in" id="{gid}-in">{" ".join(spans)}</div></div>')
    cap_js.append(f'tl.fromTo("#{gid}-in", {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "back.out(2.2)" }}, {start});')

cap_doc = f'''<template>
  <style>
{FONTS}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .grp {{ position: absolute; left: 0; right: 0; top: 1218px; height: 120px; text-align: center; overflow: visible; }}
    .in {{ display: inline-block; font-family: "Inter Tight", sans-serif; font-weight: 800; font-size: 76px; line-height: 1;
      letter-spacing: -0.02em; color: #fff; text-shadow: 0 4px 22px rgba(0,0,0,.75), 0 1px 3px rgba(0,0,0,.6); }}
    .in .ac {{ color: var(--accent, #ee4bff); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}" data-layout-allow-caption-zone>
{chr(10).join(cap_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + j for j in cap_js).strip()}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
with open(os.path.join(COMP, "captions.html"), "w") as f:
    f.write(cap_doc)
print(len(groups), "caption groups")
for g in groups:
    print(f'{g[0]["s"]:6.2f} ' + " ".join(w["text"] for w in g))
