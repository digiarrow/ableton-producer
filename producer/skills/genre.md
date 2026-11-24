# Genre recognition (any stage, or when asked "what genre is this?")

Load with `_common.md`. Uses Essentia's pre-trained Discogs-EffNet genre model (400 Discogs styles, incl. Tech House, House, Techno, Progressive House, Minimal, Deep House, Afro House, Trance). Runs on the Mac only.

## Setup (done once, see `../downloads_log.md`)
- Separate venv `~/producer-agent/.venv-genre` (Python 3.11 or 3.12, because `essentia-tensorflow` has macOS arm64 wheels only for those) with `essentia-tensorflow` 2.1b6.dev1389 (CPython 3.12.16 via uv). Installed and tested 2026-11-24.
- Models in `~/producer-agent/models/`: `discogs-effnet-bs64-1.pb`, `genre_discogs400-discogs-effnet-1.pb`, `genre_discogs400-discogs-effnet-1.json` from essentia.upf.edu/models.
- Script: `~/producer-agent/genre.py` (copy in `tools/producer-agent/genre.py`).
- Licences: Essentia AGPL-3.0, models CC BY-NC-SA 4.0 (non-commercial). Fine for study and DJ use; ask before using it in anything sold.

## Run
```
~/producer-agent/.venv-genre/bin/python ~/producer-agent/genre.py <track> [--start s --end s] [--top 3] [--json out.json]
```
- Track: a file in `~/producer-agent/references/`, a path Digi Arrow gives, or a render from `~/producer-agent/renders/`.
- For a full song, also run the drop alone (`--start/--end`), since intros and breaks blur the call.
- No audio is played; it reads files only.
- TensorFlow prints two harmless lines to stderr; add `2>/dev/null` for clean output.

## Report
Top 3 styles with scores, then one line that explains the call with the script's own measures, e.g. "127 BPM, F minor, dark: Tech House (62%), then Minimal (14%) and House (9%)". Add your own reading where the numbers suggest it (rolling swung bass, offbeat hats, long breakdown), and say when scores are low (top style under 30%) that the call is uncertain.

## Test results (2026-11-24)
- Mariô (Extended Mix), full: Electro House 22.5%, Tech Trance 20.2%, House 18.6%; 125.9 BPM, A minor.
- Mariô drop 1 (61–107 s): Electro House 34.1%, House 22.9%, Progressive House 18.2%; 126 BPM, A minor.
- Our v09 drums-only render: Ghetto House 98.4%, House 67%; key read as C major (no harmony yet), as expected for drums alone.

## Checking our own tracks
- Run it on each reference once and save `--json ~/producer-agent/analysis/<ref>-genre.json`.
- After the drums, bass and arrangement stages, run it on the latest render's drop. Note the top style next to the version number in the song sheet. If it misses the intended genre, say which style it hears and what in the measures points there (tempo, brightness), before changing anything.
- The model was trained on full releases; a drums-only loop often reads as Minimal or Techno. Judge genre on renders with bass and hook in.
