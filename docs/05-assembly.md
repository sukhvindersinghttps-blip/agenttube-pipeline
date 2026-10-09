# 05 — Assembly

Clips + voiceover are assembled with `ffmpeg`. The critical detail is **crossfade duration math** — get it wrong and the video ends up shorter than the VO with progressive A/V drift.

## The fade math

With `n` clips and a crossfade of `F` seconds between each:

```
video_duration = Σ(clip_durations) − (n − 1) × F
```

If each clip is trimmed to exactly its beat duration `dᵢ`, the video loses `(n−1)×F` seconds — e.g. 140 beats × 0.35s fades = **48.65s lost**, and the audio gets truncated at the video length (lost ending/CTA). Worse, visuals drift earlier than narration by `i×F` at beat `i`.

### The fix

Trim clip `i` to:

```
L₀ = d₀                    (first clip: no fade before it)
Lᵢ = dᵢ + F   for i ≥ 1    (cover the fade overlap)
```

Then `video_duration = Σ(dᵢ)` exactly, and each visual sits a constant `F` early (the natural fade lead-in) with no progressive drift.

## Pipeline

1. `trim` + `setpts` each clip to its `Lᵢ`
2. `scale`/`crop` to 1920×1080, `fps=30`
3. Chain `xfade=transition=fade:duration=0.35`
4. `atrim` audio to final duration, `asetpts`, `loudnorm`
5. Encode: `libx264 -preset medium -crf 19`, AAC 128k
6. Render a 720p review copy alongside the 1080p master

## Verification

- Final duration must equal VO duration (±0.5s).
- Spot-check 3+ sync points: visual on screen matches the narration line.

See [`scripts/assemble.py`](../scripts/assemble.py) for the reference implementation.
