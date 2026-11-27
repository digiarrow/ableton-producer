"""Describe-and-match: how well does the track fit the vibe the producer wrote down?

Uses LAION CLAP (music checkpoint) to compare the audio with a short text, e.g.
"dark, rolling, hypnotic tech house". Raw similarity is hard to read, so the
description is also ranked against contrast descriptions: rank 1 = the track
sounds more like the intended vibe than like any of the alternatives.

Usage (Mac, venv with laion_clap):
  ~/producer-agent/.venv-clap/bin/python ~/producer-agent/clap_match.py v12.wav \
      --vibe "dark, rolling, hypnotic tech house"
  ... --start 64 --end 128      # one section (seconds), e.g. the drop
  ... --also "bright vocal house" --also "peak time techno"   # your own contrasts

Checkpoint: music_audioset_epoch_15_esc_90.14.pt from huggingface.co/lukewys/laion_clap
(CC0), saved in ~/producer-agent/models/ on first run.
"""
import argparse
import os
import sys
import tempfile
import urllib.request

import numpy as np

CKPT = "music_audioset_epoch_15_esc_90.14.pt"
URL = "https://huggingface.co/lukewys/laion_clap/resolve/main/" + CKPT
CONTRASTS = [
    "bright, happy, uplifting vocal house", "dark, hypnotic, minimal techno",
    "rolling, groovy, percussive tech house", "big room EDM festival drop",
    "melodic, emotional progressive house", "hard, aggressive industrial techno",
    "chilled, deep, warm deep house", "funky, bouncy, jackin house",
    "dreamy ambient pads with no drums", "pop song with a sung chorus",
    "busy, cluttered, messy mix", "thin, weak, amateur production",
]

p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
p.add_argument("track")
p.add_argument("--vibe", required=True)
p.add_argument("--also", action="append", default=[], help="extra contrast description")
p.add_argument("--start", type=float)
p.add_argument("--end", type=float)
p.add_argument("--models", default="~/producer-agent/models")
a = p.parse_args()

import laion_clap  # noqa: E402  (slow import, after argument errors)
import librosa  # noqa: E402
import soundfile as sf  # noqa: E402

models = os.path.expanduser(a.models)
os.makedirs(models, exist_ok=True)
ckpt = os.path.join(models, CKPT)
if not os.path.exists(ckpt):
    print(f"downloading {CKPT} (about 2 GB, once)...", file=sys.stderr)
    urllib.request.urlretrieve(URL, ckpt)

model = laion_clap.CLAP_Module(enable_fusion=False, amodel="HTSAT-base")
model.load_ckpt(ckpt, verbose=False)

y, sr = librosa.load(os.path.expanduser(a.track), sr=48000, mono=True, offset=a.start or 0.0,
                     duration=None if a.end is None else a.end - (a.start or 0))
# CLAP reads 10 s windows: embed every 10 s and average, so a whole drop counts
chunks = [y[i:i + 480000] for i in range(0, max(len(y) - 240000, 1), 480000)] or [y]
embs = []
with tempfile.TemporaryDirectory() as tmp:
    files = []
    for i, c in enumerate(chunks):
        f = os.path.join(tmp, f"{i}.wav")
        sf.write(f, c, 48000)
        files.append(f)
    embs = model.get_audio_embedding_from_filelist(x=files, use_tensor=False)
audio = np.mean(embs, axis=0)
audio /= np.linalg.norm(audio)

texts = [a.vibe] + [c for c in CONTRASTS + a.also if c.lower() != a.vibe.lower()]
t = model.get_text_embedding(texts, use_tensor=False)
t = t / np.linalg.norm(t, axis=1, keepdims=True)
sims = t @ audio
order = np.argsort(-sims)
rank = int(np.where(order == 0)[0][0]) + 1
print(f'vibe "{a.vibe}": similarity {sims[0]:.3f}, rank {rank} of {len(texts)}')
print("closest descriptions: " + "; ".join(f"{texts[i]} ({sims[i]:.3f})" for i in order[:3]))
if rank > 3:
    print("FLAG: the track reads closer to other vibes than the intended one (second opinion; check by ear)")
