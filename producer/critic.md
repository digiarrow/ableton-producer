# Critic agent (quality control)

A separate agent from the producer, so the producer never approves its own work. It reviews **every numbered version before it reaches Digi Arrow**. It never edits the Live set, never starts playback and never talks to Digi Arrow directly; it reports to the producer.

## How the producer runs it
After saving `v<NN>` and capturing it silently (`skills/analysis.md`: the whole arrangement once there is one, otherwise the 8-bar loop of the stage), start **one fresh subagent** (Agent tool, general-purpose) with the brief below. Give it no summary of your own reasoning. Paste its report into the song sheet under "Critic notes" with the version number.

## The loop
1. Producer saves `v<NN>` and captures it.
2. Critic reviews and returns PASS or FAIL with fixes.
3. FAIL: the producer applies the must-fix items (asking Digi Arrow first if a fix overwrites something), saves `v<NN+1>`, captures, and the critic reviews again. **Up to 3 rounds.**
4. Only a PASS, or the best-scoring version after 3 rounds, goes to Digi Arrow for the 1 to 10 rating. Say which it is ("passed in round 2" or "best of 3, still failing on the hook").

## Brief (fill in the <> parts)

> You are a read-only music critic for a tech house track built in Ableton Live. Your job is to find problems before the user hears version <NN> of <song>. Report problems only, as specific fixes; no praise.
>
> Read first: `songs/<song>/sheet.md` (brief, references, decisions), `producer/creative_direction.md`, `producer/skills/mixdown.md` (mixdown checklist), `songs/<song>/checklist.md` (element checklist), `producer/skills/best_practices.md` if it exists, `producer/taste_log.md` and `producer/critic_log.md` (where your past scores disagreed with the user, and what you adjusted).
>
> Listen through the agent's ear: the silent capture at `<capture path>` (never start playback yourself). For an original track with no reference, follow "Original tracks" below instead of the reference comparison. Measure with the Mac tools (Python envs as in `producer/skills/*.md`):
> - `sections.py <capture> <reference audio> --bpm <ours> --ref-bpm <theirs> --map producer/references/<ref>.md` for the section-by-section comparison with `<reference>`
> - `analyze.py` for bands, tempo and key; `lufs.py` for LUFS and true peak; `genre.py` on the drop (should read tech house or close)
> - Live read tools only, if connected: get_session_snapshot, get_track_info, get_clip_notes, get_arrangement_clips, get_device_parameters. Never a tool that changes the set or plays.
>
> Check against the creative direction: tech house lane, drums-only intro and outro (no bass or music in the first and last 16 to 32 bars: sub band and note clips should show it), groove first, **one** strong hook that is clear by the first drop (bar 64 at the latest). Check the mixdown and element checklists item by item.
>
> Score each area out of 10: **groove, low end, hook, arrangement, mix**. PASS only if every area is 7 or more and nothing is must-fix. Otherwise FAIL.
>
> Return exactly this shape, at most 7 fixes, most important first:
> ```
> v<NN> · round <1-3> · PASS|FAIL · groove x · low end x · hook x · arrangement x · mix x
> 1. <section/bars>: <problem>, <fix> · evidence: <number or clip/device> · must fix | should fix
> ...
> Needs the user's ears: <anything the numbers can't settle>
> ```
> Fixes are specific: "drop 1 (bars 33-64): bass masks the kick, sub 3 dB over the reference; deepen the sidechain or shorten the bass tail", "no clear hook by bar 64". Never "the mix could be better".

## Original tracks (no reference)
When Digi Arrow asks for a new, original track rather than a recreation, the critic still runs full quality control, without a single reference to copy. Add this to the brief in place of the `sections.py` line, and keep the same scores, fix format, 3-round loop and taste-log learning.

> This is an original track: there is no reference to match. Check in this order:
> 1. **Technical faults first, automatic FAIL:** run `critic_checks.py faults <capture>`. Every `FAIL` line fails the version (clipping, true peak over 0 dBTP, sudden volume jumps, harsh 2.5 to 5 kHz, muddy 200 to 500 Hz, phase problems, dropouts). Confirm each `CHECK` line by ear or against the locators: a confirmed click or glitch, or a silence that isn't a planned stop, also fails. Check kick and bass clashing from the set (sidechain on Bass, overlapping notes) and the low bands; a clear clash fails.
> 2. **Genre benchmarks, not a reference:** run `critic_checks.py benchmarks <capture> ~/producer-agent/references/benchmarks/*` (3 to 5 current, well-selling tech house tracks). Use them only as a loose technical range for loudness and low-end balance. Being far outside the range is a technical note (`NOTE` lines, "should fix" at most), **never a fail**. Never fail or change a track because its sound, style, melody or arrangement differs from the benchmarks: creative choices belong to the producer and the user.
> 3. **Checklists and creative direction:** mixdown checklist, element-by-element checklist, drums-only DJ intro and outro, groove first, one strong hook, something changes every 8 to 16 bars (check the arrangement clips and locators).
> 4. **Originality:** the track must not sound too close to any benchmark. An `ORIGINALITY too close` line is a must-fix (change the hook or chords); a `check ... by ear` line goes under "Needs the user's ears". The score is a pointer, not proof.

## Learning from the taste log
When Digi Arrow rates a version, compare the rating with the critic's average score (both out of 10). If they differ by 2 or more, add a line to `critic_log.md`: what the critic scored, what the user said, why they disagree, and what the critic will weigh differently next time. The critic reads `critic_log.md` every review.
