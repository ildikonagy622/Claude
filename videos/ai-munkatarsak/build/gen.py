"""Builds every scene and the captions track from build/vo.json (word timings).

Run from the project root after build/vo.py: python3 build/gen.py
Scene times are in root seconds; each scene file uses its own local clock."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = os.path.join(ROOT, "compositions")
VO = json.load(open(os.path.join(ROOT, "build", "vo.json")))
WORDS = VO["words"]
END = 60.8

# scene windows on the root timeline
SCENES = [
    ("hook", 0.0, 4.04),
    ("forget", 4.04, 8.84),
    ("trained", 8.84, 22.32),
    ("auditor", 22.32, 34.56),
    ("eu", 34.56, 43.36),
    ("nohal", 43.36, 48.17),
    ("pages", 48.17, 57.4),
    ("recap", 57.4, END),
]


def at(word, beat=None, nth=0):
    """Root time of a spoken word (first match, or the nth)."""
    hits = [w for w in WORDS if w["text"].strip(",.?!").lower().startswith(word.lower()) and (beat is None or w["beat"] == beat)]
    return hits[nth]["start"]


FONTS = """
    @font-face { font-family: "Inter Tight"; font-weight: 700; src: url("assets/fonts/InterTight-700.ttf"); }
    @font-face { font-family: "Inter Tight"; font-weight: 800; src: url("assets/fonts/InterTight-800.ttf"); }
