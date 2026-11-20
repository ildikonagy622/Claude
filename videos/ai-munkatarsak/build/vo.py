"""Cuts the voiceover from the source talk and writes the word timings for captions.

Usage: python3 build/vo.py <source.mp4>
Source times are absolute seconds in 1-vezetoi-tech-stack-vagott.mp4; the tail transcript
(build/words_src_head.json) starts at 1350 s."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = 0.0
GAP = 0.12

# (label, [(start, end), ...]) -- pieces inside one beat are joined without a gap
BEATS = [
    ("hook",    [(929.08, 933.06)]),                     # ezek olyanok, mint a zseniális, de feledékeny gyakornokok
    ("forget",  [(1005.62, 1010.30)]),                   # okos, de majdnem mindent elfelejt, amint kilépsz az ajtón ...
    ("trained", [(1010.74, 1020.88)]),                   # Custom GPT, gemek, projektek: betanított munkatársak ...
    ("clone",   [(957.30, 960.40)]),                     # digitális klónok, amik emlékeznek a szabályaidra
    ("auditor", [(1021.08, 1033.20)]),                   # NotebookLM: szigorú belső ellenőr ... hivatkozással együtt
    ("eu",      [(666.70, 675.38)]),                     # 300 oldalas EU-s pályázat ... mik a kizáró okok
    ("nohal",   [(691.97, 696.66)]),                     # ne például egy ChatGPT-t, mert ez nem hallucinál, csak a forrásból
    ("pages",   [(760.12, 764.74), (768.38, 772.48)]),   # belinkeli a 75., 78. oldalt ... le tudod ellenőrizni
]

FIX = {"elfelejttam,": "elfelejt,", "elelemek,": "LLM-ek,", "gyakornakok.": "gyakornokok.", "feledéken": "feledékeny",
       "elem,": "LM,", "elembe,": "LM-be,", "CGPT-t,": "ChatGPT-t,", "halucinál,": "hallucinál,", "brífelés": "brifelés",
       "feltöltod": "feltöltöd", "GPT": "GPT-k,", "gemek": "Gemek,", "projektek,": "Projektek:", "75-dik,": "75.,", "78-dik,": "78. oldalán.", "megkérdezett": "megkérdezed", "notebook": "Notebook", "-dik,": "-dik,"}

def main(src):
    words = json.load(open(os.path.join(ROOT, "build", "words_src_head.json")))
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
        pass
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
