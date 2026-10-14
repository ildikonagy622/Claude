# Caption cards for script1-front.
# Each card: list of (kind, text, t) — kind "m" = main sans line, "e" = emphasis serif italic line,
# t = output-timeline second when the line arrives (word onset from the per-segment transcripts).
CARDS = [
    [("m", "Te milyen", 0.11), ("e", "AI-eszközt", 0.45), ("m", "használtál fél éve?", 1.15)],
    [("m", "Milyen", 2.53), ("e", "funkciói", 2.90), ("m", "voltak?", 3.52)],
    [("m", "És most mit", 4.10), ("e", "használsz?", 4.53)],
    [("m", "És milyen", 5.03), ("e", "funkciói", 5.48), ("m", "vannak?", 5.93)],
    [("m", "Az eszközök", 6.66), ("e", "változnak.", 7.19)],
    [("m", "Te", 8.08), ("e", "nem.", 8.23)],
    [("m", "Dr. Iványi Tamás", 8.80), ("e", "AI-szakértő", 10.29)],
    [("m", "egyetemi", 11.27), ("e", "adjunktus", 11.94)],
    [("m", "és pontosan ezért", 12.68)],
    [("m", "nem egy konkrét", 14.20), ("e", "eszközhasználatot", 14.88)],
    [("m", "szeretném", 15.86), ("e", "megtanítani", 16.32), ("m", "neked,", 16.96)],
    [("m", "hanem azt, hogy", 17.46), ("m", "te hogyan tudsz", 18.50), ("e", "változni", 19.38)],
    [("m", "és kialakítani", 20.03), ("m", "az AI-használati", 21.16), ("e", "képességeidet.", 22.36)],
    [("m", "Ma", 23.76), ("e", "ChatGPT,", 23.95), ("m", "holnap", 25.25), ("e", "Claude,", 25.76)],
    [("m", "aztán valami,", 26.23), ("m", "aminek ma még", 26.90)],
    [("m", "nem biztos, hogy", 27.50), ("m", "tudjuk", 28.37), ("e", "a nevét is.", 28.70)],
    [("m", "Van egy", 29.36), ("e", "képesség,", 29.68)],
    [("m", "ami nem avul el", 30.48), ("e", "ilyen gyorsan.", 31.44)],
    [("m", "Az, hogy tudsz-e jól", 32.57), ("e", "együtt dolgozni", 33.63), ("m", "az AI-jal.", 34.54)],
    [("m", "Tudod-e vezetni", 35.29), ("m", "egy összetett", 36.20), ("e", "feladaton", 37.25), ("m", "keresztül?", 37.88)],
    [("m", "Észreveszed-e, amikor", 38.63), ("m", "magabiztosan", 39.99), ("e", "vezet téged félre?", 40.83)],
    [("m", "És ki tudod-e hozni", 42.22), ("m", "belőle akkor is", 43.02), ("e", "a jó válaszokat?", 43.88)],
    [("m", "Többek között", 45.16), ("m", "ezt hívjuk", 46.22), ("e", "AI fluencynek.", 47.04)],
    [("m", "Erről tartok hamarosan", 48.32), ("m", "egy élő online", 49.89), ("e", "workshopot,", 50.76)],
    [("m", "ahol nem", 51.67), ("e", "kattintgatni", 52.08), ("m", "fogunk megtanulni,", 52.89)],
    [("m", "hanem a saját", 54.21), ("e", "emberi intelligenciánkat", 54.98), ("m", "fogjuk fejleszteni.", 56.52)],
    [("m", "Azt nézzük meg,", 57.83), ("m", "hogyan tudsz", 59.00), ("e", "tudatosabban", 59.80), ("m", "gondolkodni,", 60.56)],
    [("m", "hogy az AI", 61.58), ("e", "pontosabb és jobb", 61.89), ("m", "eredményeket adjon", 62.75)],
    [("m", "Ha már használod", 64.65), ("m", "az AI-t,", 65.93)],
    [("m", "de érzed, hogy lehetne", 66.73), ("e", "sokkal intelligensebben", 68.14), ("m", "is csinálni,", 69.47)],
    [("m", "akkor nézd meg", 70.21), ("e", "a workshop részleteit.", 70.88)],
    [("e", "Kattints,", 72.22), ("m", "és ott megtalálsz", 72.62), ("e", "minden információt.", 73.36)],
]

# Output-timeline start of each cut (seconds) — the punch-in / framing changes land here.
CUTS = [0.00, 2.46, 4.02, 6.58, 8.68, 17.38, 23.64, 26.14, 29.20, 32.46, 35.22, 38.52,
        42.12, 51.58, 57.74, 58.90, 64.56, 70.16]
DURATION = 74.64
