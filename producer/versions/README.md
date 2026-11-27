# Versions

Every saved attempt, numbered (rule 7). After each stage's loop, or any change Digi Arrow will hear, save a new version and ask for a rating from 1 to 10.

## Naming
- Live set: `songs/<song>/versions/<song>-v<NN>.als` (two digits, never reused, never overwritten), e.g. `kuduro-house-v03.als`.
- Silent capture of the same version: `~/producer-agent/renders/<song>-v<NN>-<section>.wav`.
- One line per version in the song sheet's decisions log and in `taste_log.md` once rated.

## How to save
AbletonMCP cannot save a set. In order of preference:
1. If computer-use tools for Live are available, use File > Save Live Set As (Cmd+Shift+S) and type the name.
2. Otherwise ask Digi Arrow: "Please Save As `<song>-v<NN>.als` in `songs/<song>/versions/`", and wait for the yes before the next stage.
Never save over an earlier version.

## template.als (made 2026-11-24)
Saved on the Mac at `~/Documents/Ableton/producer/template.als`: Kick, Drums, Perc (empty Drum Racks), Bass (Compressor: thresh -25 dB, 4:1, attack 0.1 ms, release 100 ms, sidechain from Kick post FX; then Utility), Hook and Chords-Pads (Utility), FX and Spare (audio). Returns: A-Reverb (100% wet), B-Delay (3/16 synced, 100% wet). Main: Utility -6 dB, then SPAN. Tempo 120 placeholder. Start every song with File > Open template.als, then immediately Save As `<song>-v01.als`; never save over the template.

Original plan:
A starting set with: 8 named tracks (Kick, Drums, Perc, Bass, Hook, Chords/Pads, FX, spare), the kick sent to the bass's sidechain (Compressor or Kilohearts/TDR ducking) so routing is done once, a reverb and a delay on the two returns, Utility at -6 dB headroom on the master and SPAN last. No fixed tempo. Saved as `~/Documents/Ableton/producer/template.als` and in Live's User Library > Templates. AbletonMCP can't set routing or save, so Digi Arrow sets the sidechain and saves it, guided step by step.
