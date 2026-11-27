# Stage 6: Mix

Load with `_common.md` and `best_practices.md` (frequency slots, FX restraint). Clutter is an arrangement problem: if parts fight, remove or move one before reaching for EQ. For detail, grep `/mnt/project-files/references/mixing-secrets.txt` for the chapter (Ch 3 low end, Ch 8 balance, Ch 9 compression, Ch 11 EQ, Ch 14 side chains, Ch 16 reverb).

## Mixdown checklist
- [ ] Headroom: master peaks around -6 dBFS before any master processing (Utility gain on tracks, not the master fader).
- [ ] Balance from kick and bass up; hook next; everything else under.
- [ ] Low end mono below 120 Hz (Utility Bass Mono on bass and the master).
- [ ] One sub owner; kick and bass don't clash (ducking working; check capture peaks).
- [ ] High-pass everything that doesn't need lows (TDR Nova or EQ Eight).
- [ ] Mids not muddy: compare the mid band with the reference; cut pads/chords 200 to 500 Hz first.
- [ ] Brightness: high-mid and air within about 2 dB of the reference; hats not harsh.
- [ ] Space on the two returns (reverb A, delay B), high- and low-passed; sends set by Digi Arrow if AbletonMCP can't.
- [ ] Every compressor has a reason in the log.
- [ ] Frequency slots (`best_practices.md` section 6): one owner per slot, no two melodic parts in the same octave at once.
- [ ] Three focal parts audible in every drop; everything else at least 6 dB under the foreground.
- [ ] FX restraint: no effect on the Main or drum bus in drops; FX at least 6 dB under the drums and high-passed; no reverb or delay tails spilling into drops; every effect has a reason in the sheet.
- [ ] Mono and low-volume check of each drop: kick and hook still read.
- [ ] Loudness: compare balance at matched loudness; a rough mix sits 6 to 12 LU under a mastered reference, that's fine here.
- [ ] Nothing clips anywhere (peak under 1.0 in the capture).

## Done when
All boxes ticked, each section's bands within about 2 dB of the reference, version saved and rated.
