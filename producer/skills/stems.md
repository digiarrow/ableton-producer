# Stems (Demucs) — any stage, when studying a reference

Load with `_common.md` and `analysis.md`. Splits a reference into drums, bass, vocals and other, so each layer is matched against one stem, not the full mix (lesson from the Mariô audit, `../session_notes.md`).

## Run (Mac)
```
~/producer-agent/demucs-venv/bin/python ~/producer-agent/stems.py INPUT OUTDIR [--start SEC] [--dur SEC] [--model htdemucs]
```
- Stems for references go in `~/producer-agent/references/stems/<slug>/`; tests in `~/producer-agent/tooltest/`.
- Speed: ~10 s per 30 s of audio on the CPU. Split a section (`--start/--dur`) when you only need the drop.
- Setup: demucs 4.1.0 (MIT), Python 3.11 venv `demucs-venv`, model htdemucs (84 MB, Hugging Face, cached in ~/.cache/huggingface).

## Use
- Run `analyze.py` on each stem with `--save ~/producer-agent/analysis/<slug>-<stem>.json`, then compare our soloed layer render against the matching stem.
- Feed the bass and other stems to `midi.md` (Basic Pitch) to read the notes.
- Stems are for study only. Never put reference stems or samples into a track.
