# Stage 5: Arrangement

Load with `_common.md` and `best_practices.md` (element budget, subtraction, FX restraint). Goal: a DJ-ready track whose energy curve follows the reference.

## Steps
1. Open the reference's structure map (`../references/<track>.md`). If it has none, make one: analyze the reference by section (`analyze.py --start/--end`) and fill the template.
2. Plan the energy curve (1 to 10 per section) and write it in the song sheet. Typical tech house: Intro 32 (drums, then bass) · Break 16 · Build 8 · Drop 32 · Break 16 to 32 · Build 8 · Drop 32 · Outro 32. Progressive: longer intro and break, slow filter journeys.
3. **DJ intro and outro:** 16 to 32 bars, **drums only** (`../creative_direction.md`): no bass, harmony, hook or long reverb tails at the edges, clean 8-bar phrases so a DJ can mix in and out. Bass enters after the intro and leaves before the outro.
4. **Element budget:** write the planned parts list and count for every section in the song sheet, within the budget in `best_practices.md` section 2 (drop at most 8 parts, one melodic hook, three focal parts). Bring parts in **one per 8-bar phrase**, and take one out as often as one comes in.
5. Lay out clips in the arrangement (`duplicate_to_arrangement`) and set locators at each section.
6. **Something changes every 8 or 16 bars:** add or remove a layer, filter sweep, hat pattern change, fill on the last bar, automation. AbletonMCP can't draw automation reliably; use clip variants or ask Digi Arrow to draw the sweep.
7. Transitions, with restraint (`best_practices.md` section 5): **one** riser *or* sweep *or* roll per transition, plus one impact on the drop downbeat. High-pass everything below 100 Hz in the build and bring it back on the drop. ½ to 1 bar of silence or kick-out before the drop. No whole-mix effect in a drop; every automation is back at its start value by the drop downbeat; no reverb tail or riser spills into the drop.
8. **Subtraction pass** on each drop (`best_practices.md` section 4): mute each non-drum part in turn; anything the drop doesn't miss moves to a break or the second drop.
9. Energy check: capture the whole arrangement silently (or one capture per section) and run `sections.py` against the reference with the structure map (`analysis.md`). Fix the biggest differences one section at a time, starting with the drops.

## Done when
Every section has a locator named like the reference map, `sections.py` shows no energy-curve or low-end differences in the drops, intro and outro are DJ-friendly, every section is within its parts budget, the subtraction pass and FX checks are done, version saved and rated.
