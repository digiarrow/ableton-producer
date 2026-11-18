# Mario Instrumental (study remake of David Guetta & Jast - Mariô, Extended Mix)

Full sheet with every round lives on the Mac: ~/Documents/Ableton/songs/mario-instrumental/sheet.md (rebuild scripts in its tools/). This is the project copy, 2026-11-12.

## Brief
Instrumental, no vocals. Match the reference's tempo, key, form, groove, palette and balance; all melodic parts are original (no reference audio in the set).
Reference: ~/producer-agent/references/David Guetta & Jast - Mariô (Extended Mix).mp3. Analysis JSONs: ~/producer-agent/analysis/mario-ref.json (+ intro, break1, drop1, drop2).

## Reference numbers
220 s, 126.0 BPM, A minor, -6.9 LUFS. Bands (dB rel. total): sub -5.9, low -2.3, mid -10.3, high-mid -13.9, air -18.4. Onsets 6.85/s, centroid 2832 Hz.
Harmony: bass on A through the drops; Am, Dm/D, F. Breaks Am → C → Esus → Am.

## Fundamentals
126 BPM, 4/4, A minor (Dorian F# in the D chord). Drops: Am7 | D/A | Fmaj7 | G over an A pedal. Break: Am(2) F(2) C(2) Esus(1) E(1).

## Form (113 bars, locators set; reference timestamp)
Intro 1–24 (0:00) · Break 1 25–32 (0:46) · Drop 1 33–56 (1:01) · Breakdown 57–60 (1:47) · Groove no kick 61–68 (1:55) · Build 2 69–81 (2:10) · Drop 2 82–97 (2:35) · Drop 2b 98–105 (3:05) · Outro 106–113 (3:20) · End 114

## 8-track plan
1 Kick (909 kit) · 2 Drums Top (909 clap, 16th hats, ride, rims, rolls, crashes) · 3 Perc Brazil (Percussion Core Kit: shaker, cabasa, 3-2 claves, congas, bongos, tambourine, cowbell) · 4 Bass (Mini 3 OSC, low-pass) · 5 Chords Stabs (Drift "Stereo Saw", reverb, OTT, -3 dB Utility after OTT) · 6 Hook Lead (Analog Stab Lead, dotted-8th delay, reverb) · 7 FX Risers (white-noise risers → Valhalla Supermassive) · 8 FX Impacts (stock impacts)
Notes: Surge XT / TAL-NoiseMaker expose no parameters to AbletonMCP, so stock Drift/Simpler used. No sidechain (MCP can't set routing); offbeat bass leaves room for the kick.

## Stage status
Brief ✓ · Arrangement ✓ (critic not run yet) · Sound design ✓ rough · Mix: rounds v1–v6 on Drop 1 · Master: not started (~12 LU below reference)

## Decisions log (Drop 1 vs reference 61.0–106.7 s; diffs sub/low/mid/high-mid/air dB)
- 2026-11-12 capture fix: Live ignores playhead moves while stopped; capture script now starts from the locator and trims record.py's ~1 s start delay.
- v1 baseline -1.4/-0.2/+2.8/+0.2/+2.0, peak 1.00 (clipping).
- v2 Chords -3 dB, top kit High Gain 75→60: -1.3/-0.1/+2.7/-0.7/+1.0.
- v3 Kick +4 dB (was 8 LU under bass), low-pass on bass: -0.4/+0.1/+0.7/-1.1/+1.1.
- v4 all tracks -3 dB headroom, Hook +1.5: mids +1.9, peak 0.92.
- v5 Hook back, hats darker: mids +1.7 (OTT after trim undid it).
- v6 kept: Utility -3 dB after OTT on Chords: -0.3/+0.2/+0.3/-1.8/+0.7, onsets 7.85 vs 8.14/s, peak 0.81.
- Break pads up an octave: Break 1 high-mids -5.4 → -1.4.

## Final numbers by section (sub/low/mid/high-mid/air)
Intro +0.2/-0.1/-1.0/+0.6/+4.1 · Break 1 +4.4/+3.9/-1.5/-1.4/+2.3 · Drop 1 -0.3/+0.1/+0.3/-1.8/+0.7 · Drop 2 -0.2/+0.2/+0.3/-2.5/-0.1

## Open gaps
Drop high-mids -2 to -2.5 dB (reference vocal fills 2–6 kHz); intro hats bright (air +4); Break 1 extra low end from bar-25 impact and fewer hits; no master chain; critic not run.

## Digi Arrow's listening notes
2026-11-12 14:16: "awful, not even close". Build v6 rejected; needs a redo (specifics still to come). Vital 1.6.4 + Kilohearts Essentials now installed on the Mac; use Vital for the redo instead of stock Drift/Simpler. Live set left unsaved at that point.

## Redo v2 (2026-11-12, in progress; full groove template in the Mac sheet)
- Old set discarded unsaved. Fresh set: 126 BPM, 8 named tracks (Kick, Drums, Perc, Bass, Lead Hook, Chords Stabs, FX Risers, Impacts), no parts yet.
- Reference drop study: kick long and punchy (~200 ms) tuned near A; bass = offbeat A pedal with a growl that swells into each kick (pump), drops out on beat 4 every 4 bars and in bars 48, 55–56; bars 33–40 almost no hats, offbeat hats + claps from bar 41; hook = 4 short shouts per 4 bars in fixed 16th slots around A4, bright brassy top, 16th stutter every 8th bar.
- Vital: exposes no parameters to Live/MCP, but presets converted to a Live-loadable format on the Mac; "Growl Bass Sidechain" preset has a tempo-locked pump (fakes the sidechain).
- Stopped: Remote Control usage limit (extra_usage_unavailable). Next: write parts, audition sounds vs reference layers, arrange, capture rounds, critic, master.
