# Stage 5: Arrangement

Load with `_common.md`. Goal: a DJ-ready track whose energy curve follows the reference.

## Steps
1. Open the reference's structure map (`../references/<track>.md`). If it has none, make one: analyze the reference by section (`analyze.py --start/--end`) and fill the template.
2. Plan the energy curve (1 to 10 per section) and write it in the song sheet. Typical tech house: Intro 32 (drums, then bass) · Break 16 · Build 8 · Drop 32 · Break 16 to 32 · Build 8 · Drop 32 · Outro 32. Progressive: longer intro and break, slow filter journeys.
3. **DJ intro and outro:** 16 to 32 bars, drums (and bass) only, no harmony or long reverb tails at the edges, clean 8-bar phrases so a DJ can mix in and out.
4. Lay out clips in the arrangement (`duplicate_to_arrangement`) and set locators at each section.
5. **Something changes every 8 or 16 bars:** add or remove a layer, filter sweep, hat pattern change, fill on the last bar, automation. AbletonMCP can't draw automation reliably; use clip variants or ask Digi Arrow to draw the sweep.
6. Transitions: riser and snare/clap roll into drops, one bar of silence or kick drop before the drop, crash on bar 1.
7. Energy check: capture each section silently and compare loudness and onset density curve with the reference sections.

## Done when
Every section has a locator, the energy curve matches the plan, intro and outro are DJ-friendly, version saved and rated.
