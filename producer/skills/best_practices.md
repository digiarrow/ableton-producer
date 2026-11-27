# Best practices: tech house arrangement and production

Load this with every stage skill from the hook stage on, and before any arrangement or mix decision. These are hard rules unless Digi Arrow asks otherwise. They come from Digi Arrow's feedback (`../taste_log.md`), the two books in `/mnt/project-files/references/` and the web sources at the end.

Why this file exists (2026-11-27): original-01 v03 had "too many elements at the same time" and "an effect that messes with everything"; v02 "lacks energy, not uplifting"; Mariô was rejected on sound choice and hook. All three are arrangement and taste problems, not mixing problems.

## 1. Three things at once
The ear follows about **three things at a time**; at the fourth, attention drops (Senior, *Mixing Secrets* ch. 7, quoting Jack Joseph Puig). At every moment name the three focal parts:
1. **the groove** (kick, clap, hats, perc heard as one drum group)
2. **the bass**
3. **one foreground part**: the hook, *or* a fill, *or* one transition FX, never two of them at full level

Everything else is background: quieter (at least 6 dB under the foreground), filtered, or gone. If you can't say which three parts are in focus in a bar, there are too many.

## 2. Element budget per section
Count **parts playing at the same time**, drums counted one by one (kick, clap, closed hat, open hat, shaker, perc each count 1). Write the count for each section in the song sheet and do not exceed it.

| Section | Max parts | What's allowed |
|---|---|---|
| DJ intro / outro | 5 | drums only |
| Groove (after intro) | 7 | drums + bass + at most 1 perc or texture |
| Break | 4 | no kick, or drums only; at most 1 melodic part (hook teaser or pad) |
| Build | 5 | break parts + 1 riser *or* roll; no new melodic part |
| Drop | 8 | drums (≤5) + bass + hook + at most 1 support layer (pad, stab answer or texture) |
| Second / last drop | 9 | first drop + **one** new layer or a variation, not three |

Melodic foreground: **one** hook per drop. A second melodic part is either an answer in the hook's gaps or it's not there.

## 3. Add one thing at a time
- **One change per 8-bar phrase**, one addition at most (Pig&Dan: make one element strong rather than layering many). The drop downbeat is the exception: the groove and bass return together.
- A new part enters at a phrase start (bar 1, 9, 17, 25 of a section), or fades in over 16 to 32 bars with a filter or volume.
- Something leaves as often as something arrives. Light and shade keep attention; a static full texture turns bland (Senior ch. 7).
- Arrangement audit: list every change in the first two minutes. If the only changes are a riser, a crash and a bass dropout, add musical development (a bass note change, a hook variation, a hat pattern change), not more FX.

