# Setup Guide — Run the AgentTube Pipeline Yourself

Follow these steps to set up the pipeline on your own machine and produce your first video.

---

## Step 1 — Fork this repository

1. Open https://github.com/sukhvindersinghttps-blip/agenttube-pipeline
2. Click **Fork** (top right) to copy it to your own GitHub account.
3. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/agenttube-pipeline.git
   cd agenttube-pipeline
   ```

## Step 2 — Install system requirements

| Tool | Install |
|------|---------|
| Python 3.10+ | https://www.python.org/downloads/ |
| ffmpeg | `sudo apt install ffmpeg` (Linux) / `brew install ffmpeg` (Mac) / https://ffmpeg.org/download.html (Windows) |

Verify:
```bash
python3 --version   # 3.10+
ffmpeg -version     # any recent build
```

## Step 3 — Get your API keys

The pipeline needs three AI services. Bring your own keys — nothing is hardcoded.

→ Full walkthrough: **[docs/10-api-keys.md](docs/10-api-keys.md)** — where to get each key, how to store them in `.env`, and the safety rules.

Quick version:
```bash
cp .env.example .env   # then fill in your three keys
set -a; source .env; set +a
```
Never commit `.env` — it's git-ignored.

## Step 4 — Research your topic

Follow [docs/01-research.md](docs/01-research.md):
1. Pick a niche and find 3–5 recent outlier videos on small channels (1K–20K subs, ≤25 uploads).
2. Extract the curiosity trigger; move one step sideways for your own angle.
3. Get a human to approve the topic before continuing.

## Step 5 — Write and approve the script

Follow [docs/02-script.md](docs/02-script.md):
1. Draft the script in the Hook → Setup → Conflict → Journey → Climax → Resolution → Lesson → CTA arc.
2. Fact-check every claim.
3. Get human approval — no voiceover until the script is locked.

## Step 6 — Generate the voiceover

Follow [docs/03-voiceover.md](docs/03-voiceover.md):
1. Pick one voice and lock it for the channel (never change it randomly).
2. Generate `narration.mp3` from the approved script.
3. Get human approval of the VO.

## Step 7 — Generate one clip per sentence

Follow [docs/04-visuals.md](docs/04-visuals.md):
1. Split the VO into sentences/beats.
2. Generate one true-motion clip per beat, matching the beat's duration.
3. Build your timing manifest (see [examples/beats_timing.example.json](examples/beats_timing.example.json)):
   ```json
   [{"beat": 1, "sentence": "...", "start": 0.0, "end": 4.2,
     "duration": 4.2, "clip": "beat-01.mp4"}]
   ```

## Step 8 — Assemble the video

```bash
python3 scripts/assemble.py \
  --manifest beats.json \
  --clips ./clips \
  --vo narration.mp3 \
  --out final.mp4
```

The script handles crossfade math, clip looping, loudness normalization, and renders a 1080p master. Verify: final duration ≈ VO duration, and spot-check 3+ sync points. Details in [docs/05-assembly.md](docs/05-assembly.md).

## Step 9 — Thumbnail + metadata

1. Generate the thumbnail per [docs/06-thumbnails.md](docs/06-thumbnails.md) — centered highlighted text, curiosity gap, never restating the title. Get human approval.
2. Prepare title, 2-line keyword description, chapters, and SRT per [docs/07-metadata.md](docs/07-metadata.md).

## Step 10 — Publish

Follow [docs/08-publishing.md](docs/08-publishing.md):
- Upload only on explicit human approval.
- Max 1–2 uploads per channel per day.
- Pin your engagement comment within 1 hour (manual step in YouTube Studio).

## Step 11 — Measure

At 72 hours, judge by [docs/09-analytics.md](docs/09-analytics.md): <50 views = move on, 50–200 = watch, >200 = make the sequel next.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ffmpeg: command not found` | Re-do Step 2; restart your terminal after install |
| Video shorter than VO | You're trimming clips to beat duration without fade overlap — read [docs/05-assembly.md](docs/05-assembly.md) |
| ffmpeg hangs on a clip | Don't use `-stream_loop` on MP4 inputs; the script loops at filter level |
| TTS sounds wrong | You changed the voice — re-lock one voice per channel and regenerate |
