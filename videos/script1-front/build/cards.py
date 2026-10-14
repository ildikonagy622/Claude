# Caption cards for script1-front.
# Each card: list of (kind, text, t) — kind "m" = main sans line, "e" = emphasis serif italic line,
# t = output-timeline second when the line arrives: word onset from whisper DTW alignment of the final
# (external-mic) track, cross-checked against energy onsets after pauses.
CARDS = [
    [("m", "Te milyen", 0.05), ("e", "AI-eszközt", 0.57), ("m", "használtál fél éve?", 1.09)],
    [("m", "Milyen", 2.57), ("e", "funkciói", 2.93), ("m", "voltak?", 3.49)],
    [("m", "És most mit", 4.13), ("e", "használsz?", 4.69)],
    [("m", "És milyen", 5.21), ("e", "funkciói", 5.61), ("m", "vannak?", 6.11)],
    [("m", "Az eszközök", 6.67), ("e", "változnak.", 7.21)],
    [("m", "Te", 8.05), ("e", "nem.", 8.27)],
    [("m", "Dr. Iványi Tamás", 9.07), ("e", "AI-szakértő", 10.37)],
    [("m", "egyetemi", 11.41), ("e", "adjunktus", 11.91)],
    [("m", "és pontosan ezért", 12.81)],
    [("m", "nem egy konkrét", 14.23), ("e", "eszközhasználatot", 14.95)],
    [("m", "szeretném", 15.83), ("e", "megtanítani", 16.23), ("m", "neked,", 16.81)],
    [("m", "hanem azt, hogy", 17.45), ("m", "te hogyan tudsz", 18.49), ("e", "változni", 19.25)],
    [("m", "és kialakítani", 20.29), ("m", "az AI-használati", 21.57), ("e", "képességeidet.", 22.59)],
    [("m", "Ma", 23.81), ("e", "ChatGPT,", 24.01), ("m", "holnap", 25.25), ("e", "Claude,", 25.65)],
    [("m", "aztán valami,", 26.27), ("m", "aminek ma még", 27.01)],
    [("m", "nem biztos, hogy", 27.67), ("m", "tudjuk", 28.21), ("e", "a nevét is.", 28.45)],
    [("m", "Van azonban egy", 29.35), ("e", "képesség,", 30.01)],
    [("m", "ami nem avul el", 30.87), ("e", "ilyen gyorsan.", 31.59)],
    [("m", "Az, hogy tudsz-e jól", 32.63), ("e", "együtt dolgozni", 33.63), ("m", "az AI-jal.", 34.39)],
    [("m", "Tudod-e vezetni", 35.31), ("m", "egy összetett", 36.57), ("e", "feladaton", 37.33), ("m", "keresztül?", 37.81)],
    [("m", "Észreveszed-e, amikor", 38.63), ("m", "magabiztosan", 40.23), ("e", "vezet téged félre?", 40.95)],
    [("m", "És ki tudod-e hozni", 42.25), ("m", "belőle akkor is", 43.13), ("e", "a jó válaszokat?", 43.93)],
    [("m", "Többek között", 45.79), ("m", "ezt hívjuk", 46.59), ("e", "AI fluencynek.", 47.23)],
    [("m", "Erről tartok hamarosan", 48.79), ("m", "egy élő online", 50.01), ("e", "workshopot,", 51.01)],
    [("m", "ahol nem", 51.67), ("e", "kattintgatni", 52.11), ("m", "fogunk megtanulni,", 52.85)],
    [("m", "hanem a saját", 54.17), ("e", "emberi intelligenciánkat", 54.99), ("m", "fogjuk fejleszteni.", 56.43)],
    [("m", "Azt nézzük meg,", 57.83), ("m", "hogyan tudsz", 59.03), ("e", "tudatosabban", 59.79), ("m", "gondolkodni,", 60.49)],
    [("m", "hogy az AI", 61.57), ("e", "pontosabb és jobb", 62.17), ("m", "eredményeket adjon", 63.01)],
    [("m", "Ha már használod", 65.03), ("m", "az AI-t,", 66.03)],
    [("m", "de érzed, hogy lehetne", 66.85), ("e", "sokkal intelligensebben", 68.15), ("m", "is csinálni,", 69.35)],
    [("m", "akkor nézd meg", 70.43), ("e", "a workshop részleteit.", 70.89)],
    [("e", "Kattints,", 72.17), ("m", "és ott megtalálsz", 72.57), ("e", "minden információt.", 73.31)],
]

# Output-timeline start of each cut (seconds) — the punch-in / framing changes land here.
CUTS = [0.00, 2.46, 4.02, 6.58, 8.68, 17.38, 23.64, 26.14, 29.20, 32.46, 35.22, 38.52,
        42.12, 51.58, 57.74, 58.90, 64.56, 70.16]
DURATION = 74.64

# Thin-line icons (Lucide, ISC — assets/icons). card index -> (line index the icon sits beside, icon name).
# The icon arrives with that line, beside it on the right; if the line is too wide it sits above the card.
ICONS = {
    0: (1, "smartphone"),
    1: (1, "sliders-horizontal"),
    4: (1, "refresh-cw"),
    6: (1, "sparkles"),
    7: (1, "graduation-cap"),
    9: (1, "wrench"),
    12: (2, "trending-up"),
    13: (1, "message-circle"),
    15: (2, "circle-help"),
    16: (1, "brain"),
    17: (1, "hourglass"),
    18: (1, "handshake"),
    19: (2, "route"),
    20: (2, "triangle-alert"),
    21: (2, "circle-check"),
    22: (2, "languages"),
    23: (2, "video"),
    24: (1, "mouse-pointer-click"),
    25: (1, "lightbulb"),
    26: (2, "eye"),
    27: (1, "target"),
    29: (1, "zap"),
    30: (1, "calendar"),
    31: (0, "pointer"),
}
