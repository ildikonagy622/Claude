---
workflow: hyperframes
aspect: "9:16"
language: hu
destination: social (Reels / TikTok / Shorts)
---

## Intent

Felhasználói kérés: „ebből kérlek vágj egy ilyet” — a Drive-mappa `referencia.mp4` (ai.akshu reel, „AI influencer photos still look fake”) szerkezetében és stílusában, a `hang és a mesterprompt.mov` narrációjával, annak szövegét feliratként alátéve.

## Források (Google Drive mappa)

- `hang és a mesterprompt.mov` — narráció (7.20–24.12 s és 28.40–74.95 s; a 24.2–28.4 s közti elakadás kivágva), képe nem használt.
- `b-roll.mov` — előadó laptoppal, Amazing AI neon háttér (9:16-ra vágva).
- `készülési folyamat` — Magnific (Nano Banana Pro) felület 54.5–74 s; a két generált kép (kovács, öltöző) állóképként kivágva.
- `magnific logo.png`.
- A mesterprompt szövegek (`1. CAPTURE`, valóság réteg) a felhasználó `photoreal-portret-prompt` skilljéből, szó szerint.

## Felépítés (a referenciát követve)

hook képmontázs (≈0.55 s vágások) → „Megmutatom, hogyan csinálom” nagy cím → 1. lépés Magnific felület → mester prompt → prompt-kártya szinkron kiemelésekkel → „Valóság réteg” cím → részletek képenként, angol prompt-címkével → eredmények → két CTA („AI”, „PROMPT”).

## Stílus

- Kétszintű tipográfia: nagy, szorosan szedett Inter Tight 800 cím (2. sor kiemelő színnel) az előadós jeleneteken; 1–3 szavas felirat szavanként a többin.
- Kiemelő szín: Amazing AI neon magenta `#EE4BFF` (a referencia lime-ja helyett).
- Zene: a script1-front projekt halk alapja (`assets/audio/music.mp3`, 0.12), SFX a HyperFrames beépített készletéből.

## Szerkesztés

`build/gen.py` generálja a hook / details / results jeleneteket és a feliratsávot (`build/words_src.json` a szószintű leirat); a többi jelenet kézzel írt.
