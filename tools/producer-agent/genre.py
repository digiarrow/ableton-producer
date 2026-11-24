"""Name the genre of a track with Essentia's Discogs-EffNet genre model (400 styles).

Usage:
  ~/producer-agent/.venv-genre/bin/python ~/producer-agent/genre.py track.wav
  ... genre.py track.wav --start 64 --end 128      # one section (seconds)
  ... genre.py track.wav --top 5 --json out.json   # more styles, save the result
  ... genre.py ~/producer-agent/references/*.wav   # several tracks

Models live in ~/producer-agent/models (override with --models):
  discogs-effnet-bs64-1.pb, genre_discogs400-discogs-effnet-1.pb, genre_discogs400-discogs-effnet-1.json
Models: essentia.upf.edu/models, CC BY-NC-SA 4.0 (non-commercial use only). Essentia: AGPL-3.0.
"""
import argparse
import json
import os
import sys

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import essentia
import essentia.standard as es

essentia.log.infoActive = False
essentia.log.warningActive = False

EMBED = "discogs-effnet-bs64-1.pb"
HEAD = "genre_discogs400-discogs-effnet-1.pb"
LABELS = "genre_discogs400-discogs-effnet-1.json"


def load(path, sr, start, end):
    audio = es.MonoLoader(filename=path, sampleRate=sr, resampleQuality=4)()
    a = int((start or 0) * sr)
    b = len(audio) if end is None else int(end * sr)
    return audio[a:b]


def measure(path, start, end):
    """Tempo, key and brightness, to explain the genre call."""
    y = load(path, 44100, start, end)
    bpm, _, conf, _, _ = es.RhythmExtractor2013(method="multifeature")(y)
    key, scale, strength = es.KeyExtractor(profileType="edma")(y)
    spec, cent = es.Spectrum(), es.Centroid(range=22050)
    w = es.Windowing(type="hann")
    cents = [cent(spec(w(f))) for f in es.FrameGenerator(y, frameSize=2048, hopSize=1024)
             if np.max(np.abs(f)) > 1e-4]
    return {"bpm": round(float(bpm), 1), "bpm_confidence": round(float(conf), 2),
            "key": f"{key} {scale}", "key_strength": round(float(strength), 2),
            "centroid_hz": int(np.median(cents)) if cents else 0}


def classify(path, models, start, end, top):
    y = load(path, 16000, start, end)
    emb = es.TensorflowPredictEffnetDiscogs(
        graphFilename=os.path.join(models, EMBED), output="PartitionedCall:1")(y)
    pred = es.TensorflowPredict2D(
        graphFilename=os.path.join(models, HEAD),
        input="serving_default_model_Placeholder", output="PartitionedCall:0")(emb)
    mean = np.mean(pred, axis=0)
    with open(os.path.join(models, LABELS)) as f:
        classes = json.load(f)["classes"]
    order = np.argsort(mean)[::-1][:top]
    out = []
    for i in order:
        parent, _, style = classes[i].partition("---")
        out.append({"style": style or parent, "parent": parent, "score": round(float(mean[i]), 3)})
    return out


def describe(m):
    bright = "bright" if m["centroid_hz"] > 3000 else "dark" if m["centroid_hz"] < 1800 else "mid-bright"
    return f'{m["bpm"]:g} BPM, {m["key"]}, {bright} ({m["centroid_hz"]} Hz centroid)'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tracks", nargs="+")
    ap.add_argument("--models", default="~/producer-agent/models")
    ap.add_argument("--start", type=float)
    ap.add_argument("--end", type=float)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--json", help="write all results to this file")
    args = ap.parse_args()
    models = os.path.expanduser(args.models)
    results = []
    for t in args.tracks:
        path = os.path.expanduser(t)
        if not os.path.isfile(path):
            print(f"skip (not found): {t}", file=sys.stderr)
            continue
        styles = classify(path, models, args.start, args.end, args.top)
        m = measure(path, args.start, args.end)
        results.append({"track": path, "styles": styles, "measures": m})
        print(f"\n{os.path.basename(path)}")
        for s in styles:
            print(f'  {s["score"]*100:5.1f}%  {s["style"]}  ({s["parent"]})')
        print(f'  {describe(m)}: {styles[0]["style"] if styles else "?"}')
    if args.json:
        with open(os.path.expanduser(args.json), "w") as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
