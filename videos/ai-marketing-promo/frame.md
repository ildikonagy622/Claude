---
version: alpha
name: Amazing AI — Frame (video / frame layer)
description: >
  Bespoke frame spec lifted from the go.amazingai.hu workshop landing page. Near-black canvas,
  violet as the single action color (CTA, highlights, glow), lime as the rare second accent on
  the gradient headline word, white display type in Inter Display with tight tracking, soft
  violet radial glow behind hero content, thin hairline cards on a violet-tinted surface,
  pill / rounded-rect buttons with a trailing arrow. 9:16 primary.
unit: the frame — 1080×1920 primary
principle: atoms are sacred · composition is free · copy comes from the landing page

colors:
  bg: "#0C0C0E"
  surface: "#1B162A"
  primary: "#8B5CF6"
  lavender: "#B9A4FB"
  lime: "#DEFD86"
  text: "#FFFFFF"
  text-muted: "rgba(255,255,255,0.62)"
  border: "rgba(139,92,246,0.28)"
  glow: "rgba(139,92,246,0.45)"

gradients:
  headline-accent: "linear-gradient(90deg, #B9A4FB 0%, #DEFD86 100%)"   # 'online marketingben', 'a nulláról'
  glow: "radial-gradient(closest-side, rgba(139,92,246,0.45), rgba(139,92,246,0) 70%)"

radii:
  button: "14px"
  card: "18px"
  pill: "100px"

typography:
  eyebrow: { fontFamily: "Inter", px: 34, weight: 500, color: "lavender", note: "leading ✦ / ↳ mark" }
  h1:      { fontFamily: "Inter Display", px: 150, weight: 500, lineHeight: 0.98, tracking: "-0.035em", color: "text" }
  h2:      { fontFamily: "Inter Display", px: 104, weight: 500, lineHeight: 1.02, tracking: "-0.03em", color: "text" }
  step-num:{ fontFamily: "Inter", px: 30, weight: 500, tracking: "0.04em", color: "lavender" }
  step:    { fontFamily: "Inter Display", px: 76, weight: 600, lineHeight: 1.05, tracking: "-0.02em", color: "text" }
  body:    { fontFamily: "Inter", px: 40, weight: 400, lineHeight: 1.35, color: "text-muted" }
  button:  { fontFamily: "Inter", px: 44, weight: 600, color: "text" }

fonts: # embedded, local
  - assets/fonts/InterDisplay-Medium.otf
  - assets/fonts/InterDisplay-SemiBold.otf
  - assets/fonts/InterDisplay-Bold.otf
  - assets/fonts/Inter-Regular.otf
  - assets/fonts/Inter-Medium.otf
  - assets/fonts/Inter-SemiBold.otf

components:
  cta-button: { background: "{colors.primary}", radius: "{radii.button}", padding: "34px 52px", trailing: "→ in a darker violet square" }
  card: { background: "{colors.surface}", border: "1.5px solid {colors.border}", radius: "{radii.card}" }
  footage-scrim: "linear-gradient(to top, rgba(12,12,14,0.92) 0%, rgba(12,12,14,0.55) 45%, rgba(12,12,14,0) 75%)"

dos:
  - Keep text in the lower or upper third over footage, always on a scrim.
  - Use the lavender→lime gradient only on the one accent phrase per frame.
  - Footage stays bright and real; type and glow carry the brand.
donts:
  - No heavy shadows, no thick strokes, no bouncing captions.
  - No more than one violet button on screen.
---
