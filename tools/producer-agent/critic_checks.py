"""Checks for the critic on ORIGINAL tracks (no single reference).

  faults      technical faults = automatic fail: clipping, sudden volume jumps,
              harsh frequencies, muddy low end, phase problems, silence or glitches
  benchmarks  loose technical range from 3 to 5 benchmark tracks (loudness and
              low-end balance; notes only, never a fail) plus an originality
              check: is the track too close to any benchmark?

The originality check compares beat-by-beat harmony (chroma), in any key, over
32-beat windows where our harmony moves. It is a pointer for the ear, not proof:
two tracks on one static chord can't be told apart this way.

Usage:
  python critic_checks.py faults capture.wav
  python critic_checks.py benchmarks capture.wav ~/producer-agent/references/benchmarks/*.wav

Prints one line per finding: FAIL = automatic fail, CHECK = confirm by ear or
against the locators, NOTE = technical note only, ORIGINALITY = too close. Kick/bass clash is judged with sections.py and the
set (sidechain, notes), not here.
"""
import argparse
import os
import sys
import warnings

import librosa
import numpy as np
import pyloudnorm as pyln

SR = 44100
warnings.filterwarnings("ignore", category=UserWarning)


def load(path):
    y, _ = librosa.load(os.path.expanduser(path), sr=SR, mono=False)
    y = np.atleast_2d(y)
    return np.vstack([y, y]) if y.shape[0] == 1 else y[:2]


def band_db(power, freqs, lo, hi, total):
    sel = (freqs >= lo) & (freqs < hi)
    return float(10 * np.log10(power[sel].sum() / total + 1e-20))


def profile(stereo):
    mono = stereo.mean(axis=0)
    S = np.abs(librosa.stft(mono, n_fft=4096)) ** 2
    freqs = librosa.fft_frequencies(sr=SR, n_fft=4096)
    p = S.mean(axis=1)
    t = p.sum() + 1e-20
    return {
        "lufs": float(pyln.Meter(SR).integrated_loudness(stereo.T)),
        "sub": band_db(p, freqs, 20, 60, t),
        "low": band_db(p, freqs, 60, 120, t),
        "lowmid": band_db(p, freqs, 120, 250, t),
        "mud": band_db(p, freqs, 200, 500, t),
        "harsh": band_db(p, freqs, 2500, 5000, t),
        "air": band_db(p, freqs, 6000, 20000, t),
    }


def faults(path):
    x = load(path)
    mono = x.mean(axis=0)
    out = []
    t = lambda i: f"{int(i / SR // 60)}:{i / SR % 60:04.1f}"

    # clipping: runs of 3+ samples at or above 0.999
    hot = np.abs(x).max(axis=0) >= 0.999
    runs = np.flatnonzero(np.diff(np.r_[0, hot.astype(int), 0]) == 1)
    if len(runs):
        out.append(f"FAIL clipping: {int(hot.sum())} samples at full scale, first at {t(runs[0])}")
    # inter-sample peaks (4x oversampled)
    tp = float(np.abs(librosa.resample(x, orig_sr=SR, target_sr=SR * 4)).max())
    if tp > 1.0:
        out.append(f"FAIL true peak {20 * np.log10(tp):+.1f} dBTP (over 0)")

    # sudden volume jumps: short-term (3 s) loudness every 0.5 s
    meter = pyln.Meter(SR, block_size=0.4)
    hop, win = int(0.5 * SR), int(3 * SR)
    st = []
    for i in range(0, x.shape[1] - win, hop):
        try:
            st.append(meter.integrated_loudness(x[:, i:i + win].T))
        except ValueError:
            st.append(-70.0)
    st = np.maximum(np.array(st), -70)
    for i in range(1, len(st)):
        jump = st[i] - st[i - 1]
        if jump >= 6 and st[i] > -30:
            out.append(f"FAIL sudden volume jump +{jump:.1f} LU in 0.5 s at {t(i * hop + win)} "
                       "(fine only if it is a planned drop after a break; say which)")

    # silence or glitches mid-track: digital silence >= 50 ms, or single-sample spikes
    silent = np.abs(mono) < 1e-5
    edges = np.diff(np.r_[0, silent.astype(int), 0])
    starts, ends = np.flatnonzero(edges == 1), np.flatnonzero(edges == -1)
    # A dry sample fading to zero is normal; a gap that starts with an abrupt cut is a dropout.
    lead, tail = SR * 1, len(mono) - SR * 1
    cuts, stops = [], []
    for s, e in zip(starts, ends):
        if s <= lead or e >= tail or e - s < 0.02 * SR:
            continue
        before = float(np.sqrt(np.mean(mono[s - int(0.005 * SR):s] ** 2)))
        if before > 0.05:
            cuts.append(s)
        elif e - s >= 0.5 * SR:
            stops.append((s, e))
    if cuts:
        out.append(f"FAIL dropout: {len(cuts)} abrupt cut(s) to digital silence, first at {t(cuts[0])}")
    for s, e in stops[:3]:
        out.append(f"CHECK silence {(e - s) / SR:.1f} s at {t(s)}: fine only if it is a planned stop before a drop")
    # clicks: a sample-to-sample jump far larger than the 10 ms around it
    d = np.abs(np.diff(mono))
    if d.size > SR:
        ctx = np.convolve(d, np.ones(441) / 441, mode="same")
        clicks = np.flatnonzero((d > 0.3) & (d > 25 * ctx))
        if len(clicks):
            out.append(f"CHECK possible clicks/glitches: {len(clicks)} sudden sample jumps, first at {t(clicks[0])} "
                       "(confirm by ear; a confirmed click is a fail)")

    # phase: low-end correlation and overall correlation
    b = np.fft.rfft(x, axis=1)
    f = np.fft.rfftfreq(x.shape[1], 1 / SR)
    b[:, f > 150] = 0
    low = np.fft.irfft(b, n=x.shape[1], axis=1)
    if low[0].std() > 1e-4:
        c = float(np.corrcoef(low[0], low[1])[0, 1])
        if c < 0.8:
            out.append(f"FAIL phase: low end below 150 Hz correlation {c:.2f} (should be near 1, mono)")
    c = float(np.corrcoef(x[0], x[1])[0, 1]) if x[0].std() > 0 else 1.0
    if c < 0:
        out.append(f"FAIL phase: whole-mix correlation {c:.2f} (cancels in mono)")

    # harsh and muddy: tonal balance against broad tech house norms
    p = profile(x)
    if p["harsh"] - p["air"] > 12 and p["harsh"] > -14:
        out.append(f"FAIL harsh: 2.5-5 kHz at {p['harsh']:.1f} dB rel. total, {p['harsh'] - p['air']:.0f} dB over the air band")
    if p["mud"] > p["low"] + 3 and p["mud"] > -7:
        out.append(f"FAIL muddy low end: 200-500 Hz ({p['mud']:.1f} dB) louder than 60-120 Hz ({p['low']:.1f} dB)")
    return out or ["no technical faults found"]


