"""How the track feels: groove, boredom and energy curve.

  groove   danceability (Essentia) and swing (how late the off-16ths sit):
           does it move or feel stiff?
  boredom  novelty per bar: flags stretches where nothing new happens for
           more than 16 bars
  energy   energy 1-10 per 8 bars across the whole track, and whether it
           builds and releases like a good set (intro < drop, a breakdown dip,
           second drop >= first, outro down)

Usage (Mac, the Essentia venv, which also has librosa):
  ~/producer-agent/.venv-genre/bin/python ~/producer-agent/feel.py v12.wav --bpm 126
  ... feel.py v12.wav --bpm 126 --only groove        # groove | boredom | energy
  ... feel.py v12.wav --bpm 126 --offset 0.12        # seconds before bar 1
  ... feel.py v12.wav --bpm 126 --compare ref.wav --ref-bpm 124   # groove side by side
  ... feel.py v12.wav --bpm 126 --json out.json

Prints one line per finding; FLAG lines are what the critic should act on.
"""
import argparse
import json
import os
import warnings

import librosa
import numpy as np

warnings.filterwarnings("ignore")
SR = 44100


def load(path):
    y, _ = librosa.load(os.path.expanduser(path), sr=SR, mono=True)
    return y


def danceability(y):
    try:
        import essentia
        import essentia.standard as es
        essentia.log.infoActive = False
        essentia.log.warningActive = False
    except ImportError:
        return None
    d, _ = es.Danceability(sampleRate=SR)(y.astype(np.float32))
    return float(d)


def swing(y, bpm, offset):
    """Median position of off-16th onsets inside their 8th: 50% straight, ~54-60% swung."""
    onsets = librosa.onset.onset_detect(y=y, sr=SR, units="time", backtrack=False)
    eighth = 30.0 / bpm
    pos = ((onsets - offset) / eighth) % 1.0
    off = pos[(pos > 0.3) & (pos < 0.8)]
    on = pos[(pos < 0.1) | (pos > 0.9)]
    # timing spread of on-grid hits (ms): 0 = quantised machine, a few ms = human
    spread = float(np.std(np.where(on > 0.5, on - 1, on)) * eighth * 1000) if len(on) > 8 else 0.0
    return (float(np.median(off) * 100) if len(off) >= 8 else None), spread, len(off) / max(len(onsets), 1)


def groove(y, bpm, offset):
    d = danceability(y)
    sw, spread, off_share = swing(y, bpm, offset)
    return {"danceability": None if d is None else round(d, 2),
            "swing_pct": None if sw is None else round(sw, 1),
            "timing_spread_ms": round(spread, 1),
            "off16_share": round(off_share, 2),
            "onsets_per_sec": round(len(librosa.onset.onset_detect(y=y, sr=SR)) / (len(y) / SR), 2)}


def groove_lines(g, ref=None):
    out = [f"groove: danceability {g['danceability']}, swing {g['swing_pct']}%, "
           f"off-16ths {int(g['off16_share'] * 100)}% of hits, {g['onsets_per_sec']} hits/s"]
    if g["danceability"] is not None and g["danceability"] < 1.0:
        out.append(f"FLAG groove: danceability {g['danceability']} is low (tech house drops usually read 1.2 or more)")
    if g["swing_pct"] is not None and g["swing_pct"] < 51.5 and g["timing_spread_ms"] < 1.0 and g["off16_share"] > 0.15:
        out.append("FLAG groove: off-16ths dead straight and fully quantised; it may feel stiff "
                   "(try 54-58% swing or groove pool on hats and perc)")
    if g["off16_share"] < 0.05:
        out.append("FLAG groove: almost no off-16th hits; nothing pushes between the beats")
    if ref:
        for k, label in (("danceability", "danceability"), ("swing_pct", "swing %")):
            if g[k] is not None and ref.get(k) is not None:
                out.append(f"groove vs reference: {label} {g[k]} vs {ref[k]}")
    return out


def bar_features(y, bpm, offset):
    bar = int(4 * 60.0 / bpm * SR)
    start = int(offset * SR)
    feats, rms = [], []
    for i in range(start, len(y) - bar + 1, bar):
        seg = y[i:i + bar]
        mf = librosa.feature.mfcc(y=seg, sr=SR, n_mfcc=13).mean(axis=1)
        ch = librosa.feature.chroma_stft(y=seg, sr=SR).mean(axis=1)
        S = np.abs(librosa.stft(seg, n_fft=2048)) ** 2
        f = librosa.fft_frequencies(sr=SR, n_fft=2048)
        tot = S.sum() + 1e-12
        bands = [10 * np.log10(S[(f >= lo) & (f < hi)].sum() / tot + 1e-12)
                 for lo, hi in ((20, 120), (120, 500), (500, 2000), (2000, 6000), (6000, 20000))]
        r = float(np.sqrt(np.mean(seg ** 2)) + 1e-9)
        onsets = len(librosa.onset.onset_detect(y=seg, sr=SR))
        feats.append(np.r_[mf, 4 * ch, bands, 20 * np.log10(r), onsets / 4.0])
        rms.append((20 * np.log10(r), onsets, bands))
    return np.array(feats), rms


