# Stage 5: Arrangement

Load with `_common.md`. Goal: a DJ-ready track whose energy curve follows the reference.

## Steps
1. Open the reference's structure map (`../references/<track>.md`). If it has none, make one: analyze the reference by section (`analyze.py --start/--end`) and fill the template.
2. Plan the energy curve (1 to 10 per section) and write it in the song sheet. Typical tech house: Intro 32 (drums, then bass) · Break 16 · Build 8 · Drop 32 · Break 16 to 32 · Build 8 · Drop 32 · Outro 32. Progressive: longer intro and break, slow filter journeys.
3. **DJ intro and outro:** 16 to 32 bars, **drums only** (`../creative_direction.md`): no bass, harmony, hook or long reverb tails at the edges, clean 8-bar phrases so a DJ can mix in and out. Bass enters after the intro and leaves before the outro.
4. Lay out clips in the arrangement (`duplicate_to_arrangement`) and set locators at each section.
5. **Something changes every 8 or 16 bars:** add or remove a layer, filter sweep, hat pattern change, fill on the last bar, automation. AbletonMCP can't draw automation reliably; use clip variants or ask Digi Arrow to draw the sweep.
6. Transitions: riser and snare/clap roll into drops, one bar of silence or kick drop before the drop, crash on bar 1.
7. Energy check: capture the whole arrangement silently (or one capture per section) and run `sections.py` against the reference with the structure map (`analysis.md`). Fix the biggest differences one section at a time, starting with the drops.

## Done when
Every section has a locator named like the reference map, `sections.py` shows no energy-curve or low-end differences in the drops, intro and outro are DJ-friendly, version saved and rated.
