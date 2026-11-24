# Analysis (any stage)

Load with `_common.md` whenever a stage ends or a change needs checking. Full procedure: `/mnt/project-files/agents/reference-analysis/SKILL.md` (account skill `ableton-reference-analysis`). Summary:

## Silent output
Live's output device is the aggregate **"Agent Out"** on the Mac: channels 1/2 = BlackHole (silent, the agent's ears), 3/4 = Digi Arrow's speakers/headphones. Normally the Main/Master goes to 3/4.

## Render an 8-bar loop
1. `set_master_output("1/2")` (now nobody hears it). If the tool is missing or fails, **do not play**; ask Digi Arrow to play while you record, or skip.
2. Start `~/producer-agent/.venv/bin/python ~/producer-agent/record.py --seconds <8 bars = 8*4*60/BPM> --out ~/producer-agent/renders/<song>-v<NN>-<section>.wav` in the background; start playback from the locator; stop when recording ends.
3. `set_master_output("3/4")`. **Always**, even if something failed.
4. `analyze.py <render> --compare ~/producer-agent/analysis/<ref>.json --start <s> --end <s>` comparing the same section of the reference.

For a single layer, solo the track before capture (and unsolo after) to compare it with the matching reference layer.

## Report
Tempo (±1.5 BPM is a match), key, bands sub/low/mid/high-mid/air (dB rel. total), LUFS, onsets/s, centroid. Write the diffs in the song sheet next to the version number. Change one or two things per round; about five rounds max.

## Remember
Numbers say "closer", not "good". Sound choice and hook decide the rating (`../taste_log.md`).
