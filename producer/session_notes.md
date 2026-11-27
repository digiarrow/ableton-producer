# Session notes

Written at the end of every session: what worked, what didn't, what was learned. Read before starting. Newest first.
Format: `## date · song · versions made`, then three short lists.

## 2026-11-27 · setup · none
- Worked: improvement plan sections added: section-by-section comparison (`tools/producer-agent/sections.py`, `skills/analysis.md`) and creative direction (`creative_direction.md`, wired into the checklist, hook and arrangement skills).
- Didn't: `sections.py` is tested on synthetic audio only; first real run on the Mac still to do.
- Learned / next: copy `sections.py` to `~/producer-agent/` on the Mac and run it once on a Mariô or Spotlight capture. Ask for a scout trend report before the next original track (none in `scout/` yet).

## 2026-11-18 · setup · none
- Worked: producer rules, checklist, stage skills and logs set up in `producer/`.
- Didn't: nothing built this session.
- Learned / next: `template.als` still to be made (AbletonMCP cannot save sets, so Digi Arrow saves it once). Mariô redo v2 is still open on the Mac.

## 2026-11-12 · mario-instrumental · v1 to v6, redo v2 started
- Worked: silent capture through BlackHole + analyze.py; per-section comparison with the reference; capture script fix (Live ignores playhead moves while stopped, so start from the locator).
- Didn't: the whole build. Stock Drift/Simpler sounds and a numbers-only process gave a track Digi Arrow called "awful, not even close". Surge XT, TAL-NoiseMaker and Vital expose no parameters to AbletonMCP.
- Learned: pick sounds and the hook first, by ear-proxy comparison against reference layers (solo captures, layer by layer), then balance. Vital presets can be converted to a Live-loadable format; "Growl Bass Sidechain" fakes a sidechain pump, since AbletonMCP can't set routing. Redo stalled at the Remote Control usage limit with an unsaved 8-track set.

## 2026-11-21 · mario-instrumental · self-audit (after v07–v09)
- Worked: Demucs stems (v08 on) made drum choice far closer; per-hit matching (v09).
- Didn't: numbers-first sound choice; analysis against the full mix; tech house defaults (16th hats, swing, perc) imposed on a straight Guetta track; hook too sparse (chant is ~3 notes/bar and carries the identity); lost unsaved set; silent first 32 bars looked like broken audio.
- Learned / next: match one stem at a time and move on only after a "close" rating; weight the hook most; ask Digi Arrow to save after every stage; always put content at bar 1.
- Measured audit (stems): in their drop bass ≈ drums (both ~-12 LUFS) and the chant fills the mids, so rating drums alone vs the full song was unfair. Drum gaps: bars 33–40 inverted (theirs kick + offbeat hats, no clap); ours mono (0.99) vs theirs wide (0.95, ~7 dB side in mids/highs); kick over-saturated (crest 8.9 vs 12.3 dB, attack 19 vs 8.5 ms, pitch 69 Hz start vs 92→47 Hz); clap too dark (1.8 vs 4.9 kHz centroid, their tail ~400 ms); missing quiet 16th shaker (~-14 dB under kick); hats +3/+5 dB loud. No version was ever saved (versions folder empty). Rule: next rating is drums + bass; check stereo every round.
