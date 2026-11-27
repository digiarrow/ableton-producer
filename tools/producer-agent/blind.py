"""Blind comparison: our section against the same section of a professional track.

Cuts matching sections (by bars) from both tracks, matches their loudness,
saves them as A and B in random order and prints only A/B measurements, so the
critic judges without knowing which is ours. Then reveal and record the pick.
Where the pro track keeps winning, that's the area to fix.

Usage (Mac, the Essentia venv):
  PY=~/producer-agent/.venv-genre/bin/python
  $PY ~/producer-agent/blind.py make v12.wav pro.wav --bpm 126 --ref-bpm 125 \
      --bars 33-48 --ref-bars 65-80 --name drop1
  $PY ~/producer-agent/blind.py pick <id> B "tighter low end, bigger hook"
  $PY ~/producer-agent/blind.py tally          # which sections the pro track keeps winning

Clips go to ~/producer-agent/renders/blind/<id>/A.wav, B.wav; the answer key
stays in key.json there, and picks in ~/producer-agent/analysis/blind_log.jsonl.
"""
import argparse
import json
import os
import random
import subprocess
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, "producer-agent/renders/blind")
LOG = os.path.join(HOME, "producer-agent/analysis/blind_log.jsonl")
AES_PY = os.path.join(HOME, "producer-agent/.venv-aes/bin/python")
SR = 44100


def cut(path, bars, bpm):
    import librosa
    s, e = (int(b) for b in bars.split("-"))
    bar = 4 * 60.0 / bpm
    y, _ = librosa.load(os.path.expanduser(path), sr=SR, mono=False, offset=(s - 1) * bar, duration=(e - s + 1) * bar)
    return np.atleast_2d(y)


def stats(y):
    import librosa
    import pyloudnorm as pyln
    m = y.mean(axis=0)
    S = np.abs(librosa.stft(m)) ** 2
    f = librosa.fft_frequencies(sr=SR)
    tot = S.sum() + 1e-12
    band = lambda lo, hi: round(float(10 * np.log10(S[(f >= lo) & (f < hi)].sum() / tot + 1e-12)), 1)
    out = {"sub": band(20, 60), "low": band(60, 250), "mid": band(250, 2000), "high_mid": band(2000, 6000),
           "air": band(6000, 20000), "hits_per_s": round(len(librosa.onset.onset_detect(y=m, sr=SR)) / (len(m) / SR), 2),
           "crest_db": round(float(20 * np.log10(np.abs(m).max() / (np.sqrt(np.mean(m ** 2)) + 1e-12))), 1),
           "width": round(float(1 - np.corrcoef(y[0], y[-1])[0, 1]), 3) if y.shape[0] > 1 else 0.0}
    try:
        import essentia.standard as es
        out["danceability"] = round(float(es.Danceability(sampleRate=SR)(m.astype(np.float32))[0]), 2)
    except Exception:
        pass
    return out


def aes(path):
    if not os.path.exists(AES_PY):
        return {}
    try:
        r = subprocess.run([AES_PY, "-c", "import sys,json;from audiobox_aesthetics.infer import initialize_predictor as i;"
                            "print(json.dumps(i().forward([{'path':sys.argv[1]}])[0]))", path],
                           capture_output=True, text=True, timeout=900).stdout.strip().splitlines()[-1]
        r = json.loads(r)
        return {"CE": round(r["CE"], 2), "PQ": round(r["PQ"], 2)}
    except Exception:
        return {}


p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("make")
s.add_argument("ours")
s.add_argument("pro")
s.add_argument("--bpm", type=float, required=True)
s.add_argument("--ref-bpm", type=float)
s.add_argument("--bars", required=True, help="our bars, e.g. 33-48")
s.add_argument("--ref-bars", help="pro bars (default: same)")
s.add_argument("--name", default="section")
s = sub.add_parser("pick")
s.add_argument("id")
s.add_argument("choice", choices=["A", "B"])
s.add_argument("why", nargs="?", default="")
sub.add_parser("tally")
a = p.parse_args()

if a.cmd == "make":
    import pyloudnorm as pyln
    import soundfile as sf
    ours = cut(a.ours, a.bars, a.bpm)
    pro = cut(a.pro, a.ref_bars or a.bars, a.ref_bpm or a.bpm)
    n = min(ours.shape[1], pro.shape[1])
    meter = pyln.Meter(SR)
    clips = {}
    for k, y in (("ours", ours[:, :n]), ("pro", pro[:, :n])):
        gain = 10 ** ((-14 - meter.integrated_loudness(y.T)) / 20)  # match loudness: louder always "wins" otherwise
        clips[k] = np.clip(y * gain, -1, 1)
    order = ["ours", "pro"]
    random.shuffle(order)
    cid = f"{a.name}-{time.strftime('%Y%m%d-%H%M%S')}"
    d = os.path.join(ROOT, cid)
    os.makedirs(d, exist_ok=True)
    for label, k in zip("AB", order):
        sf.write(os.path.join(d, f"{label}.wav"), clips[k].T, SR, subtype="PCM_24")
    json.dump({"A": order[0], "B": order[1], "section": a.name, "ours": a.ours, "pro": a.pro},
              open(os.path.join(d, "key.json"), "w"))
    print(f"blind pair {cid} (loudness matched to -14 LUFS, {n / SR:.1f} s). Do not open key.json before picking.")
    for label in "AB":
        f = os.path.join(d, f"{label}.wav")
        st = stats(clips[order["AB".index(label)]])
        st.update(aes(f))
        print(f"{label}: " + " · ".join(f"{k} {v}" for k, v in st.items()))
elif a.cmd == "pick":
    d = os.path.join(ROOT, a.id)
    key = json.load(open(os.path.join(d, "key.json")))
    winner = key[a.choice]
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M"), "id": a.id, "section": key["section"],
                            "ours": key["ours"], "picked": winner, "why": a.why}) + "\n")
    print(f"{a.choice} was {winner.upper()}." + (" The pro track won: fix this section first." if winner == "pro" else " Ours won this one."))
elif a.cmd == "tally":
    if not os.path.exists(LOG):
        sys.exit("no blind picks yet")
    rows = [json.loads(l) for l in open(LOG)]
    by = {}
    for r in rows:
        w = by.setdefault(r["section"], {"pro": 0, "ours": 0, "why": []})
        w[r["picked"]] += 1
        if r["picked"] == "pro" and r["why"]:
            w["why"].append(r["why"])
    for sec, w in sorted(by.items(), key=lambda kv: -kv[1]["pro"]):
        print(f"{sec}: pro {w['pro']} · ours {w['ours']}" + (f" · pro wins for: {'; '.join(w['why'][-3:])}" if w["why"] else ""))
