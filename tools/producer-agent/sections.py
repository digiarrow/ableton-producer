"""Section-by-section comparison: our track against a reference, one section at a time.

Splits both tracks into matching sections by bar numbers (from a reference
structure map, Ableton locators or a list you type), measures each section in
detail and prints ONLY the differences that matter, e.g.
  "Drop 1: sub (20-60 Hz) 3.1 dB under the reference".
Full numbers go to --json for the record; they are too large to read in chat.

Usage:
  # reference sections from its structure map, ours the same bars
  python sections.py ours.wav ~/producer-agent/references/mario.wav \
      --bpm 126 --map ~/Documents/Ableton/producer/references/mario.md

  # sections typed by hand (or read off Ableton locators); our capture starts at bar 33
  python sections.py drop.wav ref.wav --bpm 126 --start-bar 33 \
      --sections "Drop 1:33-56"

  # different bar layout in the reference
  python sections.py ours.wav ref.wav --bpm 124 --ref-bpm 126 \
      --sections "Intro:1-32,Drop:49-80" --ref-sections "Intro:1-24,Drop:33-56"

Options:
  --start-bar N / --ref-start-bar N   bar the file starts at (default 1)
  --offset S / --ref-offset S         seconds before bar 1 in the file (default 0)
  --threshold DB                      smallest spectrum difference to report (default 2)
  --json PATH                         save every number per section
"""
import argparse
import json
import os
import re

import librosa
import numpy as np
import pyloudnorm as pyln

SR = 44100
N_FFT = 4096
BANDS = {"sub (20-60 Hz)": (20, 60), "low (60-120 Hz)": (60, 120),
         "low-mid (120-250 Hz)": (120, 250), "mid (250 Hz-2 kHz)": (250, 2000),
         "high-mid (2-6 kHz)": (2000, 6000), "air (6-20 kHz)": (6000, 20000)}
# third-octave centres 25 Hz .. 16 kHz for the full-resolution spectrum comparison
THIRDS = [25 * 2 ** (i / 3) for i in range(31)]


def parse_sections(text):
    out = []
    for part in text.split(","):
        name, bars = part.rsplit(":", 1)
        a, b = re.split(r"\s*[-–]\s*", bars.strip())
        out.append((name.strip(), int(a), int(b)))
    return out


def sections_from_map(path):
    """Read the Section and Bars columns of a structure map table."""
    out = []
    with open(os.path.expanduser(path)) as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            m = re.fullmatch(r"(\d+)\s*[-–]\s*(\d+)", cells[1])
            if m:
                out.append((cells[0], int(m.group(1)), int(m.group(2))))
    if not out:
        raise SystemExit(f"no 'Section | Bars' rows found in {path}")
    return out


def bar_seconds(bpm):
    return 4 * 60.0 / bpm


def fmt_hz(f):
    return f"{f / 1000:.1f} kHz" if f >= 1000 else f"{f:.0f} Hz"


def measure(stereo):
    """Everything we compare for one section of stereo audio."""
    mono = stereo.mean(axis=0)
    mid, side = (stereo[0] + stereo[1]) / 2, (stereo[0] - stereo[1]) / 2
    S = np.abs(librosa.stft(mono, n_fft=N_FFT)) ** 2
    S_side = np.abs(librosa.stft(side, n_fft=N_FFT)) ** 2
    S_mid = np.abs(librosa.stft(mid, n_fft=N_FFT)) ** 2
    freqs = librosa.fft_frequencies(sr=SR, n_fft=N_FFT)
    power = S.mean(axis=1)
    total = power.sum() + 1e-20

    def rel_db(lo, hi, p=power):
        sel = (freqs >= lo) & (freqs < hi)
        return float(10 * np.log10(p[sel].sum() / total + 1e-20))

    bands = {k: rel_db(lo, hi) for k, (lo, hi) in BANDS.items()}
    thirds = [rel_db(c / 2 ** (1 / 6), c * 2 ** (1 / 6)) for c in THIRDS]

    low = freqs < 120
    low_side = float(10 * np.log10(S_side[low].sum() / (S_mid[low].sum() + 1e-20) + 1e-20))
    all_side = float(10 * np.log10(S_side.sum() / (S_mid.sum() + 1e-20) + 1e-20))
    corr = float(np.corrcoef(stereo[0], stereo[1])[0, 1]) if stereo[0].std() > 0 else 1.0

    rms = float(np.sqrt(np.mean(mono ** 2)) + 1e-12)
    crest = float(20 * np.log10(np.abs(mono).max() / rms + 1e-12))
    onset_env = librosa.onset.onset_strength(y=mono, sr=SR)
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=SR)
    # transient sharpness: onset strength at detected hits vs the average envelope
    sharp = float(onset_env[onsets].mean() / (onset_env.mean() + 1e-6)) if len(onsets) else 0.0
    try:
        lufs = float(pyln.Meter(SR).integrated_loudness(stereo.T))
    except ValueError:  # shorter than one 400 ms block
        lufs = float("nan")
    return {
        "seconds": round(len(mono) / SR, 1),
        "lufs": round(lufs, 1),
        "crest_db": round(crest, 1),
        "bands_db": {k: round(v, 1) for k, v in bands.items()},
        "thirds_db": [round(v, 1) for v in thirds],
        "low_side_db": round(low_side, 1),     # side vs mid below 120 Hz; lower = more mono
        "side_db": round(all_side, 1),         # side vs mid overall; higher = wider
        "correlation": round(corr, 2),
        "onsets_per_sec": round(len(onsets) / (len(mono) / SR), 2),
        "transient_sharpness": round(sharp, 2),
        "centroid_hz": round(float(librosa.feature.spectral_centroid(y=mono, sr=SR).mean())),
    }


