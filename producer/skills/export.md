# Stage 7: Export

Load with `_common.md`. Digi Arrow does the actual export from Live (File > Export Audio/Video); the agent prepares the settings and checklist.

## Free mastering chain (on the Main/Master, in order)
1. TDR Nova: broad moves only (under 2 dB), low cut under 25 to 30 Hz.
2. Glue Compressor (stock) or TDR Kotelnikov (Windows): 1 to 2 dB gain reduction, slow attack, auto release.
3. Limiter (stock): ceiling -1.0 dB true peak. More than 3 to 4 dB of reduction means go back to the mix.
4. Voxengo SPAN (Mac) / Youlean Loudness Meter 2 (Windows) last, for readings.

Targets: club/DJ -9 to -6 LUFS integrated; streaming -14 to -9; true peak at or below -1 dBTP. Compare with the reference at matched loudness.

## Exports
- [ ] Premaster: master chain off, peaks around -6 dBFS, 24-bit WAV at the project sample rate.
- [ ] Master: chain on, 24-bit WAV.
- [ ] Stems: kick, drums, perc, bass, hook, chords/pads, FX (Export > Selected tracks / All individual tracks).
- [ ] Key in Camelot notation in the file name and sheet (A minor = 8A, F minor = 4A, G minor = 6A).
- [ ] Name: `Digi Arrow - <title> (<mix>) <BPM> <Camelot>.wav`.
- [ ] Ask for the final 1 to 10 rating; log it; note how it holds up in a DJ set later.
