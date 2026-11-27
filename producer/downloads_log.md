# Downloads log

Every free plugin, sample pack or preset the agent downloads or installs. Rules in `skills/downloads.md`. Never paid, trial or pirated software. Newest first.
Format: date · machine · name and version · source URL · licence · where installed · why · verified (loads in Live: yes/no)

## 2026-11-27
- 2026-11-27 · Mac · audiobox_aesthetics 0.0.4 + torch 2.15.0, torchaudio 2.11.1, requests, soundfile in ~/producer-agent/.venv-aes (Python 3.11 via uv) · PyPI · CC BY 4.0 · weights facebook/audiobox-aesthetics from Hugging Face (415 MB, CC BY 4.0) · quality scores for the critic (`skills/ear.md`) · tested
- 2026-11-27 · Mac · laion_clap 1.1.7 + numpy 1.26.4, torch 2.15.0, torchaudio, torchvision, transformers 5.24.1 in ~/producer-agent/.venv-clap (Python 3.11 via uv) · PyPI · CC0 · describe-and-match (`clap_match.py`) · tested
- 2026-11-27 · Mac · CLAP checkpoint music_audioset_epoch_15_esc_90.14.pt (2.35 GB) + roberta-base text model · huggingface.co/lukewys/laion_clap · CC0 (roberta MIT) · ~/producer-agent/models, ~/.cache/huggingface · tested
- 2026-11-27 · Mac · librosa 1.0.1, pyloudnorm 0.2.0, soundfile 0.14.0 added to ~/producer-agent/.venv-genre · PyPI · ISC / MIT / BSD · feel.py, taste.py, blind.py · tested

## 2026-11-24
- 2026-11-24 · Mac · venv ~/producer-agent/.venv-tools (CPython 3.11.18 via uv): basic-pitch 0.4.0 (Apache-2.0, model inside the wheel), matchering 2.0.6 (GPLv3), pyloudnorm 0.2.0 (MIT), soundfile, coremltools 9.0 · PyPI · analysis tools (`skills/midi.md`, `skills/loudness.md`) · tested
- by 2026-11-19 · Mac · demucs 4.1.0 (MIT) + torch in ~/producer-agent/demucs-venv, model htdemucs 84 MB from Hugging Face (adefossez/HTDemucs) · stem splitting (`skills/stems.md`) · tested 2026-11-24
- 2026-11-24 · Mac · CPython 3.12.16 (uv-managed) · python.org builds via `uv python install` · PSF · ~/.local/share/uv · venv ~/producer-agent/.venv-genre for genre recognition · n/a (not a plugin)
- 2026-11-24 · Mac · essentia-tensorflow 2.1b6.dev1389 (+ numpy, pyyaml, six) · PyPI · AGPL-3.0 · ~/producer-agent/.venv-genre · genre recognition (`skills/genre.md`) · n/a (not a plugin)
- 2026-11-24 · Mac · Discogs-EffNet models: discogs-effnet-bs64-1.pb (18.4 MB), genre_discogs400-discogs-effnet-1.pb + .json · essentia.upf.edu/models · CC BY-NC-SA 4.0 (non-commercial only) · ~/producer-agent/models · genre recognition · tested on the Mariô reference

## Before this log existed (installed with Digi Arrow's approval)
- 2026-11-12 · Mac · BlackHole 2ch 0.7.1 · existential.audio (official pkg) · GPL-3.0 · /Library/Audio/Plug-Ins/HAL · silent analysis output · yes
- 2026-11-12 · Mac · Vital 1.6.4 (free tier) · vital.audio · free account · ~/Library/Audio/Plug-Ins (VST3+AU) · wavetable synth for the Mariô redo · yes
- 2026-11-12 · Mac · Kilohearts Essentials · kilohearts.com · free account · ~/Library/Audio/Plug-Ins · free FX · yes
- by 2026-11-12 · Mac · Surge XT, TAL-NoiseMaker, Valhalla Supermassive, Valhalla Freq Echo, Xfer OTT, TDR Nova, Voxengo SPAN · official sites · free · ~/Library/Audio/Plug-Ins · yes
- 2026-10-25 · Windows · Surge XT, TAL-NoiseMaker, Dexed, Valhalla Supermassive, TDR Nova, TDR Kotelnikov, Xfer OTT, Voxengo SPAN, Youlean Loudness Meter 2, Reason Rack Plugin (free) · official sites · free · C:\Program Files\Common Files\VST3 · yes
