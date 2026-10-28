"""Speed-ramp lanes for the split screen. Both halves of a pair get the same lane,
so they consume source time identically and every move stays in sync.

Each ramp is a list of (timeline seconds, rate) holds; rates change over XF seconds.
Prints the lane JSON and how much source each ramp consumes (log interpolation, as the runtime does)."""
import json, math

XF = 0.08

def lane(holds, total):
    pts = []
    for i, (t, v) in enumerate(holds):
        if i == 0:
            pts.append({"t": 0, "v": v})
        else:
            pts.append({"t": round(t, 3), "v": v})
        nxt = holds[i + 1][0] if i + 1 < len(holds) else total
        pts.append({"t": round(nxt - XF if i + 1 < len(holds) else total, 3), "v": v})
    return pts

def consumed(pts):
    s = 0.0
    for a, b in zip(pts, pts[1:]):
        dt = b["t"] - a["t"]
        if dt <= 0:
            continue
        v0, v1 = a["v"], b["v"]
        s += v0 * dt if abs(v1 - v0) < 1e-9 else (v1 - v0) * dt / math.log(v1 / v0)
    return s

B = 0.49  # one beat at ~122 BPM
cook = lane([(0, 1.2), (B, 0.3), (4 * B, 1.25)], 5 * B)
plate = lane([(0, 1.8), (2 * B, 1.0), (4 * B, 0.5), (7 * B, 1.28)], 9 * B)
for name, pts, start, avail in (("cook", cook, 1.6, 3.27), ("plate", plate, 0.0, 4.77)):
    c = consumed(pts)
    print(name, "dur", pts[-1]["t"], "consumes %.3f s -> source %.3f..%.3f (available up to %.2f)" % (c, start, start + c, avail))
    print(json.dumps({"version": 1, "lanes": [{"target": "rate", "points": pts}]}))
