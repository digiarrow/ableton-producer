# Stage 2: Bass

Load with `_common.md`. Goal: a bass that locks with the kick and makes the groove move.

## Writing
- **Lock to the kick.** No bass note on the kick's downbeat unless the kick is short and the bass ducks. Tech house: offbeat ("&") notes, 16th pickups into the next kick, octave jumps. Progressive techno: long rolling 16th lines on one note, movement from filter.
- One root note through the drop works (the Mariô reference holds an A pedal). Leave a gap on beat 4 every 4 bars for air.
- Note length matters more than note count: try 1/16 vs dotted-1/16 vs 1/8.

## Sound recipes
| Style | Source | Settings |
|---|---|---|
| Rolling tech house | Vital or Drift saw/square | low-pass 300 to 800 Hz, short filter envelope (decay 80 to 150 ms), mono, slight drive |
| Offbeat growl with pump | Vital "Growl Bass Sidechain" preset | tempo-locked volume LFO fakes the sidechain |
| Progressive rolling | Surge XT / Vital wavetable | slow LFO on wavetable position and cutoff, long notes |
| Prodigy-style | Vital or Surge with distortion | Saturator or Kilohearts Distortion, then low-pass |
| Sub only | Operator/Drift sine | under a separate mid bass, sub below 100 Hz only |

## Kick and bass
1. Ducking: real sidechain (Compressor on bass keyed from Kick: ratio 4:1, attack 0 to 1 ms, release 80 to 150 ms). AbletonMCP can't set the key input, so it comes from `template.als` or Digi Arrow sets it. Fallbacks: Vital pump preset, a volume LFO, or Kilohearts/TDR Nova dynamic band.
2. One owner of the sub: high-pass the bass under the kick's fundamental or low-pass the kick tail. Bass mono below 120 Hz.

## Done when
Sub and low bands within about 2 dB of the reference drop, kick and bass don't stack (check the waveform/peaks of the capture), version saved and rated.
