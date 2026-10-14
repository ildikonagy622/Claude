"""Generate index.html + compositions/captions.html for ai-fluency-narr-1 from cards.py (+ build/scenes.py for the B-roll).

Run from the project root:  python3 build/gen.py
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cards import BROLL, CARDS, DURATION, ICONS, VOICE_END  # noqa: E402
import re  # noqa: E402


def icon_svg(name):
    raw = open(os.path.join(ROOT, "assets", "icons", f"{name}.svg"), encoding="utf-8").read()
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S).strip()
    head, rest = raw.split(">", 1)  # strip sizing from the root <svg> only, never from <rect>
    raw = re.sub(r'\s(class|width|height)="[^"]*"', "", head) + ">" + rest
    raw = raw.replace('stroke-width="2"', 'stroke-width="1.3"')
    return re.sub(r"\s+", " ", raw)

MUSIC = 0.053  # bed gain: music -10.5 LUFS -> ~-36 LUFS, ~20 dB under the -16 LUFS voice
LEAD = 0.06  # a card appears this much before its first spoken word
MAX_HOLD = 2.2  # a card never lingers longer than this after its last line lands

FONT_FACES = """      @font-face {
        font-family: "Inter Tight";
        src: url("{p}assets/fonts/InterTight-800.ttf") format("truetype");
        font-weight: 800;
        font-style: normal;
      }
      @font-face {
        font-family: "Bodoni Moda";
        src: url("{p}assets/fonts/BodoniModa-Italic-400.ttf") format("truetype");
        font-weight: 400;
        font-style: italic;
      }"""

cards = []
for i, lines in enumerate(CARDS):
    start = max(0.0, lines[0][2] - LEAD)
    if i + 1 < len(CARDS):
        end = min(CARDS[i + 1][0][2] - LEAD, lines[-1][2] + MAX_HOLD)
    else:
        end = VOICE_END
    cards.append({"start": round(start, 2), "end": round(end, 2), "lines": lines})

card_html = []
for i, c in enumerate(cards):
    rows = []
    for j, (kind, text, _t) in enumerate(c["lines"]):
        cls = "ln-m" if kind == "m" else "ln-e"
        rows.append(f'          <div class="ln {cls}" id="cap-c{i}l{j}"><span>{html.escape(text)}</span></div>')
    if i in ICONS:
        rows.append(f'          <div class="ico" id="cap-c{i}ico">{icon_svg(ICONS[i][1])}</div>')
    card_html.append(
        f'        <div class="cap-inner clip" id="cap-c{i}" data-start="{c["start"]}" '
        f'data-duration="{round(c["end"] - c["start"], 2)}" data-track-index="0">\n'
        + "\n".join(rows)
        + "\n        </div>"
    )

timing = [
    {
        "id": f"cap-c{i}",
        "start": c["start"],
        "end": c["end"],
        "lines": [{"id": f"cap-c{i}l{j}", "kind": k, "t": t} for j, (k, _x, t) in enumerate(c["lines"])],
        "icon": ({"id": f"cap-c{i}ico", "line": ICONS[i][0]} if i in ICONS else None),
    }
    for i, c in enumerate(cards)
]

captions = f"""<!doctype html>
<html lang="hu">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{FONT_FACES.replace("{p}", "")}
        #captions {{
          position: absolute;
          inset: 0;
          pointer-events: none;
        }}
        .cap-inner {{
          position: absolute;
          left: 60px;
          right: 60px;
          top: 1180px;
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          color: #fffdf8;
          text-shadow: 0 2px 22px rgba(12, 8, 20, 0.28);
        }}
        .ln {{
          display: block;
          width: 100%;
          white-space: nowrap;
          transform-origin: 50% 60%;
        }}
        .ln > span {{
          display: inline-block;
        }}
        .ico {{
          position: absolute;
          left: 0;
          top: 0;
          width: 108px;
          height: 108px;
          color: #fffdf8;
          filter: drop-shadow(0 2px 14px rgba(12, 8, 20, 0.3));
        }}
        .ico svg {{
          display: block;
          width: 100%;
          height: 100%;
        }}
        .ln-m {{
          font-family: "Inter Tight", sans-serif;
          font-weight: 800;
          font-size: 94px;
          line-height: 0.9;
          letter-spacing: -0.045em;
        }}
        .ln-e {{
          font-family: "Bodoni Moda", serif;
          font-style: italic;
          font-weight: 400;
          font-size: 136px;
          line-height: 0.82;
          letter-spacing: -0.025em;
          margin: -0.06em 0 -0.02em;
        }}
      </style>

      <div id="captions" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(card_html)}
      </div>

      <script>
        (function () {{
          const CARDS = {json.dumps(timing)};
          const MAX_W = 960;

          function fitLines() {{
            document.querySelectorAll("#captions .ln > span").forEach((span) => {{
              const w = span.getBoundingClientRect().width;
              if (w > MAX_W) {{
                const ln = span.parentElement;
                const size = parseFloat(getComputedStyle(ln).fontSize);
                ln.style.fontSize = (size * MAX_W) / w + "px";
              }}
            }});
          }}

          // Park each icon beside its line (right side, vertically centred on the glyphs);
          // when the line leaves no room, centre it above the card instead.
          function placeIcons() {{
            CARDS.forEach((c) => {{
              if (!c.icon) return;
              const card = document.getElementById(c.id);
              const ico = document.getElementById(c.icon.id);
              const span = document.querySelector("#" + c.lines[c.icon.line].id + " > span");
              const cr = card.getBoundingClientRect();
              const sr = span.getBoundingClientRect();
              const S = 108, GAP = 22, EDGE = 1080 - 40;
              let x = sr.right - cr.left + GAP;
              let y = sr.top - cr.top + (sr.height - S) / 2 - 6;
              if (cr.left + x + S > EDGE) {{
                x = (cr.width - S) / 2;
                y = -S - 18;
              }}
              ico.style.left = x + "px";
              ico.style.top = y + "px";
            }});
          }}

          function build() {{
            fitLines();
            placeIcons();
            const tl = gsap.timeline({{ paused: true }});
            CARDS.forEach((c) => {{
              c.lines.forEach((l) => {{
                const el = "#" + l.id;
                const at = Math.max(c.start, l.t - 0.04);
                if (l.kind === "e") {{
                  tl.fromTo(
                    el,
                    {{ opacity: 0, scale: 1.06, y: 10, filter: "blur(6px)" }},
                    {{ opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }},
                    at
                  );
                }} else {{
                  tl.fromTo(
                    el,
                    {{ opacity: 0, scale: 0.97, y: 8 }},
                    {{ opacity: 1, scale: 1, y: 0, duration: 0.32, ease: "power2.out" }},
                    at
                  );
                }}
              }});
              let iconEnd = 0;
              if (c.icon) {{
                const at = Math.max(c.start, c.lines[c.icon.line].t + 0.08);
                tl.fromTo(
                  "#" + c.icon.id,
                  {{ opacity: 0, scale: 0.82, rotation: -10 }},
                  {{ opacity: 1, scale: 1, rotation: 0, duration: 0.55, ease: "power3.out" }},
                  at
                );
                iconEnd = at + 0.55;
              }}
              // Exit: fade every line of the card together just before the next card.
              tl.to(
                c.lines.map((l) => "#" + l.id).concat(c.icon ? ["#" + c.icon.id] : []),
                {{ opacity: 0, duration: 0.16, ease: "power1.in" }},
                Math.max(
                  c.start + 0.3,
                  c.end - 0.16,
                  iconEnd,
                  ...c.lines.map((l) => Math.max(c.start, l.t - 0.04) + (l.kind === "e" ? 0.5 : 0.32))
                )
              );
            }});
            window.__timelines["captions"] = tl;
          }}

          if (document.fonts && document.fonts.ready) {{
            document.fonts.ready.then(build);
          }} else {{
            build();
          }}
        }})();
      </script>
    </template>
  </body>
