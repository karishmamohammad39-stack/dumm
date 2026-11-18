# Handoff Report: M1 Engine Core & I/O Strategy

**Summary**: The codebase is currently empty. The M1 implementation requires initializing the `src/core` module, setting up dependencies (`moviepy`), and implementing the required I/O interface contracts.

## 1. Observation
- `PROJECT.md` defines the M1 milestone: "Ingest video files, extract audio, basic export." Code layout specifies `src/core/` for Ingestion, I/O, core pipeline, and `tests/` for Unit tests.
- `SCOPE.md` specifies the interface contracts for `src/core/io.py`:
  - `load_video(path: str) -> VideoClip/Any`
  - `export_video(clip: Any, path: str) -> None`
  - `extract_audio(video_path: str, output_audio_path: str) -> str`
- `SCOPE.md` suggests utilizing `moviepy` or `ffmpeg-python`.
- `list_dir` on the project root (`C:\Users\ganap\OneDrive\Desktop\reel\teamwork_projects\vibe_cuts_engine`) confirms it is currently empty of source code, containing only metadata (`PROJECT.md`, `SCOPE.md`, `ORIGINAL_REQUEST.md`, `TEST_INFRA.md` and `.agents/`).

## 2. Logic Chain
- **Project Scaffold**: Since no code directories exist, the implementer must create `src/core/`, `tests/core/`, and a `requirements.txt` file.
- **Dependency Choice**: `moviepy` is highly suitable for this because it abstracts `VideoClip` objects nicely (which maps perfectly to `load_video(path) -> VideoClip`), supports basic exports via `write_videofile`, and supports audio extraction via `.audio.write_audiofile()`. It also aligns well with M2's compositing requirements later on.
- **Implementation Steps**:
  1. Add `moviepy` (and potentially `pytest` for testing) to `requirements.txt`.
  2. Implement `src/core/io.py` fulfilling the three functions from `SCOPE.md`.
  3. Create `tests/core/test_io.py`.
- **Testing Requirements**: To test I/O, a dummy video file will be needed. The test setup should ideally generate a brief synthetic video or include a tiny asset in a `tests/assets/` folder to avoid external test dependencies.

## 3. Caveats
- `moviepy` depends on `ffmpeg`. While `moviepy` usually handles fetching a local binary on first run, in CI/headless environments this might need explicit handling or installation.
- No test assets exist yet; the implementer must create synthetic test data (e.g., generating a quick color clip using `moviepy` itself) to reliably test the I/O module.

## 4. Conclusion
The implementation strategy for M1 is straightforward:
1. Initialize the directory structure (`src/core/`, `tests/core/`).
2. Set up `requirements.txt` with `moviepy` and `pytest`.
3. Implement `src/core/io.py` matching the exact signatures in `SCOPE.md`.
4. Create tests in `tests/core/test_io.py` that use synthetically generated video clips (to avoid uploading large binary files) to verify `load_video`, `extract_audio`, and `export_video`.

## 5. Verification Method
- Code Structure: `src/core/io.py` and `tests/core/test_io.py` must exist.
- Code Signatures: Verify `io.py` contains `load_video`, `export_video`, and `extract_audio` with the expected parameters.
- Tests: Run the project test suite using `pytest tests/core/test_io.py`. All tests should pass and demonstrate successful file writes and reads for both video and audio.
