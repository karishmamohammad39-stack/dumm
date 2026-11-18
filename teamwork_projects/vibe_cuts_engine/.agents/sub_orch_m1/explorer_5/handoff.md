# Handoff Report: Fix Strategy for M1 Iteration 2 Issues

## 1. Observation
- **Issue 1:** In `src/core/io.py`, `extract_audio` (lines 33-42) lacks a `try/finally` block to guarantee `video.close()` and `audio.close()` are called if `write_audiofile` fails. Similarly, `export_video` (lines 19-23) does not call `clip.close()` inside a `finally` block.
- **Issue 2:** In `src/core/io.py`, both `export_video` (line 23) and `extract_audio` (line 39) write files without first ensuring the parent directory exists using `os.makedirs(os.path.dirname(path), exist_ok=True)`.
- **Issue 3:** In `src/core/io.py`, `load_video` (line 15) and `extract_audio` (line 30) use `os.path.exists(path)` instead of `os.path.isfile(path)`.
- **Issue 4:** In `src/core/io.py`, `extract_audio` is defined as `def extract_audio(video_path: str, output_audio_path: str) -> str:` (line 25), violating the contract in `PROJECT.md` (`extract_audio(video_path: str) -> str`).
- **Issue 5:** In `tests/core/test_io.py`, the integration test `test_integration_io` wraps the entire test logic in a `try/except` block (lines 111-112) that calls `pytest.skip(f"Integration test skipped due to error: {e}")` instead of letting the exception fail the test.

## 2. Logic Chain
1. The missing `try/finally` blocks can lead to file descriptor leaks or locked files (especially on Windows) if an exception occurs during reading or writing. Wrapping the resource usage in `try...finally` ensures `.close()` is executed regardless of exceptions.
2. If the user provides a path in a directory that doesn't exist, file writing will throw an `OSError`. We must call `os.makedirs(os.path.dirname(output_path), exist_ok=True)` before `write_videofile` and `write_audiofile`.
3. A path could exist but be a directory. Using `os.path.isfile` ensures we are actually targeting a file, preventing generic IO errors when we try to read a directory as a video.
4. The `extract_audio` signature must be aligned with `PROJECT.md` so that the AI/Engine interface works. The function should generate its own output path (e.g., `os.path.splitext(video_path)[0] + ".mp3"`) and take only one argument.
5. Integration tests must ensure correctness. Swallowing exceptions with `pytest.skip()` gives a false sense of security (100% pass rate when it's actually failing). The `try/except` block needs to be removed.

## 3. Caveats
- The auto-generated path for `extract_audio` assumes placing the `.mp3` alongside the original file is acceptable.
- `export_video` taking ownership of closing the clip might conflict with callers that want to reuse the `clip` object. Assuming the issue text specifically calls out closing in `export_video`, we add it, but this assumes the clip is a one-off per export.

## 4. Conclusion
**Proposed Fix Strategy**:
1. **`src/core/io.py` updates**:
   - Change `os.path.exists` to `os.path.isfile` in `load_video` and `extract_audio`.
   - Update `extract_audio` signature to `def extract_audio(video_path: str) -> str:`.
   - In `extract_audio`, generate the output path: `output_path = os.path.splitext(video_path)[0] + ".mp3"`.
   - Add `os.makedirs(os.path.dirname(output_path), exist_ok=True)` before writes.
   - Implement `try/finally` for both `extract_audio` and `export_video` to call `.close()`.
2. **`tests/core/test_io.py` updates**:
   - Update mocks in unit tests from `mock_exists` (`os.path.exists`) to `mock_isfile` (`os.path.isfile`).
   - Remove the `output_audio_path` argument from `extract_audio` calls in unit and integration tests.
   - Remove the `try...except Exception as e: pytest.skip(...)` wrapper in `test_integration_io`.

## 5. Verification Method
- **Code Inspection**: Review `src/core/io.py` and `tests/core/test_io.py` to ensure the changes are applied.
- **Unit Tests**: Run `pytest tests/core/test_io.py` to ensure mocked tests pass with the new signature and `isfile`.
- **Integration Tests**: Run `pytest tests/core/test_io.py -m integration` to confirm the integration test runs without being skipped and properly tests the new implementation.