"""

BASE = """
    #root { position: absolute; inset: 0; overflow: hidden; background: #0b0910; font-family: "Inter Tight", sans-serif; color: #fff; }
    .glow { position: absolute; left: -300px; top: 200px; width: 1680px; height: 1400px;
      background: radial-gradient(closest-side, rgba(149,112,255,.28), rgba(149,112,255,0)); }
    .grid { position: absolute; inset: 0; background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px); background-size: 60px 60px; }
    .h { position: absolute; left: 60px; right: 60px; text-align: center; font-weight: 800; letter-spacing: -0.035em; line-height: .95; }
    .ac { color: var(--accent, #9570ff); }
    .chip { position: absolute; display: inline-flex; align-items: center; gap: 12px; height: 64px; padding: 0 26px; border-radius: 999px;
      background: rgba(149,112,255,.16); border: 2px solid var(--accent, #9570ff); font-weight: 800; font-size: 32px; letter-spacing: .06em;
      text-transform: uppercase; color: #fff; }
    .card { position: absolute; border-radius: 30px; background: rgba(22,18,34,.92); border: 2px solid rgba(149,112,255,.35);
      box-shadow: 0 30px 90px rgba(0,0,0,.55); }
    .panel { position: absolute; left: 40px; width: 1000px; border-radius: 26px; overflow: hidden; background: #fff;
      box-shadow: 0 0 0 3px rgba(149,112,255,.55), 0 40px 120px rgba(0,0,0,.7); }
    .bar { position: absolute; left: 0; right: 0; top: 0; height: 54px; background: #ece9f5; display: flex; align-items: center; gap: 10px; padding: 0 20px; }
    .bar i { width: 14px; height: 14px; border-radius: 50%; background: #c9c3dc; display: block; }
    .bar span { margin-left: 14px; flex: 1; height: 34px; border-radius: 17px; background: #fff; color: #4a4560; font-size: 28px; font-weight: 700;
      display: flex; align-items: center; padding: 0 18px; letter-spacing: 0; }
    .ring { position: absolute; border: 6px solid var(--accent, #9570ff); border-radius: 18px; box-shadow: 0 0 0 4000px rgba(11,9,16,0), 0 0 40px rgba(149,112,255,.8); }
    .tag { position: absolute; height: 66px; padding: 0 26px; border-radius: 18px; background: var(--accent, #9570ff); color: #0b0910;
      font-weight: 800; font-size: 34px; display: flex; align-items: center; white-space: nowrap; box-shadow: 0 16px 40px rgba(0,0,0,.45); }
    svg.arrow { position: absolute; overflow: visible; }
    svg.arrow path { fill: none; stroke: var(--accent, #9570ff); stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }
"""


def arrow(aid, x1, y1, x2, y2, bend=0.0):
    """An SVG arrow from (x1,y1) to (x2,y2) drawn on a full-frame canvas; bend curves it sideways."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * bend, my + dx * bend
    import math
    ang = math.atan2(y2 - cy, x2 - cx)
    a1 = (x2 - 34 * math.cos(ang - 0.5), y2 - 34 * math.sin(ang - 0.5))
    a2 = (x2 - 34 * math.cos(ang + 0.5), y2 - 34 * math.sin(ang + 0.5))
    return (f'<svg class="arrow" id="{aid}" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">'
            f'<path id="{aid}-line" d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {x2:.0f},{y2:.0f}" pathLength="1" />'
            f'<path id="{aid}-head" d="M{a1[0]:.0f},{a1[1]:.0f} L{x2:.0f},{y2:.0f} L{a2[0]:.0f},{a2[1]:.0f}" /></svg>')


def draw_arrow(aid, t, dur=0.32):
    return [f'tl.fromTo("#{aid}-line", {{ strokeDasharray: 1, strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: {dur}, ease: "power2.out" }}, {t:.3f});',
            f'tl.fromTo("#{aid}-head", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08 }}, {t + dur - 0.06:.3f});']


def pop(sel, t, s0=0.6, d=0.32):
    return f'tl.fromTo("{sel}", {{ opacity: 0, scale: {s0} }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(1.9)" }}, {t:.3f});'


def blurin(sel, t, d=0.2):
    return f'tl.fromTo("{sel}", {{ opacity: 0, filter: "blur(10px)", scale: 1.08 }}, {{ opacity: 1, filter: "blur(0px)", scale: 1, duration: {d}, ease: "expo.out" }}, {t:.3f});'


def out(sel, t, d=0.16):
    return f'tl.to("{sel}", {{ opacity: 0, filter: "blur(10px)", duration: {d}, ease: "power2.in" }}, {t:.3f});'


def write(cid, css, html, js, ground=True):
    bg = '    <div class="glow"></div><div class="grid"></div>\n' if ground else ""
    doc = f"""<template>
  <style>
{FONTS}{BASE}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overflow>
{bg}{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in js).strip()}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
    open(os.path.join(COMP, f"{cid}.html"), "w").write(doc)


def win(cid):
    return next((a, b) for c, a, b in SCENES if c == cid)



# ---------------- hook: the forgetful intern ----------------
s0, s1 = win("hook")
tf = at("feledékeny") - s0
html = '''    <div class="h" id="hk-t" style="top:290px;font-size:112px">Az AI-od egy<br /><span class="ac">feledékeny</span><br />gyakornok?</div>
    <div class="card" id="hk-c" style="left:150px;top:720px;width:780px;height:420px;padding:44px 60px">
      <div style="display:flex;gap:18px">
        <img src="assets/img/logo_chatgpt.png" alt="" style="width:86px;height:86px;border-radius:20px;object-fit:cover" />
        <img src="assets/img/logo_gemini.png" alt="" style="width:86px;height:86px;border-radius:20px;object-fit:cover" />
        <img src="assets/img/logo_claude.png" alt="" style="width:86px;height:86px;border-radius:20px;object-fit:cover" />
      </div>
      <div style="margin-top:40px;font-size:40px;font-weight:800;display:flex;justify-content:space-between"><span>Memória</span><span><span id="hk-pct" style="font-variant-numeric:tabular-nums">100</span>%</span></div>
      <div style="margin-top:18px;height:56px;border-radius:28px;background:rgba(255,255,255,.08);overflow:hidden">
        <div id="hk-bar" style="height:100%;width:100%;border-radius:28px;background:var(--accent,#9570ff)"></div>
      </div>
    </div>'''
js = [f'tl.fromTo("#hk-t", {{ scale: 1.1 }}, {{ scale: 1, duration: 0.5, ease: "expo.out" }}, 0);',
      f'tl.fromTo("#hk-c", {{ y: 60 }}, {{ y: 0, duration: 0.5, ease: "expo.out" }}, 0);',
      f'tl.fromTo("#hk-bar", {{ scaleX: 1, transformOrigin: "0% 50%" }}, {{ scaleX: 0.04, duration: 1.1, ease: "power2.in" }}, {tf:.3f});',
      f'tl.fromTo("#hk-pct", {{ innerText: 100 }}, {{ innerText: 4, snap: {{ innerText: 1 }}, duration: 1.1, ease: "power2.in" }}, {tf:.3f});',
      f'tl.to("#hk-bar", {{ backgroundColor: "#ff5a6e", duration: 0.3 }}, {tf + 0.7:.3f});',
      f'tl.to("#hk-c", {{ x: -14, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }}, {tf + 1.1:.3f});',
      f'tl.to(["#hk-t", "#hk-c"], {{ opacity: 0, y: -80, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("hook", "    #hk-t .ac { display: inline-block; }\n", html, js)

# ---------------- forget: has to be briefed again and again ----------------
s0, s1 = win("forget")
td = at("ajtón") - s0
tu = at("újra", "forget") - s0
badge = lambda bid, n, role, tool, top=300: (f'<div class="card" id="{bid}" style="left:60px;top:{top}px;width:960px;height:150px;display:flex;align-items:center;gap:26px;padding:0 30px">'
                                         f'<div class="ac" style="font-size:96px;font-weight:800;width:70px">{n}</div>'
                                         f'<div><div style="font-size:52px;font-weight:800;letter-spacing:-0.02em">{role}</div>'
                                         f'<div style="font-size:32px;font-weight:700;color:rgba(255,255,255,.6);margin-top:4px">{tool}</div></div></div>')
notes = "".join(f'''    <div class="card" id="fg-n{i}" style="left:240px;top:{560 + i * 40}px;width:600px;height:420px;padding:40px;background:#f4f1fb;border:0;opacity:0">
      <div style="color:#0b0910;font-size:42px;font-weight:800">Brief #{i + 1}</div>
      <div style="margin-top:24px;height:22px;border-radius:11px;background:#d9d2ee;width:90%"></div>
      <div style="margin-top:18px;height:22px;border-radius:11px;background:#d9d2ee;width:75%"></div>
      <div style="margin-top:18px;height:22px;border-radius:11px;background:#d9d2ee;width:82%"></div>
      <div style="margin-top:18px;height:22px;border-radius:11px;background:#d9d2ee;width:60%"></div>
    </div>
''' for i in range(3))
html = "    " + badge("fg-b", 1, "Feledékeny gyakornok", "„Sima” chatbot: ChatGPT, Gemini, Claude") + "\n" + notes + \
       '    <div class="tag" id="fg-tag" style="left:0;right:0;margin:0 auto;width:fit-content;top:1110px;font-size:40px;height:76px;opacity:0">↻ Mindig újra be kell tanítani</div>'
js = [f'tl.fromTo("#fg-b", {{ opacity: 0, x: -200 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.02);',
      f'tl.fromTo("#fg-n0", {{ opacity: 0, y: 80, rotation: -3 }}, {{ opacity: 1, y: 0, rotation: -2, duration: 0.35, ease: "back.out(1.6)" }}, 0.25);',
      f'tl.to("#fg-n0", {{ opacity: 0, scale: 0.6, rotation: -25, x: -500, filter: "blur(8px)", duration: 0.4, ease: "power3.in" }}, {td:.3f});',
      f'tl.fromTo("#fg-n1", {{ opacity: 0, y: 80, rotation: 3 }}, {{ opacity: 1, y: 0, rotation: 2, duration: 0.3, ease: "back.out(1.6)" }}, {td + 0.35:.3f});',
      f'tl.to("#fg-n1", {{ opacity: 0, scale: 0.6, rotation: 25, x: 500, filter: "blur(8px)", duration: 0.35, ease: "power3.in" }}, {tu + 0.1:.3f});',
      f'tl.fromTo("#fg-n2", {{ opacity: 0, y: 80, rotation: -2 }}, {{ opacity: 1, y: 0, rotation: -1, duration: 0.3, ease: "back.out(1.6)" }}, {tu + 0.4:.3f});',
      pop("#fg-tag", td, 0.5),
      f'tl.to(["#fg-b", "#fg-n2", "#fg-tag"], {{ opacity: 0, x: -140, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("forget", "", html, js)

# ---------------- trained: Custom GPT / Gem / Project ----------------
s0, s1 = win("trained")
GPX, GPY, GS = 110, 470, 860 / 1480
gvh = round(1080 * GS)
G = lambda x, y: (GPX + x * GS, GPY + 54 + y * GS)
nx0, ny0 = G(211, 202); nx1, ny1 = G(763, 250)
lx0, ly0 = G(211, 306); lx1, ly1 = G(763, 355)
ux0, uy0 = G(211, 414); ux1, uy1 = G(763, 801)
tb = at("betanított") - s0
tm = at("munkaköri") - s0
ts = at("szabályokat", "trained") - s0
tst = at("stílust") - s0
tc = at("Digitális") - s0
ring = lambda rid, a, b, c, d: f'<div class="ring" id="{rid}" style="left:{a - 6:.0f}px;top:{b - 6:.0f}px;width:{c - a + 12:.0f}px;height:{d - b + 12:.0f}px;opacity:0"></div>'
html = f'''    {badge("tr-b", 2, "Betanított munkatárs", "Custom GPT · Gemini Gem · Claude Project")}
    <div class="panel" id="tr-panel" style="left:{GPX}px;width:860px;top:{GPY}px;height:{gvh + 54}px">
      <div class="bar"><i></i><i></i><i></i><span>gemini.google.com · Új gem</span></div>
      <video id="tr-v" class="clip" src="assets/video/gem.mp4" muted playsinline data-start="0" data-duration="{s1 - s0:.2f}" data-media-start="2" data-track-index="1" style="position:absolute;left:0;top:54px;width:860px;height:{gvh}px"></video>
    </div>
    {ring("tr-r1", nx0, ny0, nx1, ny1)}
    {ring("tr-r2", lx0, ly0, lx1, ly1)}
    {ring("tr-r3", ux0, uy0, ux1, uy1)}
    <div class="tag" id="tr-t2" style="left:560px;top:{(ly0 + ly1) / 2 - 33:.0f}px;opacity:0">Munkaköri leírás</div>
    <div class="tag" id="tr-t3" style="left:560px;top:{(uy0 + uy1) / 2 - 33:.0f}px;opacity:0">Szabályok + stílus</div>
    {arrow("tr-a2", 560, (ly0 + ly1) / 2, lx1 + 14, (ly0 + ly1) / 2, 0.2)}
    {arrow("tr-a3", 560, (uy0 + uy1) / 2, ux1 + 14, (uy0 + uy1) / 2, -0.2)}
    <div class="card" id="tr-clone" style="left:90px;top:620px;width:900px;height:420px;padding:50px;text-align:center;opacity:0;border:3px solid #9570ff">
      <div style="font-size:60px;font-weight:800;line-height:1.05">Egyszer tanítod be,</div>
      <div class="ac" style="font-size:84px;font-weight:800;margin-top:14px">mindig emlékszik.</div>
      <div style="margin-top:34px;display:flex;justify-content:center;gap:16px">
        <div class="tag" style="position:static;height:60px;font-size:30px">✓ szabályok</div>
        <div class="tag" style="position:static;height:60px;font-size:30px">✓ stílus</div>
        <div class="tag" style="position:static;height:60px;font-size:30px">✓ tudás</div>
      </div>
    </div>'''
js = [f'tl.fromTo("#tr-b", {{ opacity: 0, x: -200 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, {tb - 0.3:.3f});',
      f'tl.fromTo("#tr-panel", {{ opacity: 0, scale: 0.85, y: 120 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "expo.out" }}, 0);',
      pop("#tr-r1", 0.5, 1.1), f'tl.to("#tr-r1", {{ opacity: 0, duration: 0.15 }}, {tm - 0.2:.3f});',
      pop("#tr-r2", tm, 1.1), pop("#tr-t2", tm + 0.1), *draw_arrow("tr-a2", tm + 0.1),
      pop("#tr-r3", ts, 1.1), pop("#tr-t3", ts + 0.1), *draw_arrow("tr-a3", ts + 0.1),
      f'tl.to("#tr-r3", {{ boxShadow: "0 0 0 4000px rgba(11,9,16,0), 0 0 70px rgba(149,112,255,1)", duration: 0.2, yoyo: true, repeat: 1 }}, {tst:.3f});',
      f'tl.to(["#tr-panel", "#tr-r2", "#tr-r3", "#tr-t2", "#tr-t3", "#tr-a2", "#tr-a3"], {{ opacity: 0.12, filter: "blur(6px)", duration: 0.25 }}, {tc - 0.1:.3f});',
      f'tl.fromTo("#tr-clone", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.7)" }}, {tc - 0.05:.3f});',
      f'tl.to(["#tr-b", "#tr-clone", "#tr-panel"], {{ opacity: 0, x: -140, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("trained", "", html, js)

# ---------------- auditor: NotebookLM ----------------
s0, s1 = win("auditor")
NPX, NPY, NS = 40, 545, 1000 / 1920
nvh = round(900 * NS)
N = lambda x, y: (NPX + x * NS, NPY + 54 + y * NS)
fx0, fy0 = N(10, 76); fx1, fy1 = N(476, 893)
cx0, cy0 = N(503, 76); cx1, cy1 = N(1412, 893)
tsz = at("szigorú") - s0
tdk = at("dokumentumokkal") - s0
tfa = at("fantáziát") - s0
thv = at("hivatkozással") - s0
html = f'''    {badge("au-b", 3, "Szigorú belső ellenőr", "NotebookLM")}
    <div class="panel" id="au-panel" style="top:{NPY}px;height:{nvh + 54}px">
      <div class="bar"><i></i><i></i><i></i><span>notebooklm.google.com</span></div>
      <video id="au-v" class="clip" src="assets/video/nblm.mp4" muted playsinline data-start="0" data-duration="{s1 - s0:.2f}" data-media-start="0.5" data-track-index="1" style="position:absolute;left:0;top:54px;width:1000px;height:{nvh}px"></video>
    </div>
    {ring("au-r1", fx0, fy0, fx1, fy1)}
    {ring("au-r2", cx0, cy0, cx1, cy1)}
    <div class="tag" id="au-t1" style="left:60px;top:{fy1 + 50:.0f}px;opacity:0">📄 Csak a te dokumentumaid</div>
    {arrow("au-a1", 230, fy1 + 50, (fx0 + fx1) / 2, fy1 + 14, -0.15)}
    <div class="tag" id="au-t3" style="left:560px;top:{fy1 + 50:.0f}px;opacity:0">🔗 Forrás minden állításhoz</div>
    {arrow("au-a3", 760, fy1 + 50, (cx0 + cx1) / 2, cy1 + 14, 0.15)}
    <div class="tag" id="au-t2" style="left:0;right:0;margin:0 auto;width:fit-content;top:{NPY - 74}px;opacity:0;background:#ff5a6e;color:#fff">✗ Nincs fantázia, nincs kitalálás</div>'''
js = [f'tl.fromTo("#au-b", {{ opacity: 0, x: -200 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, {tsz - 0.5:.3f});',
      f'tl.fromTo("#au-panel", {{ opacity: 0, scale: 0.85, y: 120 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "expo.out" }}, 0);',
      pop("#au-r1", tdk, 1.1), pop("#au-t1", tdk + 0.1), *draw_arrow("au-a1", tdk + 0.1),
      pop("#au-t2", tfa, 0.5),
      pop("#au-r2", thv, 1.1), pop("#au-t3", thv + 0.1), *draw_arrow("au-a3", thv + 0.1),
      f'tl.to(["#au-b", "#au-panel", "#au-r1", "#au-r2", "#au-t1", "#au-t2", "#au-t3", "#au-a1", "#au-a3"], {{ opacity: 0, scale: 0.92, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }}, {s1 - s0 - 0.22:.3f});']
write("auditor", "", html, js)

# ---------------- eu: the 300-page tender ----------------
s0, s1 = win("eu")
t300 = at("300") - s0
tup = at("feltöltöd") - s0
tq = at("kizáró") - s0
pages = "".join(f'<div class="pg" id="eu-p{i}" style="left:{300 + i * 10}px;top:{540 - i * 12}px"></div>' for i in range(6))
html = f'''    <div class="h" id="eu-t" style="top:300px;font-size:92px">Példa: <span class="ac">EU-s pályázat</span></div>
    {pages}
    <div class="card" id="eu-doc" style="left:240px;top:480px;width:420px;height:540px;background:#f4f1fb;border:0;padding:44px">
      <div style="color:#0b0910;font-size:40px;font-weight:800">EU pályázati kiírás</div>
      <div style="margin-top:20px;height:18px;border-radius:9px;background:#d9d2ee;width:90%"></div>
      <div style="margin-top:14px;height:18px;border-radius:9px;background:#d9d2ee;width:80%"></div>
      <div style="margin-top:14px;height:18px;border-radius:9px;background:#d9d2ee;width:86%"></div>
      <div style="position:absolute;left:44px;bottom:40px;color:#0b0910;font-weight:800;font-size:110px;line-height:1;font-variant-numeric:tabular-nums"><span id="eu-n">0</span><span style="font-size:44px"> oldal</span></div>
    </div>
    <div class="card" id="eu-nb" style="left:720px;top:620px;width:260px;height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;border:3px solid #9570ff;opacity:0">
      <div style="font-size:84px">📓</div><div style="font-size:34px;font-weight:800">NotebookLM</div></div>
    {arrow("eu-a", 670, 750, 712, 750, 0)}
    <div class="card" id="eu-q" style="left:150px;top:1060px;width:780px;height:120px;border-radius:60px;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;background:var(--accent,#9570ff);color:#0b0910;border:0;opacity:0">„Mik a kizáró okok?”</div>'''
css = "    .pg { position: absolute; width: 420px; height: 540px; border-radius: 30px; background: #d9d2ee; box-shadow: 0 10px 30px rgba(0,0,0,.4); }\n"
js = [blurin("#eu-t", 0.02),
      f'tl.fromTo(["#eu-p5", "#eu-p4", "#eu-p3", "#eu-p2", "#eu-p1", "#eu-p0", "#eu-doc"], {{ opacity: 0, y: -260 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.4)", stagger: 0.06 }}, {t300 - 0.5:.3f});',
      f'tl.fromTo("#eu-n", {{ innerText: 0 }}, {{ innerText: 300, snap: {{ innerText: 1 }}, duration: 1.2, ease: "expo.out" }}, {t300:.3f});',
      f'tl.fromTo("#eu-nb", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, {tup:.3f});',
      *draw_arrow("eu-a", tup + 0.1, 0.25),
      f'tl.to(["#eu-doc", "#eu-p0", "#eu-p1", "#eu-p2", "#eu-p3", "#eu-p4", "#eu-p5"], {{ x: 420, scale: 0.4, opacity: 0, duration: 0.45, ease: "power3.in", stagger: 0.03 }}, {tup + 0.4:.3f});',
      f'tl.to("#eu-nb", {{ x: -280, scale: 1.4, duration: 0.5, ease: "power3.inOut" }}, {tup + 0.7:.3f});',
      f'tl.fromTo("#eu-q", {{ opacity: 0, y: 60, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }}, {at("megkérdezed") - s0:.3f});',
      f'tl.to(["#eu-t", "#eu-nb", "#eu-q"], {{ opacity: 0, y: -60, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("eu", css, html, js)

# ---------------- nohal: ChatGPT vs NotebookLM ----------------
s0, s1 = win("nohal")
th = at("hallucinál") - s0
tfr = at("forrásból") - s0
col = lambda cid, x, logo, name, line: (f'<div class="card" id="{cid}" style="left:{x}px;top:470px;width:470px;height:620px;padding:40px;text-align:center">'
                                         f'{logo}<div style="font-size:50px;font-weight:800;margin-top:20px">{name}</div>'
                                         f'<div style="font-size:34px;font-weight:700;color:rgba(255,255,255,.7);margin-top:16px;line-height:1.2">{line}</div></div>')
html = f'''    <div class="h" id="nh-t" style="top:300px;font-size:84px">Miért <span class="ac">ne</span> ChatGPT-vel?</div>
    {col("nh-l", 50, '<img src="assets/img/logo_chatgpt.png" alt="" style="width:140px;height:140px;border-radius:30px;object-fit:cover" />', "ChatGPT", "Ha nem tudja, kikövetkezteti")}
    {col("nh-r", 560, '<div style="font-size:120px;line-height:140px">📓</div>', "NotebookLM", "Csak abból dolgozik, amit feltöltöttél")}
    <div class="tag" id="nh-x" style="left:110px;top:900px;font-size:40px;height:84px;background:#ff5a6e;color:#fff;opacity:0">✗ Hallucinálhat</div>
    <div class="tag" id="nh-ok" style="left:610px;top:900px;font-size:40px;height:84px;opacity:0">✓ Forráshű</div>'''
js = [blurin("#nh-t", 0.02),
      f'tl.fromTo("#nh-l", {{ opacity: 0, x: -200 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.1);',
      f'tl.fromTo("#nh-r", {{ opacity: 0, x: 200 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.2);',
      pop("#nh-x", th, 0.5), f'tl.to("#nh-l", {{ opacity: 0.55, scale: 0.95, duration: 0.25 }}, {th:.3f});',
      pop("#nh-ok", tfr, 0.5), f'tl.to("#nh-r", {{ borderColor: "#9570ff", scale: 1.04, boxShadow: "0 0 70px rgba(149,112,255,.7)", duration: 0.25 }}, {tfr:.3f});',
      f'tl.to(["#nh-t", "#nh-l", "#nh-r", "#nh-x", "#nh-ok"], {{ opacity: 0, x: -140, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("nohal", "", html, js)

# ---------------- pages: every answer cites the page ----------------
s0, s1 = win("pages")
t75 = at("75") - s0
t78 = at("78") - s0
tk = at("kattintani") - s0
te = at("ellenőrizni") - s0
row = lambda rid, txt, chip, cid: (f'<div id="{rid}" style="display:flex;align-items:center;gap:16px;margin-top:26px">'
                                   f'<div style="flex:1;height:22px;border-radius:11px;background:rgba(255,255,255,.18)"></div>'
                                   f'<div class="cite" id="{cid}">{chip}</div></div>')
html = f'''    <div class="h" id="pg-t" style="top:300px;font-size:64px">Minden válasz <span class="ac">ellenőrizhető</span></div>
    <div class="card" id="pg-a" style="left:60px;top:400px;width:960px;height:430px;padding:44px">
      <div style="font-size:44px;font-weight:800">Kizáró okok:</div>
      {row("pg-r1", "", "75. o.", "pg-c1")}
      {row("pg-r2", "", "78. o.", "pg-c2")}
      {row("pg-r3", "", "76. o.", "pg-c3")}
    </div>
    <div class="card" id="pg-doc" style="left:180px;top:860px;width:720px;height:300px;background:#f4f1fb;border:0;padding:36px;opacity:0">
      <div style="color:#6a6385;font-size:30px;font-weight:800">75. oldal</div>
      <div style="margin-top:20px;height:18px;border-radius:9px;background:#d9d2ee;width:88%"></div>
      <div id="pg-hl" style="margin-top:16px;height:40px;border-radius:10px;background:rgba(149,112,255,.35);border:3px solid #9570ff;width:94%"></div>
      <div style="margin-top:16px;height:18px;border-radius:9px;background:#d9d2ee;width:80%"></div>
      <div style="margin-top:16px;height:18px;border-radius:9px;background:#d9d2ee;width:70%"></div>
    </div>
    <svg id="pg-cur" style="position:absolute;left:0;top:0;opacity:0" width="70" height="90" viewBox="0 0 24 30"><path d="M2 2 L2 24 L8 18 L12 28 L16 26 L12 17 L20 17 Z" fill="#fff" stroke="#0b0910" stroke-width="1.6" stroke-linejoin="round"/></svg>
    <div class="tag" id="pg-ok" style="left:0;right:0;margin:0 auto;width:fit-content;top:1060px;font-size:46px;height:84px;opacity:0">✓ Ellenőrizve</div>'''
css = "    .cite { height: 64px; padding: 0 22px; border-radius: 14px; background: var(--accent, #9570ff); color: #0b0910; font-weight: 800; font-size: 34px; display: flex; align-items: center; }\n"
js = [blurin("#pg-t", 0.02),
      f'tl.fromTo("#pg-a", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, 0.08);',
      f'tl.fromTo(["#pg-r1", "#pg-r2", "#pg-r3"], {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.25, ease: "expo.out", stagger: 0.12 }}, 0.3);',
      f'tl.fromTo(["#pg-c1", "#pg-c2", "#pg-c3"], {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2.2)", stagger: 0.1 }}, 0.4);',
      f'tl.to("#pg-c1", {{ scale: 1.25, duration: 0.12, yoyo: true, repeat: 1 }}, {t75:.3f});',
      f'tl.to("#pg-c2", {{ scale: 1.25, duration: 0.12, yoyo: true, repeat: 1 }}, {t78:.3f});',
      f'tl.fromTo("#pg-cur", {{ opacity: 0, x: 980, y: 1300 }}, {{ opacity: 1, x: 900, y: 530, duration: 0.6, ease: "power3.inOut" }}, {tk - 0.6:.3f});',
      f'tl.to("#pg-cur", {{ scale: 0.85, duration: 0.06 }}, {tk:.3f});', f'tl.to("#pg-cur", {{ scale: 1, duration: 0.15 }}, {tk + 0.06:.3f});',
      f'tl.fromTo("#pg-doc", {{ opacity: 0, scale: 0.4, y: -280 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.5)" }}, {tk + 0.05:.3f});',
      f'tl.to("#pg-cur", {{ opacity: 0, duration: 0.15 }}, {tk + 0.4:.3f});',
      f'tl.fromTo("#pg-hl", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.4, ease: "power2.out" }}, {te - 0.2:.3f});',
      pop("#pg-ok", te + 0.4, 0.5),
      f'tl.to(["#pg-t", "#pg-a", "#pg-doc", "#pg-ok"], {{ opacity: 0, y: -60, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("pages", css, html, js)

# ---------------- recap: your three AI colleagues ----------------
s0, s1 = win("recap")
R = [("1", "Feledékeny gyakornok", "Gyors kérdésekre"), ("2", "Betanított munkatárs", "Ismétlődő feladatokra"), ("3", "Szigorú belső ellenőr", "Dokumentumokhoz")]
html = '    <div class="h" id="rc-t" style="top:300px;font-size:96px">A te <span class="ac">3 AI-munkatársad</span></div>\n'
for i, (n, r, u) in enumerate(R):
    html += (f'    <div class="card" id="rc-{i}" style="left:60px;top:{500 + i * 200}px;width:960px;height:170px;display:flex;align-items:center;gap:26px;padding:0 30px">'
             f'<div class="ac" style="font-size:96px;font-weight:800;width:70px">{n}</div><div><div style="font-size:50px;font-weight:800">{r}</div>'
             f'<div style="font-size:32px;font-weight:700;color:rgba(255,255,255,.6);margin-top:4px">{u}</div></div></div>\n')
html += '    <div class="h" id="rc-q" style="top:1150px;font-size:64px">Melyik hiányzik <span class="ac">a csapatodból?</span></div>'
js = [blurin("#rc-t", 0.02)] + [f'tl.fromTo("#rc-{i}", {{ opacity: 0, x: 200 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, {0.2 + i * 0.25:.2f});' for i in range(3)] + \
     [f'tl.fromTo("#rc-q", {{ opacity: 0, scale: 1.4, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }}, 1.3);']
write("recap", "", html, js)

# ---------------- captions ----------------
ACCENT = {"zseniális", "feledékeny", "gyakornokok", "elfelejt", "újra", "custom", "gpt-k", "gemek", "projektek:", "betanított", "munkatársak",
          "munkaköri", "szabályokat", "stílust", "digitális", "klónok", "emlékeznek", "notebook", "lm", "szigorú", "belső", "ellenőr",
          "fantáziát", "tényeket", "hivatkozással", "300", "eu-s", "pályázat", "kizáró", "hallucinál", "forrásból", "75.", "78.", "ellenőrizni"}
FUNC = {"a", "az", "egy", "hogy", "és", "de", "ami", "meg", "is", "ha", "nem", "van", "akkor", "mint", "ezek", "mert", "ott", "le", "csak", "ki"}
groups, cur = [], []
for w in WORDS:
    if cur:
        prev = cur[-1]
        txt = " ".join(x["text"] for x in cur + [w])
        content = [x for x in cur if x["text"].lower().strip(",.?!:") not in FUNC]
        if (prev["text"][-1] in ",.?!:" or w["start"] - prev["end"] > 0.18 or w["beat"] != prev["beat"]
                or (prev["text"].lower().strip(",.?!") not in FUNC and (len(content) >= 2 or len(txt) > 16)) or len(txt) > 22):
            groups.append(cur)
            cur = []
    cur.append(w)
groups.append(cur)
ch, cj = [], []
AC = ' class="ac"'
for gi, g in enumerate(groups):
    st = round(max(0.1, g[0]["start"] - 0.04), 3)
    nx = groups[gi + 1][0]["start"] - 0.04 if gi + 1 < len(groups) else END
    en = round(min(nx, g[-1]["end"] + 0.4), 3)
    spans = " ".join("<span%s>%s</span>" % (AC if w["text"].lower().strip(",.?!„”") in ACCENT else "", w["text"].rstrip(",:"))
                     for w in g)
    gid = f"cap-{gi + 1}"
    ch.append(f'    <div id="{gid}" class="clip grp" data-start="{st}" data-duration="{round(en - st, 3)}" data-track-index="0"><div class="in" id="{gid}-in">{spans}</div></div>')
    cj.append(f'tl.fromTo("#{gid}-in", {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "back.out(2.2)" }}, {st});')
cap = f"""<template>
  <style>
{FONTS}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .grp {{ position: absolute; left: 0; right: 0; top: 1214px; height: 100px; text-align: center; overflow: visible; }}
    .in {{ display: inline-block; font-family: "Inter Tight", sans-serif; font-weight: 800; font-size: 70px; line-height: 1; letter-spacing: -0.02em;
      color: #fff; padding: 12px 26px 16px; border-radius: 20px; background: rgba(11,9,16,.72); }}
    .in .ac {{ color: var(--accent, #9570ff); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-caption-zone>
{chr(10).join(ch)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in cj).strip()}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
open(os.path.join(COMP, "captions.html"), "w").write(cap)

# ---------------- root ----------------
hosts = "\n".join(
    f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
    for c, a, b in SCENES)
sfx = []
def fx(name, f, t, d, v, tr=5, ms=None):
    m = f' data-media-start="{ms}"' if ms is not None else ""
    sfx.append(f'      <audio id="sfx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t:.3f}" data-duration="{d}"{m} data-track-index="{tr}" data-volume="{v}"></audio>')
for j, (c, a, b) in enumerate(SCENES[1:], 1):
    fx(f"cut{j}", "whoosh" if j % 2 else "whoosh-short", a - 0.12, 0.57, 0.35, 7)
fx("drain", "error", at("feledékeny") + 1.1, 0.4, 0.3, 5, 0.58)
fx("tr", "pop", at("betanított") - 0.3, 0.72, 0.35)
fx("clone", "ping", at("Digitális"), 0.6, 0.3, 6)
fx("au", "pop", at("szigorú") - 0.5, 0.72, 0.35)
fx("n300", "impact-bass-1", at("300"), 2.1, 0.3, 6)
fx("q", "pop", at("kizáró") - 0.1, 0.72, 0.35)
fx("ok", "ping", at("forrásból"), 0.6, 0.3)
fx("click", "click", at("kattintani"), 0.36, 0.6, 6)
fx("check", "ping", at("ellenőrizni") + 0.4, 0.6, 0.3)
root = f"""<!doctype html>
<html lang="hu" data-resolution="portrait"
  data-composition-variables='[{{"id":"accent","type":"color","label":"Kiemelő szín","default":"#9570FF"}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      :root {{ --ground: #0b0910; --ink: #ffffff; --accent: #9570ff; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 100%; height: 100%; background: var(--ground); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 20"></div>

      <audio id="vo" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="{VO["beats"][-1]["end"]}" data-track-index="3" data-volume="1"></audio>
      <audio id="music" class="clip" src="assets/audio/chillhop.mp3" data-start="0" data-duration="{END}" data-media-start="1.0" data-track-index="4" data-volume="0.11" data-fade-out="1.2"></audio>
{chr(10).join(sfx)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(root)
print(len(groups), "caption groups")
