# Review Report: src/core/io.py

## Review Summary

**Verdict**: REQUEST_CHANGES

## Findings

### [Major] `export_video` forcibly closes the `clip` argument
- **What**: The `export_video` function calls `clip.close()` in a `finally` block.
- **Where**: `src/core/io.py`, lines 26-29.
- **Why**: `export_video` does not create the `clip` object; it receives it as an argument. Closing a resource that a function did not open is a known anti-pattern. This prevents the caller from reusing the clip (e.g., exporting to multiple resolutions, or compositing further after an intermediate export). The original file handle leak that the worker noticed was likely caused by the caller (e.g., `test_integration_io`) failing to close the clip it opened via `load_video`. Modifying a library function to fix a caller's leak breaks the API's composability.
- **Suggestion**: Remove `clip.close()` from `export_video`. Instead, update the caller in the test (`test_integration_io` in `tests/core/test_io.py`) to explicitly call `clip.close()` after it finishes using the clip loaded via `load_video`. Additionally, ensure `dummy_video.close()` is called in the test to prevent `tempfile.TemporaryDirectory` cleanup errors on Windows.

### [Minor] `extract_audio` writes to the input directory
- **What**: `extract_audio` dynamically generates the output path by placing the `.mp3` file next to the input video (`os.path.splitext(video_path)[0] + ".mp3"`).
- **Where**: `src/core/io.py`, line 47.
- **Why**: While this strictly fulfills the interface contract (`extract_audio(video_path: str) -> str`), it assumes the directory containing the input video is writable. If a user loads a video from a read-only directory, audio extraction will fail.
- **Suggestion**: Consider adding an optional `output_audio_path: str = None` parameter. If not provided, it can fall back to the current behavior. (This is a nice-to-have for robustness).

## Verified Claims
- Replaced `os.path.exists` with `os.path.isfile` in `load_video`. → **Verified** (Static analysis confirms this).
- `extract_audio` plugged leaks by properly closing `video` and `audio` in a `finally` block. → **Verified** (The `try/finally` block correctly handles both closures, even if an exception is raised).
- Missing directory creation handled. → **Verified** (Both `export_video` and `extract_audio` use `if dir_name: os.makedirs(...)` properly).
- Tests updated to match new signature and behavior. → **Verified** (Mocks and integration tests align with the changes).

## Coverage Gaps
- **Test Execution**: Unable to run `pytest` due to system permission timeouts. Relied on static code analysis to verify the logic.

## Unverified Items
- Actual test execution output. However, logical tracing strongly indicates the current code creates lifecycle limitations for `clip` objects.
