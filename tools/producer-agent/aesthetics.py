"""Second-opinion quality scores with Meta's Audiobox Aesthetics (free, runs locally).

Scores each file 1-10 on four axes:
  CE content enjoyment · CU content usefulness · PC production complexity · PQ production quality
The critic reads CE and PQ as a second opinion, never as the only judge.

Usage (Mac, venv with audiobox_aesthetics):
  ~/producer-agent/.venv-aes/bin/python ~/producer-agent/aesthetics.py v12.wav
  ... aesthetics.py v12.wav --compare ~/producer-agent/references/benchmarks/*.wav
  ... aesthetics.py v12.wav --log ~/producer-agent/analysis/aesthetics.jsonl

Weights download once from Hugging Face (facebook/audiobox-aesthetics, CC BY 4.0), no account.
The official CLI (audio-aes input.jsonl) fails on file paths on the Mac (torchaudio needs
torchcodec + ffmpeg); use this script.
"""
import argparse
import json
import os
import sys
import time

AXES = ("CE", "CU", "PC", "PQ")


def score(paths, piece_s=30):
    """Load with soundfile (torchaudio on the Mac needs torchcodec + ffmpeg, which it lacks)
    and score 30 s pieces, weighted by length: one whole-track batch runs out of GPU memory."""
    import soundfile as sf
    import torch
    from audiobox_aesthetics.infer import initialize_predictor
    predictor = initialize_predictor()
    out = []
    for p in paths:
        data, sr = sf.read(os.path.expanduser(p), dtype="float32", always_2d=True)
        wav = torch.from_numpy(data.T.copy())
        total, acc = 0, {k: 0.0 for k in AXES}
        for s0 in range(0, wav.shape[1], piece_s * sr):
            piece = wav[:, s0:s0 + piece_s * sr]
            if piece.shape[1] < sr:  # skip a tail under 1 s
                continue
            r = predictor.forward([{"path": piece, "sample_rate": sr}])[0]
            for k in AXES:
                acc[k] += float(r[k]) * piece.shape[1]
            total += piece.shape[1]
        out.append({k: round(acc[k] / max(total, 1), 2) for k in AXES})
    return out


p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
p.add_argument("tracks", nargs="+", help="our version(s)")
p.add_argument("--compare", nargs="*", default=[], help="benchmark or reference files")
p.add_argument("--log", help="append results to this .jsonl file")
a = p.parse_args()

ours = score(a.tracks)
refs = score(a.compare) if a.compare else []
for path, s in zip(a.tracks, ours):
    print(f"{os.path.basename(path)}: " + " · ".join(f"{k} {s[k]:.2f}" for k in AXES))
if refs:
    avg = {k: sum(r[k] for r in refs) / len(refs) for k in AXES}
    print(f"benchmarks avg ({len(refs)}): " + " · ".join(f"{k} {avg[k]:.2f}" for k in AXES))
    for path, s in zip(a.tracks, ours):
        for k in ("CE", "PQ"):
            d = s[k] - avg[k]
            if d <= -0.5:
                print(f"{os.path.basename(path)}: {k} {abs(d):.2f} under the benchmarks "
                      f"({'enjoyment' if k == 'CE' else 'production quality'}); second opinion only")
if a.log:
    with open(os.path.expanduser(a.log), "a") as f:
        for path, s in zip(a.tracks, ours):
            f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M"), "file": path, **s}) + "\n")