def load(path):
    y, _ = librosa.load(os.path.expanduser(path), sr=SR, mono=False)
    y = np.atleast_2d(y)
    return np.vstack([y, y]) if y.shape[0] == 1 else y[:2]


def cut(audio, first, last, start_bar, offset, bpm):
    bs = bar_seconds(bpm)
    a = offset + (first - start_bar) * bs
    b = offset + (last - start_bar + 1) * bs
    if a < 0:
        return None, f"starts before the file (bar {start_bar})"
    ia, ib = int(a * SR), int(b * SR)
    if ia >= audio.shape[1]:
        return None, "past the end of the file"
    seg = audio[:, ia:min(ib, audio.shape[1])]
    note = "" if ib <= audio.shape[1] else f" (file ends early: {seg.shape[1] / SR:.1f} of {b - a:.1f} s)"
    return seg, note


def spectrum_regions(ours, ref, threshold):
    """Group neighbouring third-octave bands that differ the same way by >= threshold."""
    diff = np.array(ours) - np.array(ref)
    regions, i = [], 0
    while i < len(diff):
        if abs(diff[i]) < threshold:
            i += 1
            continue
        sign, j = np.sign(diff[i]), i
        while j + 1 < len(diff) and np.sign(diff[j + 1]) == sign and abs(diff[j + 1]) >= threshold:
            j += 1
        lo, hi = THIRDS[i] / 2 ** (1 / 6), THIRDS[j] * 2 ** (1 / 6)
        regions.append((float(diff[i:j + 1].mean()), lo, hi))
        i = j + 1
    regions.sort(key=lambda r: -abs(r[0]))
    return regions[:4]