## 4. Subtraction pass (do it before every arrangement version)
Arrange by subtraction (DeSantis, *Arranging as a Subtractive Process* and *The Power of Erasing*): it's easier to hear what's bad than to imagine what's good.
1. Capture the densest drop silently.
2. Mute each non-drum part in turn and capture again (or compare the section's bands with `sections.py`).
3. If the drop isn't clearly worse without a part, **remove it from the drop** (keep it for a break or the second drop, or delete it after asking).
4. If two parts clash in the same register, move one an octave or let it play only in the other's gaps; don't fix it with EQ (Senior: "If two things sound crap together, just don't put them together").
"Fullness comes from balancing a few good parts, not from adding more" (DeSantis). If the track feels weak, take a part away first.

## 5. FX restraint
Effects support the transition; they never take over the track.
- **One transition device per transition**: a riser *or* a filter sweep *or* a snare/clap roll, plus at most one impact or crash on the drop downbeat. Not all of them.
- **No effects on the Main/Master or the drum bus during drops**: no filter, Beat Repeat, reverb, phaser, flanger or bitcrusher across the whole mix. A whole-mix effect is allowed only in a build or break, and only for 1 to 8 bars.
- **Every automation returns to its exact start value by the drop downbeat** (filter fully open, send back to its level). Check this in the clip envelope.
- **Nothing spills into the drop**: risers end on the bar before, reverb or delay tails are cut (send to 0 or gate) at the drop. Keep reverb pre-delay low and prefer short plates in the drop; long tails only in breaks.
- **No effect that changes the groove's pitch, timing or stereo image** (pitch-shifting, tape stop, stutter, wide chorus) in a drop. Stutters and tape stops only as a 1-beat or 1-bar fill before a phrase.
- FX sit **at least 6 dB under the drums**, and transition FX are high-passed (from 200 to 300 Hz).
- **A new effect is a version of its own**: add it, capture, compare, save, ask for a rating. Never add a new effect in the same version as new parts, so a bad effect can be found and removed.
- Every effect has a one-line reason in the song sheet. No reason, no effect.

## 6. Frequency slots
One owner per slot. Two parts that fight for a slot is a clash, even if each sounds good alone.

| Slot | Owner | Keep out |
|---|---|---|
| 30 to 60 Hz | sub (bass or kick tail, one only) | everything else high-passed; roll off under 30 Hz |
| 60 to 120 Hz | kick punch, bass body; bass ducks on the kick | pads, hook, FX; mono below 120 Hz |
| 150 to 500 Hz | bass harmonics, clap body | pads cut here first; hook high-passed at 150 to 250 Hz |
| 500 Hz to 4 kHz | **hook** (one register, about one octave) | pads and stabs in a different octave or out of the hook's gaps |
| 2 to 6 kHz | clap crack, hook presence | hats not harsh here |
| 6 kHz and up | hats, shaker, air | risers high-passed and kept under the hats |

## 7. Energy and uplift
Energy comes from groove, contrast and movement, not from more layers.
- **Contrast makes the drop**: the break carries about half the drop's energy or less; the build stays quieter than the drop; **everything below 100 Hz leaves in the build** (high-pass) and returns on the drop downbeat. Leave ½ to 1 bar of silence or kick-out before the drop.
- **Naked groove test**: kick, bass and one percussion part alone must groove for a full minute. If not, fix the groove (bass rhythm, swing, hat placement) before adding anything.
- Bass movement: a rolling, offbeat or octave-jumping bass with one or two notes and a pitch bend on a few is more energy than any pad.
- **Uplifting** (v02 feedback): brighter, rising hook (ends a step up, or uses the 3rd/5th above the root), open hats and claps on the offbeat lift, a filter opening over the build, a major-feeling chord or a stab answer in the second drop. Avoid long minor pads in the drop.
- Mono and low-volume check on every drop capture: the hook and the kick must still read.

## 8. Hook
- Rhythm first, 3 to 5 notes, 2 bars repeated, a change at the end of bar 4 or 8. Call and response with the bass: it plays in the bass's gaps.
- **Hook alone test**: hook with the kick only must already sound like a record. If it needs pads or FX to work, it's the wrong hook or the wrong sound.
- Introduce it in pieces: a filtered teaser in the break, full on the drop.

## 9. Before saving any version from the hook stage on
- [ ] Parts count per section within the budget (section 2), written in the sheet
- [ ] The three focal parts named for each drop
- [ ] Subtraction pass done on the drop
- [ ] FX restraint checks pass (section 5); new effects in their own version
- [ ] No two parts in the same slot or octave at once (section 6)
- [ ] Naked groove and hook alone tests pass

## Sources
- Mike Senior, *Mixing Secrets for the Small Studio*, ch. 7 "Clear out the clutter", "Clashing timbres" (`references/mixing-secrets.txt`, around line 4155).
- Dennis DeSantis, *Making Music*: "Arranging as a Subtractive Process", "The Power of Erasing", "Common Forms 2: Layering as Form", "Maximal Density" (`references/making-music-desantis.txt`, around lines 5270 to 5945).
- Pig&Dan, Magnetic Magazine tech house guide: https://magneticmag.com/2022/05/pig-dans-essential-guide-to-tech-house-production/
- BeatsToRapOn, tech house groove and bassline: https://beatstorapon.com/blog/tech-house-production-groove-bassline/
- MusicRadar, tech house groove: https://www.musicradar.com/how-to/tech-house-groove
- MusicRadar, minimal arrangement tips: https://www.musicradar.com/how-to/9-minimal-track-arrangement-tips-find-out-how-a-little-can-go-a-long-way
- EDMProd, build-ups: https://www.edmprod.com/ultimate-guide-build-ups/
