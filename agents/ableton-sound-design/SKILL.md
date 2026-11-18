---
name: ableton-sound-design
description: Use when Digi Arrow asks for a sound and no suitable sample exists: builds it in Live 12 Lite with a native instrument or installed plugin, writes a demo MIDI clip (never played) and offers to resample.
---

# Sound design

Use this skill when Digi Arrow asks for a sound and no suitable sample exists. You work under the `ableton-lead-producer` rules: never auto-play, ask before deleting or overwriting anything, never download or buy anything without approval, and log decisions in the song sheet if there is one.

## 1. Check for a sample first

Briefly check the Live browser (`get_browser_tree`, `get_browser_items_at_path`) and the User Library for a fitting sample. If one fits, offer it. Design a sound only when nothing suitable exists or Digi Arrow asks for one.

## 2. Pick the instrument

Choose the instrument that fits the sound best. Before loading a native instrument, confirm it's in this Live edition with `get_browser_tree`. Digi Arrow runs **Live 12 Lite**: Drift, Simpler, Impulse and Drum Rack are available; Wavetable, Analog and Operator are Standard/Suite instruments and are probably not. Lite also caps stock instruments at 5 per set, so count them.

| Sound | First choice | Lite / plugin fallback |
|---|---|---|
| Basses, leads, pads | Wavetable or Analog (if present) | Drift (stock, Lite), Surge XT, TAL-NoiseMaker |
| Plucks, bells, FM sounds | Operator (if present) | Dexed (FM, DX7-style), Surge XT FM modes |
| Drums | Drum Rack with Simpler | Drum Rack with Simpler (Lite), Reason Kong |
| Evolving textures | Wavetable (if present) | Surge XT wavetable, Reason Europa |

Genre leads: rolling tech house bass = Drift or TAL-NoiseMaker, saw or square, low-pass with short filter envelope; progressive techno bass and pads = Surge XT wavetable with a slow LFO or macro on position and cutoff; stabs and plucks = Dexed or Drift with fast decay.

## 3. Third-party plugins: check what's exposed

Before relying on a plugin parameter, call `get_device_parameters` on the loaded plugin and confirm the parameter is there. Live shows only the parameters a plugin exposes (sometimes after "Configure" in the device header).
- If a needed parameter isn't available, load a close preset by name instead, or tell Digi Arrow exactly which setting to change in the plugin window ("in Surge XT, Filter 1 cutoff to about 40%, Env 1 decay to 180 ms").
- Don't guess parameter indexes.

## 4. If nothing installed can do it well

Say so, and suggest plugins Digi Arrow could get, **free ones first**, each with one line on what it adds (for example Vital: visual wavetable synth for modern basses and leads; Spitfire LABS: free organic and cinematic textures; Kilohearts Essentials: free utility and character FX). Never download or buy anything without Digi Arrow's approval.

## 5. Shape the sound

Set oscillator, filter, envelope and effects parameters with `set_device_parameter`, following genre conventions and the knowledge base:
- grep `/mnt/project-files/references/live12-manual.txt` for the device chapter (e.g. "Drift", "Simpler") for parameter meaning and ranges;
- grep `making-music-desantis.txt` for "Presets as Starting Points", "Simple Sounds", "Tuning Everything", "The Tyranny of the Default";
- keep sub content to one bass source and leave room for the kick (sound design shouldn't create mix problems).

Start from a preset when one is close, then change the 2 or 3 parameters that matter. Effects: Saturator or Reason Scream 4 for grit, Auto Filter for movement, Xfer OTT (low mix) for bite; space goes on the returns (see `ableton-arrange-and-sound` stage 3).

## 6. Demo clip, never played

- Put the sound on a new track (don't replace an existing one without asking; respect the 8-track limit).
- Name the track clearly by role and character, e.g. `BASS rolling Drift`, `PLUCK FM Dexed`.
- Write a short MIDI clip (1 to 4 bars) in the song's key and tempo that shows the sound in a genre-typical pattern, and name it (e.g. `demo bass 16ths`).
- **Never fire the clip or start playback.** Tell Digi Arrow which clip to launch.

## 7. Explain

In plain language, in a few lines: which instrument and why, the key settings and what each does to the sound, and one or two tweaks to try if they want it darker, brighter, shorter or wider.

## 8. Resample offer

If Digi Arrow likes it, offer to resample it to audio so it can be reused like a sample: a new audio track with input set to the synth track (or Resampling), record the demo, trim, and save to the User Library (`C:\Users\NEO\Documents\Ableton\User Library\Samples\Digi Arrow`). Recording needs transport, so ask Digi Arrow to press record and play themselves, or get their explicit OK before you start recording. Freezing and flattening the original track replaces it, so ask first.
