"""Cuts the voiceover from the source talk and writes the word timings for captions.

Usage: python3 build/vo.py <source.mp4>
Source times are absolute seconds in 1-vezetoi-tech-stack-vagott.mp4; the tail transcript
(build/words_src_tail.json) starts at 1350 s."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = 1350.0
GAP = 0.12

# (label, [(start, end), ...]) -- pieces inside one beat are joined without a gap
BEATS = [
    ("q",        [(1493.48, 1495.95)]),                    # felmerülhet benned a kérdés, hogy oké, de melyiket válaszd
    ("four",     [(1487.95, 1492.62)]),                    # a legsűrűbben használtak ezek a ChatGPT, Claude, a Gemini és a Perplexity
    ("today",    [(1527.98, 1530.78)]),                    # ami ma a legjobb, egy hónap múlva ... csak a második lesz
    ("two",      [(1583.20, 1587.80)]),                    # legalább kettő ilyen nagynyelvi modellhez legyen céges előfizetésed
    ("sites",    [(1748.25, 1751.45), (1752.66, 1755.70)]),# van két ajánlott oldal ... hogy éppen melyiket használd
    ("arena",    [(1757.08, 1758.62)]),                    # az egyik az Arena oldala
    ("board",    [(1762.08, 1769.64)]),                    # egy ilyen leaderboard ... hogyan van rangsorolódva
    ("opus",     [(1787.48, 1788.52), (1789.68, 1791.88)]),# mondjuk szöveggenerálásban a ... Opus 4.6-ot tartják most a legjobbnak
    ("points",   [(1838.08, 1845.10)]),                    # 1504 és 1500 pont ... Claude meg a Gemini között
    ("warn",     [(1819.84, 1823.40), (1823.80, 1829.84)]),# szeretnélek attól óva inteni ... Ki lehet próbálni
    ("aa",       [(1845.18, 1846.08), (1847.96, 1849.36), (1854.18, 1856.36), (1857.24, 1858.80)]),
    ("end",      [(1619.84, 1624.74)]),                    # ne kötődj egy modellhez sem érzelmileg, folyamatosan tesztelj más modelleket is
]

FIX = {"Chagy,GPT,": "ChatGPT,", "Cloud": "Claude", "Cloud,": "Claude,", "Cloud-nél,": "Claude", "Cloud-ra.": "Claude-ra.",
       "válasz.": "válaszd?", "óváintani,": "óva inteni,", "kisitebben": "kicsit"}

def main(src):
    words = json.load(open(os.path.join(ROOT, "build", "words_src_tail.json")))
    for w in words:
        w["s"], w["e"] = w["start"] + OFF, w["end"] + OFF
    # glue suffix tokens ("-ot", ".6", "PT,") onto the word before
    glued = []
    for w in words:
        t = w["text"].strip()
        if glued and (t[:1] in "-." or t in ("PT,",)) :
            glued[-1]["text"] += t if t[:1] in "-." else "GPT,"
            glued[-1]["e"] = w["e"]
        else:
            glued.append(dict(w, text=t))
    out, beats, pieces, cur = [], [], [], 0.0
    for label, segs in BEATS:
        b0 = cur
        for i, (a, b) in enumerate(segs):
            pieces.append((a, b))
            for w in glued:
                if a - 0.02 <= w["s"] < b - 0.05:
                    out.append({"text": w["text"], "start": round(cur + max(0, w["s"] - a), 3),
                                "end": round(cur + min(b, w["e"]) - a, 3), "beat": label})
            cur += b - a
        beats.append({"id": label, "start": round(b0, 3), "end": round(cur, 3)})
        cur += GAP
    for w in out:
        if w["text"] == "a" and w["beat"] == "opus":  # "a Claude 4.6" was cut: drop that first "a" only
            w["drop"] = True
            break
    out = [w for w in out if not w.get("drop")]
    for w in out:
        w["text"] = FIX.get(w["text"], w["text"])
    seen = set()
    for w in out:  # each beat opens a sentence
        if w["beat"] not in seen:
            seen.add(w["beat"])
            w["text"] = w["text"][:1].upper() + w["text"][1:]
    # audio: each piece with 15 ms fades, beats separated by GAP of silence
    inputs, filt, labels = [], [], []
    n = 0
    for label, segs in BEATS:
        for a, b in segs:
            filt.append(f"[0:a]atrim={a}:{b},asetpts=N/SR/TB,pan=mono|c0=c0,afade=t=in:d=0.015,afade=t=out:st={b-a-0.02:.3f}:d=0.02[p{n}]")
            labels.append(f"[p{n}]"); n += 1
        filt.append(f"anullsrc=r=48000:cl=mono,atrim=0:{GAP}[g{n}]"); labels.append(f"[g{n}]"); n += 1
    labels = labels[:-1]
    filt.pop()  # the trailing gap is not used
    npieces = sum(len(segs) for _, segs in BEATS)
    filt.insert(0, "[0:a]asplit=%d%s" % (npieces, "".join(f"[s{i}]" for i in range(npieces))))
    k = 0
    for i, f in enumerate(filt):
        if f.startswith("[0:a]atrim"):
            filt[i] = f.replace("[0:a]", f"[s{k}]", 1); k += 1
    filt.append("".join(labels) + f"concat=n={len(labels)}:v=0:a=1,highpass=f=80,acompressor=threshold=-22dB:ratio=3:attack=5:release=90,loudnorm=I=-14:TP=-1.5:LRA=6,aresample=48000[o]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(filt), "-map", "[o]", "-ac", "2",
                    "-c:a", "pcm_s16le", os.path.join(ROOT, "assets", "audio", "vo.wav")], check=True)
    json.dump({"beats": beats, "words": out}, open(os.path.join(ROOT, "build", "vo.json"), "w"), ensure_ascii=False, indent=1)
    for b in beats:
        print(f'{b["id"]:7s} {b["start"]:6.2f}-{b["end"]:6.2f}  ' + " ".join(w["text"] for w in out if w["beat"] == b["id"]))

main(sys.argv[1])
