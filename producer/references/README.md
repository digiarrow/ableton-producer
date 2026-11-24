# References folder

Reference tracks the agent compares against (rule 4), and a structure map for each.

- **Audio** lives on the Mac in `~/producer-agent/references/` (WAV or high-quality MP3 that Digi Arrow bought). Analysis JSONs go in `~/producer-agent/analysis/`. Audio is never committed to GitHub or copied to project files.
- **Structure maps** live here, one file per track: `references/<artist> - <title>.md`, made with the template below. The arrangement stage copies the map's section lengths and energy curve.
- Reference tracks are for study only. Never copy their melodies or samples into a track.

## Index
| Track | Genre | BPM | Key | Map | Analysis JSON |
|---|---|---|---|---|---|
| David Guetta & Jast - Mariô (Extended Mix) | tech house / Latin house | 126 | A minor (8A) | `mario.md` | mario-ref.json (+ intro, break1, drop1, drop2) |
| Andrea Oliva - Spotlight (radio edit) | progressive house / tech house | 123 | D# minor (2A) | `spotlight.md` | andreaoliva-spotlight-ref.json, -genre.json, -genre-drop2.json |

## Structure map template
```
# <artist> - <title>
BPM · key (Camelot) · length · integrated LUFS
Bands (dB rel. total): sub / low / mid / high-mid / air · onsets/s · centroid

| Section | Bars | Start time | Energy 1-10 | What plays | What changes |
|---|---|---|---|---|---|

Sound notes: kick, bass, hook, top, FX (what makes it sound like this)
What to take from it:
```
