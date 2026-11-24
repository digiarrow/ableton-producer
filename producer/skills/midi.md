# Audio to MIDI (Basic Pitch) — bass, hook and pad stages, when studying a reference

Load with `_common.md`. Turns a stem into MIDI so you can read a reference's notes: root, scale, rhythm, range.

## Run (Mac)
```
~/producer-agent/.venv-tools/bin/python ~/producer-agent/tomidi.py OUTDIR AUDIO [AUDIO ...]
```
- Best on a Demucs stem (`stems.md`), not the full mix. Bass stems come out clean; the "other" stem gives ghost notes, so keep the notes that repeat.
- Setup: basic-pitch 0.4.0 (Apache-2.0, Spotify), CoreML backend, venv `.venv-tools` (Python 3.11; setuptools pinned below 81 or it crashes on import).

## Use
- Report the most common notes, range and rhythm (e.g. Spotlight bass: D#2 most, D#1–D#3, so a D# root pedal).
- Use the result to pick key, root movement and rhythmic feel, then write our own line.
- **Study only.** A reference's melody or bassline may be rebuilt note for note only in a declared study remake (like `songs/mario-instrumental`). For original tracks, never copy a reference's melody or bassline; this follows `../references/README.md`.
