"""Measure a track and, with --compare, print the differences from a reference.

Usage:
  python analyze.py ref.wav --save ~/producer-agent/analysis/ref.json
  python analyze.py render.wav --compare ~/producer-agent/analysis/ref.json
  python analyze.py render.wav --start 64 --end 96   # analyse one section (seconds)
"""
import argparse
import json
import os

import librosa
import numpy as np
import pyloudnorm as pyln

BANDS = {"sub": (20, 60), "low": (60, 250), "mid": (250, 2000),
         "high_mid": (2000, 6000), "air": (6000, 20000)}
MAJOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def analyze(path, start=None, end=None):
    sr = 44100
    dur = None if end is None else end - (start or 0)
    stereo, sr = librosa.load(os.path.expanduser(path), sr=sr, mono=False,
                              offset=start or 0.0, duration=dur)
    stereo = np.atleast_2d(stereo)
    y = stereo.mean(axis=0)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr).mean(axis=1)
    best = max(((np.corrcoef(chroma, np.roll(prof, i))[0, 1], NOTES[i] + mode)
                for i in range(12)
                for prof, mode in ((MAJOR, " major"), (MINOR, " minor"))))
    S = np.abs(librosa.stft(y)) ** 2
    freqs = librosa.fft_frequencies(sr=sr)
    total = S.sum() + 1e-12
    bands = {k: round(float(10 * np.log10(S[(freqs >= lo) & (freqs < hi)].sum() / total + 1e-12)), 1)
             for k, (lo, hi) in BANDS.items()}
    onsets = librosa.onset.onset_detect(y=y, sr=sr)
    return {
        "file": os.path.basename(path),
        "seconds": round(len(y) / sr, 1),
        "tempo": round(float(np.atleast_1d(tempo)[0]), 1),
        "key": best[1],
        "lufs": round(float(pyln.Meter(sr).integrated_loudness(stereo.T)), 1),
        "bands_db": bands,
        "onsets_per_sec": round(len(onsets) / (len(y) / sr), 2),
        "centroid_hz": round(float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())),
    }


p = argparse.ArgumentParser()
p.add_argument("track")
p.add_argument("--compare", help="reference audio or saved JSON")
p.add_argument("--save", help="write results to this JSON file")
p.add_argument("--start", type=float, help="section start in seconds")
p.add_argument("--end", type=float, help="section end in seconds")
a = p.parse_args()

res = analyze(a.track, a.start, a.end)
if a.save:
    out = os.path.expanduser(a.save)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as f:
        json.dump(res, f, indent=2)
if a.compare:
    c = os.path.expanduser(a.compare)
    if c.endswith(".json"):
        with open(c) as f:
            ref = json.load(f)
    else:
        ref = analyze(c, a.start, a.end)
    diff = {k: round(res["bands_db"][k] - ref["bands_db"][k], 1) for k in BANDS}
    print(json.dumps({"track": res, "reference": ref, "band_diff_db": diff,
                      "tempo_diff": round(res["tempo"] - ref["tempo"], 1),
                      "lufs_diff": round(res["lufs"] - ref["lufs"], 1),
                      "onset_diff": round(res["onsets_per_sec"] - ref["onsets_per_sec"], 2),
                      "centroid_diff_hz": res["centroid_hz"] - ref["centroid_hz"]}, indent=2))
else:
    print(json.dumps(res, indent=2))