def boredom(feats, max_bars=16):
    if len(feats) < 4:
        return [], []
    z = (feats - feats.mean(axis=0)) / (feats.std(axis=0) + 1e-9)
    change = np.zeros(len(z))
    for i in range(1, len(z)):
        prev = z[max(0, i - 4):i].mean(axis=0)
        change[i] = np.linalg.norm(z[i] - prev)
    thr = np.median(change[1:]) + 0.5 * change[1:].std()
    events = [0] + [i for i in range(1, len(z)) if change[i] >= thr]
    stretches = []
    for a, b in zip(events, events[1:] + [len(z)]):
        if b - a > max_bars:
            stretches.append((a + 1, b))
    return stretches, events


def energy(rms, block=8):
    vals = []
    for i in range(0, len(rms), block):
        chunk = rms[i:i + block]
        loud = np.mean([c[0] for c in chunk])
        dens = np.mean([c[1] for c in chunk])
        low = np.mean([c[2][0] for c in chunk])
        vals.append((loud, dens, low))
    v = np.array(vals)
    norm = (v - v.min(axis=0)) / (np.ptp(v, axis=0) + 1e-9)
    e = 1 + 9 * (0.5 * norm[:, 0] + 0.3 * norm[:, 1] + 0.2 * norm[:, 2])
    return [int(round(x)) for x in e]


def energy_lines(curve, block=8):
    out = ["energy per 8 bars: " + " ".join(str(x) for x in curve)]
    n = len(curve)
    if n < 6:
        out.append("energy: track too short to judge the set shape")
        return out
    peak = int(np.argmax(curve))
    first_drop = next((i for i, x in enumerate(curve) if x >= max(curve) - 1), peak)
    if curve[0] >= curve[first_drop] - 2:
        out.append("FLAG energy: the intro is nearly as hot as the drop; DJs need a lower-energy drums-only intro")
    dip = min(curve[first_drop:], default=10)
    dip_at = first_drop + int(np.argmin(curve[first_drop:]))
    if dip > curve[first_drop] - 3 or dip_at >= n - 2:
        out.append("FLAG energy: no clear breakdown after the first drop (energy should fall 3+ points, then build)")
    else:
        second = max(curve[dip_at:], default=0)
        if second < curve[first_drop]:
            out.append(f"FLAG energy: second drop ({second}) is weaker than the first ({curve[first_drop]})")
        rise = curve[dip_at:dip_at + 3]
        if len(rise) >= 2 and rise[-1] <= rise[0]:
            out.append(f"FLAG energy: no build out of the breakdown at bar {dip_at * block + 1}")
    if curve[-1] >= max(curve) - 2:
        out.append("FLAG energy: the outro stays near peak energy; let it release for the DJ")
    flat = max(len(s) for s in "".join("=" if a == b else "|" for a, b in zip(curve, curve[1:])).split("|"))
    if flat + 1 >= 6:
        out.append(f"FLAG energy: energy flat for {(flat + 1) * block} bars in a row")
    return out


p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
p.add_argument("track")
p.add_argument("--bpm", type=float, required=True)
p.add_argument("--offset", type=float, default=0.0, help="seconds before bar 1")
p.add_argument("--only", choices=["groove", "boredom", "energy"])
p.add_argument("--compare", help="reference audio for the groove comparison")
p.add_argument("--ref-bpm", type=float)
p.add_argument("--max-bars", type=int, default=16)
p.add_argument("--json")
a = p.parse_args()

y = load(a.track)
res, lines = {}, []
if a.only in (None, "groove"):
    g = groove(y, a.bpm, a.offset)
    ref = groove(load(a.compare), a.ref_bpm or a.bpm, 0.0) if a.compare else None
    res["groove"], res["groove_ref"] = g, ref
    lines += groove_lines(g, ref)
if a.only in (None, "boredom", "energy"):
    feats, rms = bar_features(y, a.bpm, a.offset)
    if a.only in (None, "boredom"):
        stretches, events = boredom(feats, a.max_bars)
        res["boredom"] = {"bars": len(feats), "change_bars": [e + 1 for e in events], "stretches": stretches}
        lines += [f"FLAG boredom: nothing new for {b - s + 1} bars (bars {s}-{b}); add or remove a part, "
                  "a fill or a filter move" for s, b in stretches] or [f"boredom: something changes at least every {a.max_bars} bars"]
    if a.only in (None, "energy"):
        curve = energy(rms)
        res["energy"] = curve
        lines += energy_lines(curve)
if a.json:
    with open(os.path.expanduser(a.json), "w") as f:
        json.dump(res, f, indent=1)
print("\n".join(lines))
