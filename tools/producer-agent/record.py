"""Record whatever reaches BlackHole (Mac) or VB-Cable (PC) into a WAV file.

Usage:
  python record.py --seconds 30 --out ~/producer-agent/renders/drop1.wav
  python record.py --list            # show audio input devices
"""
import argparse
import os
import sys

import sounddevice as sd
import soundfile as sf

p = argparse.ArgumentParser()
p.add_argument("--seconds", type=float)
p.add_argument("--out")
p.add_argument("--device", default="BlackHole")  # use "CABLE Output" on PC
p.add_argument("--sr", type=int, default=44100)
p.add_argument("--list", action="store_true", help="list input devices and exit")
a = p.parse_args()

if a.list:
    print(sd.query_devices())
    sys.exit(0)
if not a.seconds or not a.out:
    p.error("--seconds and --out are required")

out = os.path.expanduser(a.out)
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
audio = sd.rec(int(a.seconds * a.sr), samplerate=a.sr, channels=2, device=a.device)
sd.wait()
peak = float(abs(audio).max()) if audio.size else 0.0
sf.write(out, audio, a.sr)
print("saved", out, "peak", round(peak, 4))
if peak < 1e-4:
    print("WARNING: recording is silent. Is the Master routed to 1/2 (BlackHole) and playing?")
