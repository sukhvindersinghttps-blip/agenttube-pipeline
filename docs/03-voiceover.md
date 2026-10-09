# 03 — Voiceover

Each channel has a **locked voice identity** — never changed randomly. Only delivery style may borrow from a reference; the voice itself stays fixed.

## Voice locks (examples)

| Channel | Voice | Speed | Notes |
|---------|-------|-------|-------|
| History / documentary | `avocado_v2:magnus` | 92 (~150 wpm) | Calm documentary feel |
| War stories | `avocado_v2:casper` | 92 | Same benchmark tone |
| Psychology | `avocado_v2:Twenty` | 120 | Reference delivery style only |

## Rules

- Get script + voiceover **approved before** generating visuals (visuals are the expensive step; remakes redo only what changed).
- If any TTS request fails: **report immediately and auto-retry** the exact same request (same voice, same settings) — never silently switch voices or engines.
- Audio is loudness-normalized at assembly (`loudnorm`).
- VO approval is a hard gate — no visuals until the VO is approved.
