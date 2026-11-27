# Analysis (any stage)

Load with `_common.md` whenever a stage ends or a change needs checking. Full procedure: `/mnt/project-files/agents/reference-analysis/SKILL.md` (account skill `ableton-reference-analysis`). Summary:

## Silent output
The agent hears through a virtual cable, never exported files or the speakers. Mac: Live's output device is the aggregate **"Agent Out"**: channels 1/2 = BlackHole (silent, the agent's ears), 3/4 = Digi Arrow's speakers/headphones. Normally the Main/Master goes to 3/4. Windows PC: VB-Cable (`record.py --device "CABLE Output"`), not set up yet.

## Render an 8-bar loop
1. `set_master_output("1/2")` (now nobody hears it). If the tool is missing or fails, **do not play**; ask Digi Arrow to play while you record, or skip.
2. Start `~/producer-agent/.venv/bin/python ~/producer-agent/record.py --seconds <8 bars = 8*4*60/BPM> --out ~/producer-agent/renders/<song>-v<NN>-<section>.wav` in the background; start playback from the locator; stop when recording ends.
3. `set_master_output("3/4")`. **Always**, even if something failed.
4. `analyze.py <render> --compare ~/producer-agent/analysis/<ref>.json --start <s> --end <s>` comparing the same section of the reference.

For a single layer, solo the track before capture (and unsolo after) to compare it with the matching reference layer.

## Section-by-section comparison (the agent's ear)
Use it from the arrangement stage on, and whenever a whole track or a long capture needs checking. The raw spectrograms are far too large for the context window, so the script reads them and prints only the differences.
1. Capture the arrangement silently from bar 1 (steps above; length = bars × 4 × 60 / BPM), or one capture per section.
2. Run `~/producer-agent/.venv/bin/python ~/producer-agent/sections.py <capture> ~/producer-agent/references/<ref audio> --bpm <ours> --ref-bpm <theirs> --map ../references/<ref>.md --json ~/producer-agent/analysis/<song>-v<NN>-sections.json`.
   - Sections come from the reference map's `Section | Bars` table. If our bars differ, add `--sections "Intro:1-32,Drop 1:33-64,..."` (read them off the Ableton locators; names must match the map). `--start-bar N` when the capture starts at bar N; `--ref-offset S` if the reference has silence before bar 1.
3. It compares each section with the same reference section: third-octave spectrum, six bands (sub, low, low-mid, mid, high-mid, air), the energy curve (each section's LUFS against the track's loudest section), low-end mono below 120 Hz, stereo width, crest factor, hits per second, transient sharpness and brightness. Output is one line per difference, e.g. `Drop 1: sub (20-60 Hz) 3.1 dB under the reference`.
4. Exact copying isn't possible (synths, samples, effects, layered mix), so work in steps: pick the worst section, match one stem against the matching Demucs stem of the reference (`stems.md`), re-capture, re-run, refine. Then the next section.

## Report
Tempo (±1.5 BPM is a match), key, bands sub/low/mid/high-mid/air (dB rel. total), LUFS, onsets/s, centroid. Write the diffs in the song sheet next to the version number. Change one or two things per round; about five rounds max.

## Remember
Numbers say "closer", not "good". Sound choice and hook decide the rating (`../taste_log.md`).
