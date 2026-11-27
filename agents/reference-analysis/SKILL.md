---
name: reference-analysis
description: Let the Ableton producer agent hear its own track silently (Master routed to BlackHole), measure it with analyze.py and compare it against a reference track, then iterate in small steps. Use after building or changing a track, or when Digi Arrow asks for something "like" a reference.
---

# Reference-based track analysis

Gives the producer agent ears: capture the track silently, measure it, compare it with a reference, change one or two things, repeat. Loaded by `ableton-lead-producer`; it is the only agent that edits Live.

## Where things live (Mac, the main production machine)

```
~/producer-agent/.venv/        Python env (librosa, soundfile, pyloudnorm, sounddevice, numpy)
~/producer-agent/record.py     records BlackHole into a WAV
~/producer-agent/analyze.py    measures a WAV, --compare against a reference
~/producer-agent/sections.py   section-by-section comparison against a reference, differences only
~/producer-agent/references/   reference tracks Digi Arrow bought (WAV or high-quality MP3)
~/producer-agent/renders/      the agent's silent captures
~/producer-agent/analysis/     saved JSON results
```

Run scripts as `~/producer-agent/.venv/bin/python ~/producer-agent/<script>.py ...`. Masters of the scripts are in the project folder at `tools/producer-agent/`.

Audio routing (set once by Digi Arrow): Live's output device is the aggregate device **"Agent Out"**. Channels 1/2 = BlackHole (silent, the agent's ears), 3/4 = headphones/interface. Normally the Master goes to **3/4**.

## Before the first round, check

- `record.py --list` shows a BlackHole input. If not, stop and ask Digi Arrow to finish the BlackHole setup.
- AbletonMCP has the `set_master_output` tool. If it doesn't, Live was opened before the Remote Script was patched, or Claude Code was started before Live: ask Digi Arrow to restart Live, then Claude Code.

## Steps

1. If a reference has no JSON in `analysis/`, run `analyze.py <ref> --save ~/producer-agent/analysis/<name>.json`.
2. `set_master_output("1/2")`. Digi Arrow now hears nothing.
3. Start `record.py --seconds <section length> --out ~/producer-agent/renders/<song>-<section>-r<round>.wav` in the background, then start playback through AbletonMCP from the section's locator. Stop playback when recording ends. Section length in seconds = bars × 4 × 60 / BPM.
4. `set_master_output("3/4")`. **Always do this, even if something failed.** Then confirm with Digi Arrow's routing that the Master is back on 3/4.
5. `analyze.py <render> --compare <ref json>`. For sections, use `--start/--end` (seconds) on the reference so you compare drop with drop, not drop with whole track.
6. **Whole track or arrangement:** capture from bar 1 and run `sections.py <capture> <ref audio> --bpm <ours> --ref-bpm <theirs> --map <reference structure map .md> [--sections "Intro:1-32,..."] --json <file>`. It splits both tracks into matching sections (map bars or Ableton locators) and prints only the differences per section (spectrum, bands, energy curve, low-end mono, width, crest, hits/s, transients, brightness).
7. Read the differences (below), change one or two things, log them, repeat from step 2. Stop after about five rounds or when everything is within tolerance, then report to Digi Arrow with what changed and the before/after numbers.

## Reading the results

- **Tempo:** librosa's estimate is coarse (128 often reads as 129.2), so treat anything within about 1.5 BPM as a match and trust the session tempo. Otherwise set the session tempo.
- **Key:** if different, transpose the MIDI clips (ask first: it overwrites notes).
- **Band balance (dB relative to total):** sub (20–60 Hz) and low (60–250 Hz) are the core of tech house. More than 3 dB under the reference: raise bass or kick level, or swap the sound. Over: cut with EQ or check the sidechain.
- **Mids (250 Hz–2 kHz):** too high usually means muddy chords or pads. **High-mids (2–6 kHz)** and **air (6–20 kHz)** control brightness: hats, percussion, top of leads.
- **Loudness (LUFS):** a rough mix is quieter than a mastered reference. Compare balance, not loudness, until the master stage.
- **Onset density (hits/sec):** lower than the reference means the groove is sparse (add percussion or hats); higher means busy.
- **Spectral centroid:** overall brightness; use it to confirm the band readings.

## Rules

- Numbers say "closer to the reference", not "good". Final judgement stays with Digi Arrow.
- **This is the only exception to "never auto-play"**: playback is allowed only while the Master is routed to 1/2 (BlackHole), so Digi Arrow hears nothing. Never start playback with the Master on 3/4. If `set_master_output` is missing or fails, do not play; ask Digi Arrow to play the section while you record instead.
- Change small things per round and log each change and its effect in the song sheet's decisions log.
- Reference tracks are for study. Never copy their melodies or samples into tracks meant for release.
- Windows PC: no aggregate device. Needs VB-Cable plus an ASIO driver exposing both (e.g. ASIO4ALL) for the same 1/2 vs 3/4 routing, and `record.py --device "CABLE Output"`. Not set up yet.