def differences(name, o, r, threshold, curve_o, curve_r):
    lines = []

    def say(text):
        lines.append(f"{name}: {text}")

    for band in BANDS:
        d = o["bands_db"][band] - r["bands_db"][band]
        if abs(d) >= 3 or (band.startswith(("sub", "low (")) and abs(d) >= 2):
            say(f"{band} {abs(d):.1f} dB {'over' if d > 0 else 'under'} the reference")
    for d, lo, hi in spectrum_regions(o["thirds_db"], r["thirds_db"], threshold):
        say(f"spectrum {fmt_hz(lo)}-{fmt_hz(hi)} {abs(d):.1f} dB {'louder' if d > 0 else 'quieter'}")
    d = curve_o - curve_r
    if not np.isnan(d) and abs(d) >= 1.5:
        say(f"energy vs the track's loudest section {abs(d):.1f} LU {'higher' if d > 0 else 'lower'} "
            f"than in the reference ({curve_o:+.1f} vs {curve_r:+.1f} LU)")
    if o["low_side_db"] - r["low_side_db"] >= 6 and o["low_side_db"] > -20:
        say(f"low end below 120 Hz less mono (side {o['low_side_db']} vs {r['low_side_db']} dB)")
    d = o["side_db"] - r["side_db"]
    if abs(d) >= 4:
        say(f"stereo image {'wider' if d > 0 else 'narrower'} (side {o['side_db']} vs {r['side_db']} dB, "
            f"correlation {o['correlation']} vs {r['correlation']})")
    d = o["crest_db"] - r["crest_db"]
    if abs(d) >= 2:
        say(f"crest factor {o['crest_db']} vs {r['crest_db']} dB: "
            + ("more dynamic, transients stick out more" if d > 0 else "flatter, transients squashed"))
    d = o["onsets_per_sec"] - r["onsets_per_sec"]
    if abs(d) >= 1:
        say(f"{abs(d):.1f} hits/s {'busier' if d > 0 else 'sparser'} ({o['onsets_per_sec']} vs {r['onsets_per_sec']})")
    if r["transient_sharpness"] and abs(o["transient_sharpness"] / r["transient_sharpness"] - 1) >= 0.25:
        say(f"transients {'sharper' if o['transient_sharpness'] > r['transient_sharpness'] else 'softer'} "
            f"({o['transient_sharpness']} vs {r['transient_sharpness']})")
    d = o["centroid_hz"] - r["centroid_hz"]
    if abs(d) >= 0.15 * r["centroid_hz"]:
        say(f"{'brighter' if d > 0 else 'darker'} (centroid {o['centroid_hz']} vs {r['centroid_hz']} Hz)")
    return lines


p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
p.add_argument("ours")
p.add_argument("reference")
p.add_argument("--bpm", type=float, required=True, help="our tempo")
p.add_argument("--ref-bpm", type=float, help="reference tempo (default: --bpm)")
p.add_argument("--map", help="reference structure map (.md) with a Section | Bars table")
p.add_argument("--sections", help='ours, e.g. "Intro:1-32,Drop:33-64" (default: same as reference)')
p.add_argument("--ref-sections", help="reference sections (default: --map, else --sections)")
p.add_argument("--start-bar", type=int, default=1)
p.add_argument("--ref-start-bar", type=int, default=1)
p.add_argument("--offset", type=float, default=0.0)
p.add_argument("--ref-offset", type=float, default=0.0)
p.add_argument("--threshold", type=float, default=2.0)
p.add_argument("--json")
a = p.parse_args()

ref_secs = (parse_sections(a.ref_sections) if a.ref_sections
            else sections_from_map(a.map) if a.map
            else parse_sections(a.sections) if a.sections else None)
if ref_secs is None:
    p.error("give --map, --sections or --ref-sections")
our_secs = parse_sections(a.sections) if a.sections else ref_secs
ref_by_name = {n.lower(): (n, s, e) for n, s, e in ref_secs}

ours_audio, ref_audio = load(a.ours), load(a.reference)
results, skipped = {}, []
for name, s, e in our_secs:
    if name.lower() not in ref_by_name:
        skipped.append(f"{name}: no section with this name in the reference")
        continue
    _, rs, re_ = ref_by_name[name.lower()]
    o_seg, o_note = cut(ours_audio, s, e, a.start_bar, a.offset, a.bpm)
    r_seg, r_note = cut(ref_audio, rs, re_, a.ref_start_bar, a.ref_offset, a.ref_bpm or a.bpm)
    if o_seg is None or r_seg is None or min(o_seg.shape[1], r_seg.shape[1]) < SR:
        skipped.append(f"{name}: skipped, ours {o_note or 'ok'}, reference {r_note or 'ok'}")
        continue
    if o_note:
        skipped.append(f"{name}: ours{o_note}")
    results[name] = {"bars": [s, e], "ref_bars": [rs, re_],
                     "ours": measure(o_seg), "reference": measure(r_seg)}

if not results:
    raise SystemExit("\n".join(skipped) or "no sections to compare")


def curve(side):
    vals = {n: r[side]["lufs"] for n, r in results.items()}
    top = max(v for v in vals.values() if not np.isnan(v))
    return {n: v - top for n, v in vals.items()}


curve_o, curve_r = curve("ours"), curve("reference")
report = []
for name, r in results.items():
    lines = differences(name, r["ours"], r["reference"], a.threshold, curve_o[name], curve_r[name])
    r["differences"] = lines
    report += lines or [f"{name}: within tolerance"]

if a.json:
    out = os.path.expanduser(a.json)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
print("\n".join(report + skipped))
