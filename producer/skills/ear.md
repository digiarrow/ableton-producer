# Human-like ear (critic and any stage)

Tools that help judge how a track **feels**, on top of loudness, low end, spectrum and genre. All run on the Mac, read files only (no playback), and are free and local. They are second opinions: Digi Arrow's ears and ratings decide. Install record in `../downloads_log.md`.

| Tool | Run (Mac) | What it says |
|---|---|---|
| Quality scores (Meta Audiobox Aesthetics) | `~/producer-agent/.venv-aes/bin/python ~/producer-agent/aesthetics.py <file> [--compare <benchmarks>] --log ~/producer-agent/analysis/aesthetics.jsonl` | 1-10 scores: CE enjoyment, CU usefulness, PC complexity, PQ production quality. The critic reads CE and PQ. Official CLI also works: `audio-aes input.jsonl --batch-size 1 > output.jsonl` with lines `{"path": "/path/track.wav"}`. |
| Groove, boredom, energy curve | `~/producer-agent/.venv-genre/bin/python ~/producer-agent/feel.py <file> --bpm <bpm> [--offset s] [--compare ref.wav --ref-bpm n]` | Danceability (Essentia) and swing %: moves or stiff? Novelty per bar: FLAG when nothing new happens for more than 16 bars. Energy 1-10 per 8 bars and whether it builds and releases like a set. |
| Describe-and-match (LAION CLAP) | `~/producer-agent/.venv-clap/bin/python ~/producer-agent/clap_match.py <file> --vibe "dark, rolling, hypnotic tech house" [--start s --end s]` | How well the track matches the vibe written in the song sheet, ranked against 12 contrast vibes. Rank 1 to 3 = on target. |
| Taste learning | `~/producer-agent/.venv-genre/bin/python ~/producer-agent/taste.py add <version> <file> like|ok|dislike <word>`, then `learn` after 30 to 50 ratings, `predict <file>` | Which measurements go with "like". Writes `taste_profile.json`; the critic weighs it in once it exists. |
| Blind comparison | `~/producer-agent/.venv-genre/bin/python ~/producer-agent/blind.py make <ours> <pro> --bpm n --ref-bpm n --bars 33-48 --ref-bars 65-80 --name drop1`, then `pick <id> A|B "<why>"`, `tally` | Matching sections, loudness matched, labelled A and B at random; judge before revealing. Where the pro track keeps winning, fix that area. |

## Rules
- The producer writes the **intended vibe** (one line, e.g. "dark, rolling, hypnotic tech house") in the song sheet at the setup step; `clap_match.py` checks against it.
- Every rating Digi Arrow gives also gets **like / OK / don't like plus one word** (`taste.py add`), next to the 1 to 10 in `../taste_log.md`.
- No score here can fail a track on its own; only the critic's technical faults do (`../critic.md`).
