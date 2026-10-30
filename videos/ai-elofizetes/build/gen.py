"""Builds every scene and the captions track from build/vo.json (word timings).

Run from the project root after build/vo.py: python3 build/gen.py
Scene times are in root seconds; each scene file uses its own local clock."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = os.path.join(ROOT, "compositions")
VO = json.load(open(os.path.join(ROOT, "build", "vo.json")))
WORDS = VO["words"]
END = 63.6

# scene windows on the root timeline
SCENES = [
    ("hook", 0.0, 7.32),
    ("rank", 7.32, 10.24),
    ("two", 10.24, 14.96),
    ("sites", 14.96, 21.32),
    ("arena", 21.32, 33.96),
    ("points", 33.96, 41.16),
    ("warn", 41.16, 50.88),
    ("aa", 50.88, 57.04),
    ("outro", 57.04, END),
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


AIS = [("chatgpt", "ChatGPT"), ("claude", "Claude"), ("gemini", "Gemini"), ("perplexity", "Perplexity")]

# ---------------- hook ----------------
s0, s1 = win("hook")
cw, ch, gap = 236, 472, 18
x0 = (1080 - 4 * cw - 3 * gap) // 2
html = ['    <div class="h" id="hk-t" style="top:250px;font-size:132px">Melyik AI-ra<br /><span class="ac">fizess elő?</span></div>']
js = ['tl.fromTo("#hk-t", { scale: 1.06 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);']
names = {"chatgpt": at("ChatGPT"), "claude": at("Claude", "four"), "gemini": at("Gemini", "four"), "perplexity": at("Perplexity")}
for i, (k, label) in enumerate(AIS):
    x = x0 + i * (cw + gap)
    html.append(f'''    <div class="card" id="hk-c{i}" style="left:{x}px;top:600px;width:{cw}px;height:{ch}px;overflow:hidden;background:#fff;border:0">
      <img src="assets/img/ai_{k}.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover" />
      <div id="hk-d{i}" style="position:absolute;inset:0;background:rgba(11,9,16,.78);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:150px;color:var(--accent,#9570ff)">?</div>
    </div>''')
    t = names[k] - s0
    js.append(f'tl.fromTo("#hk-c{i}", {{ y: 40 }}, {{ y: 0, duration: 0.35, ease: "expo.out" }}, {i * 0.06:.2f});')
    js.append(f'tl.to("#hk-d{i}", {{ opacity: 0, duration: 0.14 }}, {t:.3f});')
    js.append(f'tl.fromTo("#hk-c{i}", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.1, ease: "power2.out", immediateRender: false }}, {t:.3f});')
    js.append(f'tl.to("#hk-c{i}", {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {t + 0.1:.3f});')
# the question pulses on "melyiket válaszd"
js.append(f'tl.to("#hk-t .ac", {{ scale: 1.08, duration: 0.12, ease: "power2.out" }}, {at("melyiket") - s0:.3f});')
js.append(f'tl.to("#hk-t .ac", {{ scale: 1, duration: 0.3, ease: "expo.out" }}, {at("melyiket") - s0 + 0.12:.3f});')
js.append(out("#hk-t", s1 - s0 - 0.2))
js.append(f'tl.to(["#hk-c0", "#hk-c1", "#hk-c2", "#hk-c3"], {{ y: -80, opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power3.in", stagger: 0.03 }}, {s1 - s0 - 0.24:.3f});')
write("hook", "    #hk-t .ac { display: inline-block; }\n", "\n".join(html), js)

# ---------------- rank: today's #1 is next month's #2 ----------------
s0, s1 = win("rank")
order0 = ["chatgpt", "claude", "gemini", "perplexity"]
order1 = ["claude", "chatgpt", "gemini", "perplexity"]
rows_y = [420, 580, 740, 900]
html = ['    <div class="chip" id="rk-chip" style="left:0;right:0;margin:0 auto;width:fit-content;top:270px"><span id="rk-c0">Ma</span><span id="rk-c1" style="position:absolute;left:0;right:0;text-align:center;opacity:0">1 hónap múlva</span></div>']
for i, y in enumerate(rows_y):
    html.append(f'    <div class="h" id="rk-n{i}" style="left:70px;right:auto;width:110px;top:{y + 30}px;font-size:76px;text-align:left;color:{"var(--accent,#9570ff)" if i == 0 else "rgba(255,255,255,.55)"}">#{i + 1}</div>')
for k, label in AIS:
    y = rows_y[order0.index(k)]
    html.append(f'''    <div class="card" id="rk-{k}" style="left:190px;top:{y}px;width:830px;height:136px;display:flex;align-items:center;gap:28px;padding:0 28px">
      <img src="assets/img/logo_{k}.png" alt="" style="width:88px;height:88px;border-radius:20px;object-fit:cover" />
      <span style="font-weight:800;font-size:58px;letter-spacing:-0.02em">{label}</span>
    </div>''')
js = [f'tl.fromTo("#rk-chip", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "expo.out" }}, 0.02);']
for j, (k, _) in enumerate(AIS):
    js.append(f'tl.fromTo("#rk-{k}", {{ opacity: 0, x: 120 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }}, {0.04 + j * 0.06:.2f});')
swap = at("múlva") - s0
js += [f'tl.to("#rk-c0", {{ opacity: 0, duration: 0.1 }}, {swap:.3f});', f'tl.to("#rk-c1", {{ opacity: 1, duration: 0.1 }}, {swap:.3f});',
       f'tl.to("#rk-chip", {{ width: 440, duration: 0.2, ease: "power2.out" }}, {swap:.3f});']
for k, _ in AIS:
    dy = rows_y[order1.index(k)] - rows_y[order0.index(k)]
    if dy:
        js.append(f'tl.to("#rk-{k}", {{ y: {dy}, duration: 0.45, ease: "power3.inOut" }}, {swap + 0.05:.3f});')
js.append(f'tl.to("#rk-chatgpt", {{ borderColor: "#9570ff", boxShadow: "0 0 0 4px rgba(149,112,255,.9), 0 0 60px rgba(149,112,255,.6)", duration: 0.2 }}, {at("második") - s0:.3f});')
js.append(f'tl.to(["#rk-chip", "#rk-n0", "#rk-n1", "#rk-n2", "#rk-n3", "#rk-chatgpt", "#rk-claude", "#rk-gemini", "#rk-perplexity"], {{ opacity: 0, x: -120, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});')
write("rank", "", "\n".join(html), js)

# ---------------- two: at least two paid models ----------------
s0, s1 = win("two")
html = ['''    <div class="chip" id="tw-chip" style="left:0;right:0;margin:0 auto;width:fit-content;top:270px">Alapelv</div>
    <div class="h ac" id="tw-n" style="top:370px;font-size:400px;line-height:1">2+</div>
    <div class="card" id="tw-a" style="left:150px;top:820px;width:380px;height:230px;padding:30px"><div style="font-size:34px;font-weight:700;color:rgba(255,255,255,.6)">Előfizetés</div><div style="font-size:70px;font-weight:800;margin-top:10px">AI #1 <span class="ac">✓</span></div></div>
    <div class="card" id="tw-b" style="left:550px;top:820px;width:380px;height:230px;padding:30px"><div style="font-size:34px;font-weight:700;color:rgba(255,255,255,.6)">Előfizetés</div><div style="font-size:70px;font-weight:800;margin-top:10px">AI #2 <span class="ac">✓</span></div></div>
    <div class="h" id="tw-sub" style="top:1100px;font-size:62px">céges <span class="ac">előfizetés</span></div>''']
k2 = at("kettő") - s0
js = [blurin("#tw-chip", 0.02),
      f'tl.fromTo("#tw-n", {{ opacity: 0, scale: 2.4, filter: "blur(16px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }}, {k2:.3f});',
      f'tl.fromTo("#tw-a", {{ opacity: 0, x: -200, rotation: -8 }}, {{ opacity: 1, x: 0, rotation: -3, duration: 0.4, ease: "back.out(1.6)" }}, {k2 + 0.5:.3f});',
      f'tl.fromTo("#tw-b", {{ opacity: 0, x: 200, rotation: 8 }}, {{ opacity: 1, x: 0, rotation: 3, duration: 0.4, ease: "back.out(1.6)" }}, {k2 + 0.7:.3f});',
      blurin("#tw-sub", at("céges") - s0),
      f'tl.to(["#tw-chip", "#tw-n", "#tw-a", "#tw-b", "#tw-sub"], {{ opacity: 0, y: -60, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("two", "", html[0], js)

# ---------------- sites: two pages that help you decide ----------------
s0, s1 = win("sites")
html = '''    <div class="h" id="st-t" style="top:250px;font-size:96px"><span class="ac">2 oldal,</span> ami segít<br />dönteni</div>
    <div class="card" id="st-1" style="left:60px;top:560px;width:460px;height:470px;overflow:hidden;padding:0">
      <div class="bar" style="height:48px"><i></i><i></i><span style="font-size:28px">arena.ai</span></div>
      <img src="assets/img/arena_still.jpg" alt="" style="position:absolute;left:0;top:48px;width:100%;height:300px;object-fit:cover;object-position:0 0" />
      <div style="position:absolute;left:0;right:0;bottom:0;height:122px;display:flex;align-items:center;gap:18px;padding:0 24px;background:rgba(22,18,34,.96)">
        <div class="ac" style="font-size:76px;font-weight:800">1</div><div style="font-size:40px;font-weight:800;line-height:1.05">Arena<br /><span style="font-size:26px;font-weight:700;color:rgba(255,255,255,.65)">ranglista</span></div></div>
    </div>
    <div class="card" id="st-2" style="left:560px;top:560px;width:460px;height:470px;overflow:hidden;padding:0">
      <div class="bar" style="height:48px"><i></i><i></i><span style="font-size:28px">artificialanalysis.ai</span></div>
      <img src="assets/img/aa_still.jpg" alt="" style="position:absolute;left:0;top:48px;width:100%;height:300px;object-fit:cover;object-position:0 30%" />
      <div style="position:absolute;left:0;right:0;bottom:0;height:122px;display:flex;align-items:center;gap:18px;padding:0 24px;background:rgba(22,18,34,.96)">
        <div class="ac" style="font-size:76px;font-weight:800">2</div><div style="font-size:40px;font-weight:800;line-height:1.05">Artificial<br /><span style="font-size:26px;font-weight:700;color:rgba(255,255,255,.65)">Analysis</span></div></div>
    </div>'''
js = [blurin("#st-t", 0.02),
      f'tl.fromTo("#st-1", {{ opacity: 0, y: 160, rotation: -4 }}, {{ opacity: 1, y: 0, rotation: -2, duration: 0.45, ease: "back.out(1.5)" }}, {at("ajánlott") - s0:.3f});',
      f'tl.fromTo("#st-2", {{ opacity: 0, y: 160, rotation: 4 }}, {{ opacity: 1, y: 0, rotation: 2, duration: 0.45, ease: "back.out(1.5)" }}, {at("oldal", "sites") - s0:.3f});',
      f'tl.to(["#st-1", "#st-2"], {{ scale: 1.05, duration: 0.12, ease: "power2.out" }}, {at("melyiket", "sites") - s0:.3f});',
      f'tl.to(["#st-1", "#st-2"], {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {at("melyiket", "sites") - s0 + 0.12:.3f});',
      out("#st-t", s1 - s0 - 0.5),
      out("#st-2", s1 - s0 - 0.5),
      # card 1 becomes the next scene
      f'tl.to("#st-1", {{ x: -20, y: -140, scale: 2.2, rotation: 0, duration: 0.42, ease: "power3.in" }}, {s1 - s0 - 0.42:.3f});']
write("sites", "", html, js)

# ---------------- arena: the leaderboard in a bubble ----------------
s0, s1 = win("arena")
PX, PY, SC = 40, 380, 1000 / 1720  # panel position and video scale (arena.mp4 is 1720x1010)
vh = round(1010 * SC)
def P(x, y):  # arena.mp4 coords -> frame coords
    return PX + x * SC, PY + 54 + y * SC
tx0, ty0 = P(116, 290); tx1, ty1 = P(876, 1010)
cx0, cy0 = P(912, 290); cx1, cy1 = P(1672, 1010)
r1x, r1y = P(150, 472)
html = f'''    <div class="chip" id="ar-chip" style="left:0;right:0;margin:0 auto;width:fit-content;top:250px"><span class="ac">1</span> arena.ai</div>
    <div class="panel" id="ar-panel" style="top:{PY}px;height:{vh + 54}px">
      <div class="bar"><i></i><i></i><i></i><span>arena.ai/leaderboard</span></div>
      <video id="ar-v" class="clip" src="assets/video/arena.mp4" muted playsinline data-start="0" data-duration="{s1 - s0:.2f}" data-media-start="0.6" data-track-index="1" style="position:absolute;left:0;top:54px;width:1000px;height:{vh}px"></video>
    </div>
    <div class="ring" id="ar-r1" style="left:{tx0 - 6:.0f}px;top:{ty0 - 6:.0f}px;width:{tx1 - tx0 + 12:.0f}px;height:{min(ty1, PY + 54 + vh) - ty0 + 12:.0f}px;opacity:0"></div>
    <div class="ring" id="ar-r2" style="left:{cx0 - 6:.0f}px;top:{cy0 - 6:.0f}px;width:{min(cx1, 1040) - cx0 + 12:.0f}px;height:{min(cy1, PY + 54 + vh) - cy0 + 12:.0f}px;opacity:0"></div>
    <div class="tag" id="ar-l1" style="left:{tx0 + 20:.0f}px;top:{ty0 - 90:.0f}px">Szöveg</div>
    <div class="tag" id="ar-l2" style="left:{cx0 + 20:.0f}px;top:{cy0 - 90:.0f}px">Kód</div>
    <div class="card" id="ar-zoom" style="left:60px;top:1000px;width:960px;height:212px;overflow:hidden;padding:0;background:#fff;border:4px solid #9570ff">
      <img src="assets/img/zoom_arena.png" alt="" style="position:absolute;left:0;top:0;width:960px;height:auto" />
      <div id="ar-hl" style="position:absolute;left:0;top:0;width:960px;height:60px;background:rgba(149,112,255,.22);border:4px solid #9570ff;border-radius:10px;opacity:0"></div>
    </div>
    {arrow("ar-a1", 360, 1000, r1x + 40, r1y + 22, 0.25)}
    <div class="tag" id="ar-win" style="left:0;right:0;margin:0 auto;width:fit-content;top:249px;opacity:0">#1 szövegre: Claude Opus 4.6</div>'''
ft = at("feladatokra") - s0
rt = at("rangsorolódva") - s0
ot = at("Opus") - s0
js = [blurin("#ar-chip", 0.02),
      f'tl.fromTo("#ar-panel", {{ opacity: 0, scale: 0.85, y: 120 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0);',
      f'tl.fromTo("#ar-panel", {{ boxShadow: "0 0 0 3px rgba(149,112,255,.55), 0 40px 120px rgba(0,0,0,.7)" }}, {{ boxShadow: "0 0 0 8px rgba(149,112,255,.9), 0 40px 120px rgba(0,0,0,.7)", duration: 0.15, yoyo: true, repeat: 1 }}, {at("leaderboard") - s0:.3f});',
      pop("#ar-r1", ft, 1.1), pop("#ar-l1", ft + 0.05),
      pop("#ar-r2", ft + 0.5, 1.1), pop("#ar-l2", ft + 0.55),
      f'tl.to(["#ar-r2", "#ar-l2"], {{ opacity: 0, duration: 0.15 }}, {rt - 0.3:.3f});',
      f'tl.to("#ar-l1", {{ opacity: 0, duration: 0.15 }}, {rt - 0.3:.3f});',
      f'tl.fromTo("#ar-zoom", {{ opacity: 0, scale: 0.4, y: -200 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.5)" }}, {rt:.3f});',
      *draw_arrow("ar-a1", rt + 0.25),
      f'tl.fromTo("#ar-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {ot:.3f});',
      f'tl.to("#ar-chip", {{ opacity: 0, duration: 0.1 }}, {ot:.3f});',
      pop("#ar-win", ot + 0.05, 0.5),
      f'tl.to(["#ar-chip", "#ar-panel", "#ar-r1", "#ar-zoom", "#ar-a1", "#ar-win"], {{ opacity: 0, scale: 0.92, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }}, {s1 - s0 - 0.22:.3f});']
write("arena", "", html, js)

# ---------------- points: 1504 vs 1500 ----------------
s0, s1 = win("points")
t1504 = at("1504") - s0
t1500 = at("1500") - s0
t4 = at("négy", "points") - s0
bw = lambda v: round((v - 1400) / 110 * 600)
html = f'''    <div class="h" id="pt-t" style="top:250px;font-size:84px">Szöveg ranglista</div>
    <div style="position:absolute;left:60px;top:345px;right:60px;text-align:center;font-size:30px;font-weight:700;color:rgba(255,255,255,.55)" id="pt-src">arena.ai · pontszám</div>
    <div class="card" id="pt-c" style="left:40px;top:470px;width:1000px;height:600px"></div>
    <img src="assets/img/logo_claude.png" alt="" id="pt-lc" style="position:absolute;left:80px;top:560px;width:100px;height:100px;border-radius:22px;object-fit:cover" />
    <div id="pt-nc" style="position:absolute;left:200px;top:540px;font-size:40px;font-weight:800">Claude Opus 4.6</div>
    <div id="pt-bc" style="position:absolute;left:200px;top:600px;height:80px;width:{bw(1504)}px;border-radius:14px;background:var(--accent,#9570ff)"></div>
    <div id="pt-vc" style="position:absolute;left:{200 + bw(1504) + 20}px;top:600px;font-size:64px;font-weight:800;font-variant-numeric:tabular-nums">1504</div>
    <img src="assets/img/logo_gemini.png" alt="" id="pt-lg" style="position:absolute;left:80px;top:810px;width:100px;height:100px;border-radius:22px;object-fit:cover" />
    <div id="pt-ng" style="position:absolute;left:200px;top:790px;font-size:40px;font-weight:800">Gemini 3.1 Pro</div>
    <div id="pt-bg" style="position:absolute;left:200px;top:850px;height:80px;width:{bw(1500)}px;border-radius:14px;background:#5d5a6e"></div>
    <div id="pt-vg" style="position:absolute;left:{200 + bw(1500) + 20}px;top:850px;font-size:64px;font-weight:800;font-variant-numeric:tabular-nums">1500</div>
    <div class="tag" id="pt-d" style="left:300px;top:975px;font-size:46px;height:80px">Csak 4 pont különbség!</div>'''
js = [blurin("#pt-t", 0.02), blurin("#pt-src", 0.1), f'tl.fromTo("#pt-c", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, 0.05);',
      blurin("#pt-lc", t1504 - 0.1), blurin("#pt-nc", t1504 - 0.1),
      f'tl.fromTo("#pt-bc", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.7, ease: "expo.out" }}, {t1504:.3f});',
      f'tl.fromTo("#pt-vc", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {t1504:.3f});',
      f'tl.fromTo("#pt-vc", {{ innerText: 1400 }}, {{ innerText: 1504, snap: {{ innerText: 1 }}, duration: 0.7, ease: "expo.out" }}, {t1504:.3f});',
      blurin("#pt-lg", t1500 - 0.1), blurin("#pt-ng", t1500 - 0.1),
      f'tl.fromTo("#pt-bg", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.7, ease: "expo.out" }}, {t1500:.3f});',
      f'tl.fromTo("#pt-vg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {t1500:.3f});',
      f'tl.fromTo("#pt-vg", {{ innerText: 1400 }}, {{ innerText: 1500, snap: {{ innerText: 1 }}, duration: 0.7, ease: "expo.out" }}, {t1500:.3f});',
      pop("#pt-d", t4, 0.5),
      f'tl.to(["#pt-bc", "#pt-bg"], {{ boxShadow: "0 0 40px rgba(149,112,255,.9)", duration: 0.2 }}, {t4:.3f});',
      f'tl.to(["#pt-t", "#pt-src", "#pt-c", "#pt-lc", "#pt-nc", "#pt-bc", "#pt-vc", "#pt-lg", "#pt-ng", "#pt-bg", "#pt-vg", "#pt-d"], {{ opacity: 0, x: -120, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("points", "", html, js)

# ---------------- warn: don't cancel on the spot ----------------
s0, s1 = win("warn")
tj = at("jobb", "warn") - s0
tl_ = at("lemondod") - s0
te = at("előfizetsz") - s0
tk = at("Ki", "warn") - s0
html = '''    <div class="chip" id="wn-chip" style="left:0;right:0;margin:0 auto;width:fit-content;top:250px">⚠ Gyakori hiba</div>
    <div class="card" id="wn-phone" style="left:200px;top:400px;width:680px;height:700px;padding:40px">
      <div style="font-size:44px;font-weight:800">Előfizetéseim</div>
      <div style="margin-top:36px;height:150px;border-radius:22px;background:rgba(255,255,255,.06);display:flex;align-items:center;gap:24px;padding:0 24px">
        <img src="assets/img/logo_gemini.png" alt="" style="width:96px;height:96px;border-radius:22px;object-fit:cover" />
        <div><div style="font-size:42px;font-weight:800">Gemini</div><div style="font-size:30px;font-weight:700;color:#7fe0a0">Aktív</div></div>
      </div>
      <div id="wn-btn" style="margin-top:30px;height:110px;border-radius:22px;border:3px solid rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800">Lemondás</div>
      <div id="wn-new" style="margin-top:30px;height:110px;border-radius:22px;background:var(--accent,#9570ff);color:#0b0910;display:flex;align-items:center;justify-content:center;gap:18px;font-size:40px;font-weight:800;opacity:0">
        <img src="assets/img/logo_claude.png" alt="" style="width:64px;height:64px;border-radius:14px;object-fit:cover" />Előfizetés: Claude</div>
    </div>
    <div class="tag" id="wn-toast" style="left:120px;top:330px;font-size:38px;opacity:0">„Szövegre most a Claude jobb!”</div>
    <svg id="wn-cur" style="position:absolute;left:0;top:0;opacity:0" width="70" height="90" viewBox="0 0 24 30"><path d="M2 2 L2 24 L8 18 L12 28 L16 26 L12 17 L20 17 Z" fill="#fff" stroke="#0b0910" stroke-width="1.6" stroke-linejoin="round"/></svg>
    <div id="wn-x" style="position:absolute;left:170px;top:370px;width:740px;height:760px;opacity:0">
      <div style="position:absolute;left:-40px;top:360px;width:820px;height:34px;border-radius:17px;background:#ff5a6e;transform:rotate(43deg)"></div>
      <div style="position:absolute;left:-40px;top:360px;width:820px;height:34px;border-radius:17px;background:#ff5a6e;transform:rotate(-43deg)"></div>
    </div>
    <div class="h" id="wn-ok" style="top:1060px;font-size:84px;opacity:0">Előbb <span class="ac">próbáld ki!</span></div>'''
js = [blurin("#wn-chip", 0.02),
      f'tl.fromTo("#wn-phone", {{ opacity: 0, y: 140, rotation: 3 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.4)" }}, 0.1);',
      pop("#wn-toast", tj - 0.3, 0.5),
      f'tl.fromTo("#wn-cur", {{ opacity: 0, x: 900, y: 1300 }}, {{ opacity: 1, x: 560, y: 760, duration: 0.6, ease: "power3.inOut" }}, {tl_ - 0.6:.3f});',
      f'tl.to("#wn-cur", {{ scale: 0.85, duration: 0.06 }}, {tl_:.3f});', f'tl.to("#wn-cur", {{ scale: 1, duration: 0.15 }}, {tl_ + 0.06:.3f});',
      f'tl.to("#wn-btn", {{ backgroundColor: "rgba(255,90,110,.25)", borderColor: "#ff5a6e", color: "#ff5a6e", duration: 0.12 }}, {tl_:.3f});',
      f'tl.fromTo("#wn-new", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.8)" }}, {te:.3f});',
      f'tl.to("#wn-cur", {{ x: 560, y: 900, duration: 0.3, ease: "power2.inOut" }}, {te:.3f});',
      f'tl.fromTo("#wn-x", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "expo.out" }}, {te + 0.6:.3f});',
      f'tl.to("#wn-phone", {{ opacity: 0.45, duration: 0.2 }}, {te + 0.6:.3f});',
      f'tl.to("#wn-cur", {{ opacity: 0, duration: 0.15 }}, {te + 0.6:.3f});',
      f'tl.to("#wn-toast", {{ opacity: 0, duration: 0.15 }}, {te + 0.6:.3f});',
      f'tl.fromTo("#wn-ok", {{ opacity: 0, scale: 1.5, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.26, ease: "expo.out" }}, {te + 0.8:.3f});',
      f'tl.to(["#wn-chip", "#wn-phone", "#wn-x", "#wn-ok"], {{ opacity: 0, y: -60, filter: "blur(10px)", duration: 0.18, ease: "power3.in" }}, {s1 - s0 - 0.2:.3f});']
write("warn", "", html, js)

# ---------------- aa: speed and price ----------------
s0, s1 = win("aa")
def Q(x, y):
    return PX + x * SC, PY + 54 + y * SC
ix0, iy0 = Q(60, 320); ix1, iy1 = Q(579, 750)
sx0, sy0 = Q(599, 320); sx1, sy1 = Q(1118, 750)
px0, py0 = Q(1138, 320); px1, py1 = Q(1657, 750)
tg = at("gyorsaság") - s0
ta = at("árazás") - s0
tn = at("artificialanalysis") - s0
ring = lambda rid, a, b, c, d: f'<div class="ring" id="{rid}" style="left:{a - 6:.0f}px;top:{b - 6:.0f}px;width:{c - a + 12:.0f}px;height:{d - b + 12:.0f}px;opacity:0"></div>'
html = f'''    <div class="chip" id="aa-chip" style="left:0;right:0;margin:0 auto;width:fit-content;top:250px"><span class="ac">2</span> artificialanalysis.ai</div>
    <div class="panel" id="aa-panel" style="top:{PY}px;height:{vh + 54}px">
      <div class="bar"><i></i><i></i><i></i><span>artificialanalysis.ai</span></div>
      <video id="aa-v" class="clip" src="assets/video/aa.mp4" muted playsinline data-start="0" data-duration="{s1 - s0:.2f}" data-media-start="1.6" data-track-index="1" style="position:absolute;left:0;top:54px;width:1000px;height:{vh}px"></video>
    </div>
    {ring("aa-ri", ix0, iy0, ix1, iy1)}
    {ring("aa-rs", sx0, sy0, sx1, sy1)}
    {ring("aa-rp", px0, py0, px1, py1)}
    <div class="tag" id="aa-li" style="left:70px;top:1090px;opacity:0">Okosság</div>
    <div class="tag" id="aa-ls" style="left:380px;top:1090px;opacity:0">Gyorsaság</div>
    <div class="tag" id="aa-lp" style="left:780px;top:1090px;opacity:0">Ár</div>
    {arrow("aa-ai", 180, 1086, (ix0 + ix1) / 2, iy1 + 10, -0.15)}
    {arrow("aa-as", 520, 1086, (sx0 + sx1) / 2, sy1 + 10, 0.0)}
    {arrow("aa-ap", 850, 1086, (px0 + px1) / 2, py1 + 10, 0.15)}'''
js = [blurin("#aa-chip", tn - 0.05),
      f'tl.fromTo("#aa-panel", {{ opacity: 0, scale: 0.85, y: 120 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0);',
      pop("#aa-ri", tn + 0.6, 1.1), pop("#aa-li", tn + 0.65), *draw_arrow("aa-ai", tn + 0.7),
      pop("#aa-rs", tg, 1.1), pop("#aa-ls", tg + 0.05), *draw_arrow("aa-as", tg + 0.1),
      pop("#aa-rp", ta, 1.1), pop("#aa-lp", ta + 0.05), *draw_arrow("aa-ap", ta + 0.1),
      f'tl.to(["#aa-chip", "#aa-panel", "#aa-ri", "#aa-rs", "#aa-rp", "#aa-li", "#aa-ls", "#aa-lp", "#aa-ai", "#aa-as", "#aa-ap"], {{ opacity: 0, scale: 0.92, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }}, {s1 - s0 - 0.22:.3f});']
write("aa", "", html, js)

# ---------------- outro: don't get attached, keep testing ----------------
s0, s1 = win("outro")
tt = at("tesztelj") - s0
cw2, ch2 = 220, 440
x0 = (1080 - 4 * cw2 - 3 * 20) // 2
html = ['    <div class="h" id="ou-t1" style="top:250px;font-size:100px">Ne ragaszkodj<br />egy modellhez.</div>',
        '    <div class="h" id="ou-t2" style="top:1060px;font-size:96px;opacity:0"><span class="ac">Tesztelj</span> folyamatosan!</div>']
for i, (k, _) in enumerate(AIS):
    html.append(f'''    <div class="card" id="ou-c{i}" style="left:{x0 + i * (cw2 + 20)}px;top:540px;width:{cw2}px;height:{ch2}px;overflow:hidden;background:#fff;border:0">
      <img src="assets/img/ai_{k}.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover" /></div>''')
js = [blurin("#ou-t1", 0.02)]
for i in range(4):
    js.append(f'tl.fromTo("#ou-c{i}", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, {0.15 + i * 0.07:.2f});')
step = cw2 + 20
# the cards shuffle on "tesztelj": 0<->2 and 1<->3, then back
js += [f'tl.to("#ou-c0", {{ x: {2 * step}, y: -40, duration: 0.45, ease: "power3.inOut" }}, {tt:.3f});',
       f'tl.to("#ou-c2", {{ x: {-2 * step}, y: 40, duration: 0.45, ease: "power3.inOut" }}, {tt:.3f});',
       f'tl.to("#ou-c1", {{ x: {2 * step}, y: 40, duration: 0.45, ease: "power3.inOut" }}, {tt + 0.5:.3f});',
       f'tl.to("#ou-c3", {{ x: {-2 * step}, y: -40, duration: 0.45, ease: "power3.inOut" }}, {tt + 0.5:.3f});',
       f'tl.to(["#ou-c0", "#ou-c1", "#ou-c2", "#ou-c3"], {{ y: 0, duration: 0.3, ease: "back.out(2)" }}, {tt + 1.0:.3f});',
       f'tl.fromTo("#ou-t2", {{ opacity: 0, scale: 1.5, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.26, ease: "expo.out" }}, {tt:.3f});']
write("outro", "", "\n".join(html), js)

# ---------------- captions ----------------
ACCENT = {"válaszd", "chatgpt", "claude", "gemini", "perplexity", "legjobb", "második", "kettő", "céges", "előfizetésed", "két",
          "arena", "leaderboard", "feladatokra", "opus", "4.6-ot", "legjobbnak", "1504", "1500", "négy", "pontnyi", "lemondod",
          "próbálni", "artificialanalysis.ai", "gyorsaság", "árazás", "kötődj", "tesztelj", "claude-ra"}
FUNC = {"a", "az", "egy", "hogy", "és", "de", "ami", "meg", "is", "ha", "nem", "van", "akkor", "ilyen", "ezek", "mert", "ide", "sem", "most"}
groups, cur = [], []
for w in WORDS:
    if cur:
        prev = cur[-1]
        txt = " ".join(x["text"] for x in cur + [w])
        content = [x for x in cur if x["text"].lower().strip(",.?!") not in FUNC]
        if (prev["text"][-1] in ",.?!" or w["start"] - prev["end"] > 0.18 or w["beat"] != prev["beat"]
                or (prev["text"].lower().strip(",.?!") not in FUNC and (len(content) >= 2 or len(txt) > 16)) or len(txt) > 22):
            groups.append(cur)
            cur = []
    cur.append(w)
groups.append(cur)
ch, cj = [], []
for gi, g in enumerate(groups):
    st = round(max(0.1, g[0]["start"] - 0.04), 3)
    nx = groups[gi + 1][0]["start"] - 0.04 if gi + 1 < len(groups) else END
    en = round(min(nx, g[-1]["end"] + 0.4), 3)
    AC = ' class="ac"'
    spans = " ".join("<span%s>%s</span>" % (AC if w["text"].lower().strip(",.?!„”") in ACCENT else "", w["text"].rstrip(",."))
                     for w in g)
    gid = f"cap-{gi + 1}"
    ch.append(f'    <div id="{gid}" class="clip grp" data-start="{st}" data-duration="{round(en - st, 3)}" data-track-index="0"><div class="in" id="{gid}-in">{spans}</div></div>')
    cj.append(f'tl.fromTo("#{gid}-in", {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "back.out(2.2)" }}, {st});')
cap = f"""<template>
  <style>
{FONTS}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .grp {{ position: absolute; left: 0; right: 0; top: 1236px; height: 100px; text-align: center; overflow: visible; }}
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
def fx(name, f, t, d, v, tr=5):
    sfx.append(f'      <audio id="sfx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t:.3f}" data-duration="{d}" data-track-index="{tr}" data-volume="{v}"></audio>')
for i, k in enumerate(["chatgpt", "claude", "gemini", "perplexity"]):
    fx(f"pop{i}", "pop", names[k], 0.72, 0.35, 5 + i % 2)
for j, (c, a, b) in enumerate(SCENES[1:], 1):
    fx(f"cut{j}", "whoosh" if j % 2 else "whoosh-short", a - 0.12, 0.57, 0.35, 7)
fx("two", "ping", at("kettő"), 0.6, 0.3)
fx("click", "click", at("lemondod"), 0.36, 0.6)
sfx.append(f'      <audio id="sfx-x" class="clip" src="assets/sfx/error.mp3" data-start="{at("előfizetsz") + 0.6:.3f}" data-duration="0.4" data-media-start="0.58" data-track-index="5" data-volume="0.35"></audio>')
fx("zoom", "pop", at("rangsorolódva"), 0.72, 0.3)
fx("win", "ping", at("Opus") + 0.1, 0.6, 0.25, 6)
fx("diff", "impact-bass-1", at("négy", "points"), 2.1, 0.3, 6)
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

      <audio id="vo" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="62" data-track-index="3" data-volume="1"></audio>
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