def chroma_seq(mono):
    tempo, beats = librosa.beat.beat_track(y=mono, sr=SR)
    ch = librosa.feature.chroma_cqt(y=mono, sr=SR)
    sync = librosa.util.sync(ch, beats, aggregate=np.median)
    # beats with no clear pitch (drums only, noise) are zeroed so they can't match anything
    tonal = sync.max(axis=0) / (sync.mean(axis=0) + 1e-9) >= 2.5
    sync = sync / (np.linalg.norm(sync, axis=0, keepdims=True) + 1e-9)
    # remove the track's average chroma (key, pedal bass) so only the harmonic motion is compared
    sync = sync - sync[:, tonal].mean(axis=1, keepdims=True) if tonal.any() else sync
    sync = sync / (np.linalg.norm(sync, axis=0, keepdims=True) + 1e-9)
    return sync * tonal


def similarity(a, b, win=32):
    """Best match of any 32-beat window of ours inside the benchmark, over all 12 transpositions."""
    na, nb = a.shape[1], b.shape[1]
    if na < win or nb < win:
        return 0.0
    # only windows where our harmony/melody moves (a one-chord stab matches everything)
    move = np.r_[0, 1 - (a[:, 1:] * a[:, :-1]).sum(axis=0)] * (a.sum(axis=0) > 0)
    moving = np.convolve(move, np.ones(win) / win, mode="valid")[:na - win + 1] >= 0.1
    if not moving.any():
        return 0.0
    best = 0.0
    for k in range(12):
        M = np.roll(a, k, axis=0).T @ b          # beat-by-beat similarity, ours x benchmark
        S = sum(M[t:na - win + 1 + t, t:nb - win + 1 + t] for t in range(win)) / win
        best = max(best, float(S[moving].max()))
    return best


def benchmarks(path, refs):
    if not 3 <= len(refs) <= 5:
        print(f"note: the plan asks for 3 to 5 benchmarks, got {len(refs)}", file=sys.stderr)
    x = load(path)
    ours = profile(x)
    ours_ch = chroma_seq(x.mean(axis=0))
    profs, sims = [], []
    for r in refs:
        y = load(r)
        profs.append(profile(y))
        sims.append((similarity(ours_ch, chroma_seq(y.mean(axis=0))), os.path.basename(r)))
    out = []
    for key, label in (("lufs", "loudness (LUFS)"), ("sub", "sub 20-60 Hz (dB rel.)"),
                       ("low", "low 60-120 Hz (dB rel.)"), ("lowmid", "low-mid 120-250 Hz (dB rel.)")):
        vals = [p[key] for p in profs]
        lo, hi = min(vals) - 1.5, max(vals) + 1.5
        if not lo <= ours[key] <= hi:
            out.append(f"NOTE {label} {ours[key]:.1f}, benchmark range {min(vals):.1f} to {max(vals):.1f} "
                       "(technical note only, not a fail)")
    for s, name in sorted(sims, reverse=True):
        if s >= 0.5:
            out.append(f"ORIGINALITY too close to {name}: harmony/melody match {s:.2f} over 32 beats "
                       "(check by ear and change the hook or chords)")
        elif s >= 0.4:
            out.append(f"ORIGINALITY check {name} by ear: match {s:.2f} over 32 beats")
    return out or ["within the benchmark range; nothing too close to a benchmark"]


p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
sub = p.add_subparsers(dest="cmd", required=True)
f = sub.add_parser("faults")
f.add_argument("track")
b = sub.add_parser("benchmarks")
b.add_argument("track")
b.add_argument("refs", nargs="+")
a = p.parse_args()
print("\n".join(faults(a.track) if a.cmd == "faults" else benchmarks(a.track, a.refs)))
