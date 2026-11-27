"""Learn Digi Arrow's taste from simple ratings.

Each attempt gets: like / ok / dislike, plus one word of reason (and the 1-10
rating stays in taste_log.md). After 30 to 50 ratings, `learn` compares the
measurements of every rated file with the ratings and writes a taste profile
the critic weighs in.

Usage (Mac, the Essentia venv, which also has librosa and pyloudnorm):
  PY=~/producer-agent/.venv-genre/bin/python
  $PY ~/producer-agent/taste.py add mario-v12 ~/producer-agent/renders/mario-v12.wav like punchy
  $PY ~/producer-agent/taste.py list
  $PY ~/producer-agent/taste.py learn          # needs 30+ ratings; prints what predicts "like"
  $PY ~/producer-agent/taste.py predict v13.wav  # after learn: how close v13 sits to liked versions

Files: ratings in ~/Documents/Ableton/producer/taste_ratings.csv (synced to the
repo like the other logs), measurements cached in ~/producer-agent/analysis/taste/,
profile in ~/Documents/Ableton/producer/taste_profile.json.
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HOME = os.path.expanduser("~")
RATINGS = os.path.join(HOME, "Documents/Ableton/producer/taste_ratings.csv")
PROFILE = os.path.join(HOME, "Documents/Ableton/producer/taste_profile.json")
CACHE = os.path.join(HOME, "producer-agent/analysis/taste")
AES_PY = os.path.join(HOME, "producer-agent/.venv-aes/bin/python")
SCORE = {"like": 2, "ok": 1, "dislike": 0}
MIN_RATINGS = 30


def measure(path):
    import librosa
    import pyloudnorm as pyln
    key = os.path.basename(path) + f"-{int(os.path.getmtime(path))}"
    cache = os.path.join(CACHE, key + ".json")
    if os.path.exists(cache):
        return json.load(open(cache))
    sr = 44100
    st, _ = librosa.load(path, sr=sr, mono=False)
    st = np.atleast_2d(st)
    y = st.mean(axis=0)
    S = np.abs(librosa.stft(y)) ** 2
    f = librosa.fft_frequencies(sr=sr)
    tot = S.sum() + 1e-12
    band = lambda lo, hi: float(10 * np.log10(S[(f >= lo) & (f < hi)].sum() / tot + 1e-12))
    m = {
        "lufs": float(pyln.Meter(sr).integrated_loudness(st.T)),
        "sub": band(20, 60), "low": band(60, 250), "mid": band(250, 2000),
        "high_mid": band(2000, 6000), "air": band(6000, 20000),
        "centroid": float(librosa.feature.spectral_centroid(y=y, sr=sr).mean()),
        "onsets_per_sec": len(librosa.onset.onset_detect(y=y, sr=sr)) / (len(y) / sr),
        "crest_db": float(20 * np.log10(np.abs(y).max() / (np.sqrt(np.mean(y ** 2)) + 1e-12))),
        "width": float(1 - np.corrcoef(st[0], st[-1])[0, 1]) if st.shape[0] > 1 else 0.0,
    }
    try:
        import essentia.standard as es
        m["danceability"] = float(es.Danceability(sampleRate=sr)(y.astype(np.float32))[0])
    except Exception:
        pass
    if os.path.exists(AES_PY):  # optional: production quality and enjoyment scores
        try:
            out = subprocess.run([AES_PY, "-c",
                                  "import sys,json;from audiobox_aesthetics.infer import initialize_predictor as i;"
                                  "print(json.dumps(i().forward([{'path':sys.argv[1]}])[0]))", path],
                                 capture_output=True, text=True, timeout=900).stdout.strip().splitlines()[-1]
            r = json.loads(out)
            m.update({"aes_CE": r["CE"], "aes_PQ": r["PQ"]})
        except Exception:
            pass
    os.makedirs(CACHE, exist_ok=True)
    json.dump(m, open(cache, "w"))
    return m


def read():
    if not os.path.exists(RATINGS):
        return []
    with open(RATINGS) as f:
        return list(csv.DictReader(f))


def ranks(x):
    """Average ranks, so tied values share a rank (ratings have many ties)."""
    x = np.asarray(x, float)
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[order] = np.arange(len(x))
    for v in np.unique(x):
        r[x == v] = r[x == v].mean()
    return r


def spearman(x, y):
    rx, ry = ranks(np.round(x, 6)), ranks(y)
    return float(np.corrcoef(rx, ry)[0, 1]) if rx.std() > 0 and ry.std() > 0 else 0.0


p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("add")
s.add_argument("version")
s.add_argument("file")
s.add_argument("rating", choices=list(SCORE))
s.add_argument("word", help="one word of reason")
sub.add_parser("list")
sub.add_parser("learn")
s = sub.add_parser("predict")
s.add_argument("file")
a = p.parse_args()

if a.cmd == "add":
    new = not os.path.exists(RATINGS)
    os.makedirs(os.path.dirname(RATINGS), exist_ok=True)
    with open(RATINGS, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "version", "file", "rating", "word"])
        w.writerow([time.strftime("%Y-%m-%d"), a.version, os.path.expanduser(a.file), a.rating, a.word])
    n = len(read())
    print(f"saved; {n} ratings" + ("" if n >= MIN_RATINGS else f" ({MIN_RATINGS - n} more before learning)"))
elif a.cmd == "list":
    rows = read()
    for r in rows:
        print(f"{r['date']} {r['version']}: {r['rating']} ({r['word']})")
    words = {}
    for r in rows:
        words.setdefault(r["rating"], []).append(r["word"])
    for k, v in words.items():
        print(f"{k}: " + ", ".join(sorted(set(v), key=v.count, reverse=True)[:8]))
elif a.cmd == "learn":
    rows = [r for r in read() if os.path.exists(r["file"])]
    if len(rows) < MIN_RATINGS:
        sys.exit(f"{len(rows)} rated files found; learning starts at {MIN_RATINGS} (aim for 30 to 50)")
    ms = [measure(r["file"]) for r in rows]
    y = np.array([SCORE[r["rating"]] for r in rows], float)
    keys = sorted(set.intersection(*[set(m) for m in ms]))
    prof = {"ratings": len(rows), "updated": time.strftime("%Y-%m-%d"), "features": {}}
    for k in keys:
        x = np.array([m[k] for m in ms])
        liked = x[y == 2]
        prof["features"][k] = {"corr": round(spearman(x, y), 2),
                               "liked_median": round(float(np.median(liked)), 2) if len(liked) else None,
                               "liked_range": [round(float(np.percentile(liked, 25)), 2),
                                               round(float(np.percentile(liked, 75)), 2)] if len(liked) >= 4 else None}
    words = {}
    for r in rows:
        words.setdefault(r["rating"], []).append(r["word"].lower())
    prof["words"] = {k: sorted(set(v), key=v.count, reverse=True)[:10] for k, v in words.items()}
    json.dump(prof, open(PROFILE, "w"), indent=1)
    top = sorted(prof["features"].items(), key=lambda kv: -abs(kv[1]["corr"]))[:6]
    print(f"taste profile from {len(rows)} ratings -> {PROFILE}")
    for k, v in top:
        print(f"{k}: {'more' if v['corr'] > 0 else 'less'} is liked (corr {v['corr']:+.2f}), liked range {v['liked_range']}")
    print("words: " + "; ".join(f"{k}: {', '.join(v[:5])}" for k, v in prof["words"].items()))
elif a.cmd == "predict":
    if not os.path.exists(PROFILE):
        sys.exit("no taste profile yet; run learn after 30+ ratings")
    prof = json.load(open(PROFILE))
    m = measure(os.path.expanduser(a.file))
    strong = [(k, v) for k, v in prof["features"].items() if abs(v["corr"]) >= 0.3 and v["liked_range"] and k in m]
    if not strong:
        print("no measurement predicts the ratings strongly yet (all |corr| < 0.3); taste is in the sound, ask by ear")
    for k, v in strong:
        lo, hi = v["liked_range"]
        where = "inside" if lo - 1e-6 <= round(m[k], 2) <= hi + 1e-6 else ("under" if m[k] < lo else "over")
        print(f"{k} {m[k]:.2f}: {where} the liked range {lo} to {hi} (corr {v['corr']:+.2f})")
