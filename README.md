# AgentTube Pipeline

The end-to-end process behind AgentTube's AI-produced YouTube videos — from outlier research to published video. This repo documents the exact workflow, quality gates, and tooling we use in production.

> **Honesty note:** This documents our real process, including what is automated and where humans stay in control. No inflated claims — what works is stated plainly, what is experimental is labeled as such.

## The Pipeline

```
Topic → Research → Script → Voiceover → Visuals → Assembly → Thumbnail → Metadata → Review → Publish
```

| # | Stage | Gate |
|---|-------|------|
| 1 | [Outlier Research](docs/01-research.md) | Topic approved by human |
| 2 | [Scriptwriting](docs/02-script.md) | Script approved by human |
| 3 | [Voiceover](docs/03-voiceover.md) | VO approved by human |
| 4 | [Visual Generation](docs/04-visuals.md) | Sentence-level sync check |
| 5 | [Assembly](docs/05-assembly.md) | Duration & sync verified |
| 6 | [Thumbnails](docs/06-thumbnails.md) | Thumbnail approved by human |
| 7 | [Metadata & SEO](docs/07-metadata.md) | Package review |
| 8 | [Publishing](docs/08-publishing.md) | Explicit publish approval |
| 9 | [Analytics](docs/09-analytics.md) | 72-hour judgment |

**Hard rule:** Nothing moves past a gate without explicit human approval. "OK" and "Sure" don't count — publishing requires unambiguous words like "upload kar do" or "go ahead".

## Repo layout

- `docs/` — the process, stage by stage
- `scripts/` — reusable tooling (sanitized, no secrets)
- `examples/` — sample manifests and configs

## Requirements

- `ffmpeg` (assembly, loudness normalization)
- Python 3.10+
- AI services: TTS provider, text LLM, image/video generation (bring your own keys — nothing is hardcoded here)

## License

MIT — use it, fork it, improve it.
