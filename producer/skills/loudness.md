# Loudness and reference mastering (pyloudnorm + Matchering) — mix and export stages

Load with `_common.md` and `mixdown.md` or `export.md`.

## Measure (pyloudnorm)
```
~/producer-agent/.venv-tools/bin/python ~/producer-agent/lufs.py FILE [FILE ...]
```
Integrated LUFS and peak. Reference values: Spotlight -9.9 LUFS, Mariô -6.9 LUFS. Compare balance, not loudness, until the master stage.

## Match a reference (Matchering)
```
~/producer-agent/.venv-tools/bin/python ~/producer-agent/master.py TARGET REFERENCE OUT.wav
```
- TARGET is our premaster (headroom about -6 dB, no limiter on the master); REFERENCE is the track whose loudness and tone we want. Output is 24-bit WAV.
- Name it `<song>-v<NN>-master-<ref>.wav` and save it as a numbered version; ask for a rating.
- **Check true peak after.** Matchering's limiter checks sample peaks only: on the first test it gave -10.35 LUFS but +0.41 dBTP. Turn the result down ~1.5 dB or put a true-peak limiter last, then re-run `lufs.py`. Aim for true peak at or below -1 dBTP.
- Matchering matches the reference's EQ curve too. If the result sounds wrong, the mix is the problem; fix it in the mix, not here.

## Setup
matchering 2.0.6 (GPLv3, fine to use as a tool), pyloudnorm 0.2.0 (MIT), venv `.venv-tools` (Python 3.11). The old `.venv` (Python 3.10) also has pyloudnorm for `analyze.py`.
