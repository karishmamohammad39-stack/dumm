# Project: Vibe Cuts Engine

## Architecture
- **Engine Core & I/O**: Handles media ingestion, decoding, and basic rendering pipeline.
- **Layer Compositing System**: Manages stacking of multiple media layers, custom keyframing, masking shapes, and dynamic blend modes.
- **AI Automation System**: Handles audio-synced speed curves, audio extraction, and auto-generated subtitles.
- **Integration & API**: The overarching architecture (backend library/API) demonstrating the combination of AI workflows and motion graphics.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Engine Core & I/O | Ingest video files, extract audio, basic export | none | IN_PROGRESS |
| 2 | M2: Compositing System | Stack layers, apply masks, blend modes, keyframing | M1 | PLANNED |
| 3 | M3: AI Automation System | Generate subtitles, apply dynamic speed curves | M1 | PLANNED |
| 4 | M4: Integration API | Unified API to apply edits and composite, meeting all criteria | M2, M3 | PLANNED |
| 5 | M5: E2E Final Pass | Pass 100% E2E tests (Tiers 1-4) | M4 | IN_PROGRESS (E2E Track) |
| 6 | M6: Adversarial Testing | Adversarial coverage hardening (Tier 5) | M5 | PLANNED |

## Interface Contracts
### Engine Core ↔ AI System
- `extract_audio(video_path: str) -> str`
- `apply_speed_curve(video_segment, curve_data) -> processed_segment`

### Engine Core ↔ Compositing System
- `composite_layers(base_layer, overlay_layer, blend_mode, mask)`
- `apply_keyframe_transform(layer, keyframes)`

## Code Layout
- `src/core/`: Ingestion, I/O, core pipeline.
- `src/compositing/`: Layer stacks, blend modes, masking.
- `src/ai/`: Auto-captions, speed curves.
- `src/api/`: Unified interface.
- `tests/`: Unit tests.
- `e2e_tests/`: End-to-end tests.