</html>
"""

FADE_AT = round(DURATION - 2.5, 2)
BROLL_HTML = "\n".join(
    f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
    f'data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="3" '
    f'data-width="1080" data-height="1920"></div>'
    for cid, a, b in BROLL
)
MUSIC_AUTOMATION = json.dumps(
    {"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": 1.2, "v": MUSIC}, {"t": FADE_AT, "v": MUSIC}, {"t": DURATION, "v": 0}]}]}
)
index = f"""<!doctype html>
<html lang="hu">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
{FONT_FACES.replace("{p}", "")}
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #0b0a10;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #0b0a10;
      }}
      /* One continuous stage behind every B-roll scene: the script1-front insert backdrop. */
      #stage {{
        position: absolute;
        inset: 0;
        overflow: hidden;
      }}
      #glow {{
        position: absolute;
        left: -20%;
        top: -10%;
        width: 140%;
        height: 100%;
        background: radial-gradient(ellipse 58% 48% at 50% 38%, #2a1d52 0%, #150f2a 55%, rgba(11, 10, 16, 0) 100%);
      }}
      #grid {{
        position: absolute;
        left: -90px;
        top: -90px;
        width: 1260px;
        height: 2100px;
        background-image:
          linear-gradient(rgba(255, 253, 248, 0.05) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255, 253, 248, 0.05) 1px, transparent 1px);
        background-size: 90px 90px;
        background-position: 45px 30px;
      }}
      /* Soft low-frame shade under the captions. Not a caption box. */
      #shade {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(
          180deg,
          rgba(10, 8, 16, 0) 52%,
          rgba(10, 8, 16, 0.32) 66%,
          rgba(10, 8, 16, 0.4) 80%,
          rgba(10, 8, 16, 0.2) 100%
        );
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{DURATION}"
      data-width="1080"
      data-height="1920"
    >
      <div id="stage">
        <div id="glow"></div>
        <div id="grid"></div>
      </div>
      <audio
        id="voice"
        src="assets/audio/voice.m4a"
        data-start="0"
        data-duration="{VOICE_END}"
        data-track-index="0"
        data-volume="1"
      ></audio>
      <audio
        id="music"
        src="assets/audio/music.mp3"
        data-start="0"
        data-duration="{DURATION}"
        data-track-index="1"
        data-volume="1"
        data-automation='{MUSIC_AUTOMATION}'
      ></audio>
{BROLL_HTML}
      <div id="shade"></div>
      <div
        id="captions"
        data-composition-id="captions"
        data-composition-src="compositions/captions.html"
        data-track-kind="captions"
        data-start="0"
        data-duration="{VOICE_END}"
        data-track-index="2"
        data-width="1080"
        data-height="1920"
      ></div>
    </div>
    <script>
      const DURATION = {DURATION};
      const tl = gsap.timeline({{ paused: true }});
      // The stage never cuts: the glow breathes and the grid drifts one cell over the whole film.
      tl.fromTo("#stage", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power1.out" }}, 0);
      tl.fromTo("#grid", {{ x: 0, y: 0 }}, {{ x: -45, y: -90, duration: DURATION, ease: "none" }}, 0);
      tl.fromTo("#glow", {{ xPercent: -4, scale: 1 }}, {{ xPercent: 4, scale: 1.08, duration: DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);
      tl.to("#stage", {{ opacity: 0, duration: 0.6, ease: "power1.in" }}, DURATION - 0.6);
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
with open(os.path.join(ROOT, "compositions", "captions.html"), "w", encoding="utf-8") as f:
    f.write(captions)
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index)
print(f"wrote index.html + compositions/captions.html: {len(cards)} cards, {DURATION}s")
