# Caption cards for ai-fluency-narr-1.
# Each card: list of (kind, text, t) — kind "m" = main sans line, "e" = emphasis serif italic line,
# t = output-timeline second when the line arrives: word onset from whisper large-v3 (build/words.json),
# shifted -4.34 s after the retake cut at 34.76 s.
CARDS = [
    [("m", "Gyakran nem tudják", 0.14), ("m", "a felhasználók,", 1.11)],
    [("m", "hogy melyik", 1.96), ("e", "AI-eszközt", 2.56), ("m", "mire érdemes használni.", 3.11)],
    [("m", "Például, hogy mivel", 4.74), ("m", "készítsünk", 5.61)],
    [("m", "egy dokumentumból", 6.12), ("e", "összefoglalót,", 6.94)],
    [("m", "hogyan használjuk", 7.98), ("m", "az AI-t", 8.87)],
    [("m", "egy kampány", 9.21), ("e", "megtervezéséhez,", 9.77)],
    [("m", "vagy mivel", 11.04), ("m", "dolgoztassunk át", 11.58), ("e", "egy szöveget", 12.48)],
    [("m", "úgy, hogy közben", 13.14), ("e", "megmaradjon", 13.98), ("m", "az eredeti stílusa.", 14.64)],
    [("m", "Az", 16.00), ("e", "AI Fluency", 16.15), ("m", "képzésen megtudod,", 16.84)],
    [("m", "hogy a", 18.14), ("e", "ChatGPT,", 18.53), ("m", "a Gemini, a Claude,", 19.14)],
    [("m", "a Perplexity és a", 20.29), ("e", "NotebookLM", 21.36)],
    [("m", "eszközöket milyen", 22.43), ("e", "feladatokra", 23.54)],
    [("m", "érdemes használnod", 24.18), ("m", "a munkád során,", 25.09)],
    [("m", "gyakorolhatod", 26.04), ("m", "a pontos", 26.81), ("e", "feladatkiadási", 27.22), ("m", "folyamatokat,", 28.05)],
    [("m", "az eredmények", 28.82), ("e", "ellenőrzését,", 29.53)],
    [("m", "és hogy mit érdemes", 30.58), ("e", "kiadni", 31.68), ("m", "az AI-nak,", 32.09)],
    [("m", "és mi az, ami", 32.70), ("m", "jobb, ha", 33.39), ("e", "nálad marad.", 33.87)],
    [("m", "Kipróbálhatsz", 35.10), ("m", "különböző", 35.91), ("e", "ellenőrzési", 36.47)],
    [("m", "és", 37.15), ("e", "kutatási", 37.27), ("m", "technikákat is.", 37.77)],
    [("m", "A képzés", 39.04), ("e", "három élő", 39.56), ("m", "alkalomból áll,", 40.14)],
    [("m", "összesen", 41.18), ("e", "hat órában.", 41.76)],
]

VOICE_END = 43.90  # narration (and the captions) end here
CTA = 3.0  # closing call-to-action card, its own page after the voice
DURATION = round(VOICE_END + CTA, 2)

# card index -> (line index the icon sits beside, Lucide icon name in assets/icons/)
ICONS = {
    3: (1, "file-text"),
    5: (1, "megaphone"),
    6: (2, "pen-line"),
    8: (1, "sparkles"),
    11: (1, "target"),
    13: (2, "route"),
    14: (1, "circle-check"),
    17: (2, "search-check"),
    19: (1, "calendar"),
    20: (1, "clock"),
}

# (composition id, start, end) on the output timeline — back to back, the whole film is B-roll.
BROLL = [
    ("broll-match", 0.00, 4.62),      # melyik AI-eszközt mire? — tangled tool → task lines
    ("broll-doc", 4.62, 7.88),        # dokumentumból összefoglaló
    ("broll-campaign", 7.88, 10.96),  # kampány megtervezése
    ("broll-rewrite", 10.96, 15.92),  # átdolgozás, megmarad a stílus
    ("broll-brand", 15.92, 18.06),    # AI Fluency képzés
    ("broll-tools", 18.06, 25.98),    # eszközök → feladatok, tiszta párosítás
    ("broll-flow", 25.98, 30.52),     # feladatkiadás → eredmény → ellenőrzés
    ("broll-split", 30.52, 34.74),    # AI-nak kiadni vs. nálad marad
    ("broll-verify", 34.74, 38.98),   # ellenőrzési és kutatási technikák
    ("broll-sessions", 38.98, 43.90), # 3 élő alkalom, 6 óra
    ("broll-cta", 43.90, 46.90),      # Kattints és nézd meg a részleteket!
]
