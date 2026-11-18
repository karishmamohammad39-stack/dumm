# Scope: M1: Engine Core & I/O

## Architecture
- **Engine Core & I/O**: Handles media ingestion, decoding, audio extraction, and basic rendering pipeline/export.
- Will likely utilize libraries like `moviepy` or `ffmpeg-python`.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1 | Ingest video files, extract audio, basic export | none | IN_PROGRESS |

## Interface Contracts
### `src/core/io.py`
- `load_video(path: str) -> VideoClip/Any`
- `export_video(clip: Any, path: str) -> None`
- `extract_audio(video_path: str) -> str`
