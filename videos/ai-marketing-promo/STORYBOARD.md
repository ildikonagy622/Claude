---
compositionId: ai-marketing-promo
duration_s: 20.0 # == audiomap.audio.duration_sec
canvas: {"w": 1080, "h": 1920, "fps": 30}
style:
  font: "Inter Display / Inter"
  palette: ["#0C0C0E", "#1B162A", "#8B5CF6", "#B9A4FB", "#DEFD86", "#FFFFFF"]
assets: "assets/clips/ has 7 muted 1080×1920 proxies (05 is 1080×996 — place as a floating card)"
build_notes:
  - "one paused timeline per frame"
  - "no remote assets; fonts from assets/fonts via @font-face"
  - "track is 123 BPM, steady grid with hi-hat rolls → beat_cut throughout"
  - "track read: hit at 0.5s, dense 4–13s with a short dip at 7s, surge at 14s, fade-out from 18.6s"
avoid: ["generic slideshow", "tiny unreadable text", "bouncing captions", "heavy shadows"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 4.389s
- span_sec: [0.0, 4.389]
- pacing: beat_cut
- mood: [elegant, warm]
- feel: first downbeat hit at 0.5s out of a quiet lead-in, steady medium-high groove into a hi-hat fill at 4.39

### Groups

- **g1** — asset
  - span_sec: [0.0, 4.389]
  - asset: { treatment: bg_under_text, clips: [assets/clips/01-typing.mp4], anchors: [0.511, 0.998, 1.486, 1.974], overlay_copy: ["✦ Az Amazing AI online workshopja", "AI az", "online", "marketingben"] }
  - copy: "✦ Az Amazing AI online workshopja / AI az / online / marketingben" — headline in the lower third on a dark scrim; 'online marketingben' wears the lavender→lime gradient; eyebrow on 0.511, then one word-line per beat; footage opens from black on 0.511 with a slow push.

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 3.692s
- span_sec: [4.389, 8.081]
- pacing: beat_cut
- mood: [elegant]
- feel: dense hi-hat fill and accel-roll into a short dip at 7s, then a surge at 8

### Groups

- **g1** — asset
  - span_sec: [4.389, 8.081]
  - asset: { treatment: bg_under_text, clips: [assets/clips/02-logo.mp4], anchors: [4.435, 4.923, 5.898, 7.059], overlay_copy: ["Ma már egyedül is lehetsz", "egy teljes ügynökség"] }
  - copy: "Ma már egyedül is lehetsz / egy teljes ügynökség" — top third over a top-down scrim (the ChatGPT + Canva logos stay visible mid-frame); line 1 on 4.923, line 2 on 5.898 with 'teljes ügynökség' in lavender; the clip's own push-in and blur ending carry into the cut.

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 4.919s
- span_sec: [8.081, 13.0]
- pacing: beat_cut
- mood: [elegant, hype]
- feel: two sustained hi-hat fills back to back, densest stretch, ending on a hard stop at 13

### Groups

- **g1** — asset
  - span_sec: [8.081, 13.0]
  - asset: { treatment: beat_cut, clips: [assets/clips/03-chatgpt-prompt.mp4, assets/clips/04-chatgpt-plan.mp4, assets/clips/05-canva-post.mp4, assets/clips/06-ai-image.mp4], anchors: [8.081, 9.334, 10.333, 11.796], overlay_copy: ["01 · Stratégia és csalitermék", "02 · Tartalomnaptár percek alatt", "03 · Hírlevelek és posztok", "04 · Látványos kreatívok Canvával"] }
  - copy: one step label per cut, in a lower-third card (step number in lavender, title in white); a thin progress rail with 4 ticks fills one tick per cut; clip 05 (landscape crop) floats as a rounded card on the dark violet-glow ground.

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 3.231s
- span_sec: [13.0, 16.231]
- pacing: beat_cut
- mood: [elegant, hype]
- feel: brief dip at 13 then the strongest surge of the cut at 14, dense into the next downbeat

### Groups

- **g1** — asset
  - span_sec: [13.0, 16.231]
  - asset: { treatment: bg_under_text, clips: [assets/clips/07-canva-deck.mp4], anchors: [13.282, 13.769, 14.257], overlay_copy: ["Komplett kampány", "a nulláról", "4 óra alatt"] }
  - copy: "Komplett kampány / a nulláról" (gradient on 'a nulláról') lands on 13.282 / 13.769; a lime pill "4 óra alatt" snaps in on the 14.257 surge; slow push on the Canva deck footage.

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 3.769s
- span_sec: [16.231, 20.0]
- pacing: beat_cut
- mood: [elegant, warm]
- feel: final two bars, steady groove fading out from 18.6 to silence at 20

### Groups

- **g1** — free_design
  - span_sec: [16.231, 20.0]
  - free_design: { dominant_system: "branded end card on the landing page's dark ground with a breathing violet glow", primitives: ["staggered line reveal", "button press pulse"], density_topology: "accumulate then hold" }
  - anchors: [16.231, 16.718, 17.206, 17.717, 18.204, 18.692]
  - copy: ["✦ Online workshop", "2026. 10. 21.", "9:00–13:00 · Online, 100% élőben", "Jelentkezz most →", "go.amazingai.hu", "Amazing AI"] — accumulate one line per beat from 16.231; the violet CTA button lands on 17.717 and pulses softly on 18.204 / 18.692; everything holds still through the fade-out.
