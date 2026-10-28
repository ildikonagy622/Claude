---
workflow: hyperframes
aspect: "9:16"
language: hu
destination: social (Reels / TikTok / Shorts)
---

## Intent

Osztott képernyős összehasonlítás: felül az eredeti felvétel, alul a Seedance 2.5-tel átszerkesztett (étterem) változat, címkézve. Sorrend: főzés (`főzés felső eredeti` / `főzés alsó.mov`), majd a tányér (`mutatós felső.mp4` üres tányér / `mutatós alsó.mov` kész étel). Vége: „Tetszett? Kövess be!” CTA. Zene: `zephiramusic-chill-hop-603159.mp3` (a felhasználó választása). Forrás: Drive `1Ykj0Y9O61o0ObpJZuRfTm8CclwWnX6mJ`.

## Felépítés (a zene ütéseire, ~0.7 s)

- 0–0.735 s hook: felül az otthoni főzés, alul sötét, „Otthon főztem egyet…”.
- 0.735 s: villanással előtűnik a Seedance-változat, „…az AI étterembe vitt.”, címkék: EREDETI / SEEDANCE 2.5.
- 4.905 s: váltás a tányéros párra; „Ugyanaz a mozdulat.” → „Más világ.”.
- 9.2 s: az alsó (AI) tányér kitölti a képet → CTA, követés-gomb lenyomással, 14 s-ig.

## v2 (felhasználói kérés)

- A nyitó „Otthon főztem egyet… / …az AI étterembe vitt.” felirat kivéve; a többi szöveg marad.
- CTA: „Kövess be, ha szeretnéd látni, hogyan készült!”
- Szinkron: mozgáselemzés szerint mindkét pár valós időben 1:1 egyezik, ezért a felső és az alsó videó azonos időben, azonos sebességgel indul (főzés 0.77×, tányér 0.985×); az alsó a nyitásban takarva fut, és 0.735 s-nál tűnik elő. A renderen mérve: főzés 1.00 arány, 0 képkocka eltolás.
- Felirat nélküli figyelemtartás: ránagyítás mindkét félen az előtűnéskor és a második feldobásnál (2.85 s), suhanással.

## v3 (felhasználói kérés)

- Kiemelő szín: `#9570FF` (lila) a magenta helyett.
- Első 3 s sűrítve, felirat nélkül: 0–0.735 s előtte–utána villogás teljes képernyőn (otthon → étterem → otthon → étterem → kész étel) glitch- és ütéshanggal; utána az osztott kép (+0.735 s eltolással), az AI-fél előtűnése 1.47 s-nál, ütemre lüktetés 2.1 és 2.8 s-nál, ránagyítás a második feldobásnál (~3.6 s).

## v4 (felhasználói kérés)

- Az előtte–utána villogás kivéve; a főzéses párból csak egy serpenyődobás marad (forrás 1.6 s-tól, 0.77×, 0–2.125 s), utána rögtön a tányéros pár (2.125–7.005 s), majd a CTA (11.24 s-ig).
