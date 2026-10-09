# Using Your Own API Keys

The pipeline needs three AI services. You bring your own keys — here's exactly how to get and use each one safely.

## The three keys

| # | Key | Used for | Pipeline stage |
|---|-----|----------|----------------|
| 1 | `LLM_API_KEY` | Research + scriptwriting | Steps 4–5 |
| 2 | `TTS_API_KEY` | Voiceover generation | Step 6 |
| 3 | `MEDIA_API_KEY` | Thumbnails + motion clips | Steps 7, 9 |

## Step-by-step: get each key

### 1. LLM key (research + scripts)
1. Pick a provider: Anthropic (console.anthropic.com), OpenAI (platform.openai.com), or Google AI Studio (aistudio.google.com).
2. Create an account → go to **API keys** → **Create new key**.
3. Copy the key immediately (most providers show it only once).
4. Add billing if required — set a **spending limit** on day one.

### 2. TTS key (voiceover)
1. Pick a TTS provider (e.g. ElevenLabs, PlayHT, or your preferred engine).
2. Sign up → find **API keys** in settings/dashboard → generate a key.
3. Note which **voice ID** you want to lock per channel (see [docs/03-voiceover.md](docs/03-voiceover.md)) — the voice ID goes in your config, not the key.

### 3. Media key (thumbnails + clips)
1. Pick an image/video generation provider (e.g. Google Gemini image gen, fal.ai, Replicate, or similar).
2. Sign up → API section → create a key.
3. Check the provider's per-image/per-second pricing before batch runs.

## Step-by-step: use the keys safely

### 1. Copy the example file
```bash
cp .env.example .env
```

### 2. Fill in your keys
Open `.env` and paste each key:
```bash
LLM_API_KEY=sk-ant-your-real-key-here
TTS_API_KEY=your-tts-key-here
MEDIA_API_KEY=your-media-key-here
```

### 3. Load them in your shell
```bash
set -a; source .env; set +a
```
Or export them directly:
```bash
export LLM_API_KEY="sk-ant-..."
```

### 4. Verify they're set (without printing them)
```bash
[ -n "$LLM_API_KEY" ] && echo "LLM key: OK" || echo "LLM key: MISSING"
[ -n "$TTS_API_KEY" ] && echo "TTS key: OK" || echo "TTS key: MISSING"
[ -n "$MEDIA_API_KEY" ] && echo "MEDIA key: OK" || echo "MEDIA key: MISSING"
```

## Safety rules (non-negotiable)

1. **NEVER commit `.env` to git.** The repo's `.gitignore` already excludes it — verify with `git status` before every commit.
2. **NEVER paste keys into chat, issues, or screenshots.** If you need help debugging, redact them.
3. **One key per service, stored in one place** (your `.env`). Don't scatter copies.
4. **Set spending limits** on every provider from day one.
5. **If a key leaks** (pasted publicly, committed by accident): revoke it immediately in the provider's dashboard and generate a new one. Don't wait.

## Rotating a key

1. Generate a new key in the provider's dashboard.
2. Update your `.env`.
3. Revoke/delete the old key.
4. Re-run the verify commands above.
