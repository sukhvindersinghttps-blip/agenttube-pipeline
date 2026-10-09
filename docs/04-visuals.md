# 04 — Visual Generation

**True-motion AI video clips only.** No Ken Burns stills, no image slideshows. Every visual is a generated moving clip.

## The sync bar (critical)

Every visual must appear at the **exact moment** the narration discusses it:
1. Break the VO into sentences/phrases.
2. Assign each sentence one visual.
3. Match durations.
4. Verify after generation.

## Style rules

- Match durations: clip length = narration beat length (+ fade overlap — see [Assembly](05-assembly.md)).
- New visual every ~4–7 seconds (rapid montage pacing).
- Visuals stay consistent with the channel's previous videos and aligned to the narrated era (e.g. 1995 narration → 1995-era visuals).
- Cuts use 0.35s crossfades (see assembly for the duration math).
- No vignette unless the channel style calls for it.
- If a narration beat is longer than the generated clip, loop the clip (filter-level loop, not input-level `-stream_loop` which can hang on MP4 seek).

## Output

- One clip per beat, named per the timing manifest
- `beats_timing.json` — beat → clip → start/end/duration mapping
