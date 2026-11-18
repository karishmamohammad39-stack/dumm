# Handoff Report: Fix Strategy for M1 Iteration 1 Failures

## Observation
- In `src/core/io.py` at line 25: `def extract_audio(video_path: str, output_audio_path: str) -> str:`.
- In `SCOPE.md` at line 16 and `PROJECT.md` at line 21: `extract_audio(video_path: str) -> str`.
- In `src/core/io.py` at lines 33-42, `extract_audio` uses `VideoFileClip` and `.audio`, then calls `.close()` sequentially without a `try/finally` block. 
- In `src/core/io.py`, `export_video` and `extract_audio` call `clip.write_videofile()` and `audio.write_audiofile()` directly on the provided paths without checking if the parent directory exists.
- In `src/core/io.py` at line 15, `load_video(path: str)` uses `if not os.path.exists(path):` to validate the path, which evaluates to true for directories.
- In `tests/core/test_io.py` at lines 111-112, the integration test `test_integration_io` wraps the entire test execution in a `try...except Exception as e:` block and calls `pytest.skip(f"Integration test skipped due to error: {e}")`.

## Logic Chain
1. **Resource Leaks**: The lack of `try/finally` in `extract_audio` causes file handles to remain open if `audio.write_audiofile()` raises an exception. Wrapping the resource usage in `try...finally` guarantees cleanup.
2. **Missing Directories**: Writing to paths where parent directories don't exist will raise a `FileNotFoundError`. Calling `os.makedirs(os.path.dirname(path), exist_ok=True)` before writing ensures the export succeeds.
3. **Directory Ingestion**: `load_video` currently accepts directories, which causes unexpected errors when `moviepy` tries to read them. Changing the check to `os.path.isfile(path)` and raising `IsADirectoryError` when a directory is passed enforces the correct behavior.
4. **Interface Mismatch**: `extract_audio` requires `output_audio_path`, violating the contract in `SCOPE.md`. Removing this parameter, automatically deriving the output path (e.g., by changing the extension to `.mp3`), and returning it will conform to the contract. Tests in `test_io.py` and `test_io_adversarial.py` must be updated to match the new signature.
5. **Integrity Violation**: Catching all exceptions and calling `pytest.skip()` in `test_integration_io` masks real test failures. Removing this block allows standard test assertion failures and runtime exceptions to surface correctly, providing accurate CI feedback.

## Caveats
- Fixing `export_video` and `extract_audio` to create parent directories will alter the behavior of existing adversarial tests in `test_io_adversarial.py` that currently expect these functions to fail when provided a nonexistent directory. Those tests must be refactored to either assert successful creation of nested directories or use paths that cause actual OS permission errors.
- The default extension for the automatically generated audio path is assumed to be `.mp3`.

## Conclusion
- **Fix 1**: Refactor `extract_audio` to use `try/finally` blocks to guarantee that `audio.close()` and `video.close()` are called regardless of exceptions.
- **Fix 2**: Add `dirname = os.path.dirname(path); if dirname: os.makedirs(dirname, exist_ok=True)` in both `export_video` and `extract_audio` prior to the write operations.
- **Fix 3**: Update `load_video` to use `os.path.isfile(path)` to verify it is a file, raising `IsADirectoryError` (or `ValueError`) if it is a directory.
- **Fix 4**: Change `extract_audio` signature to `def extract_audio(video_path: str) -> str:`, generate `output_audio_path = os.path.splitext(video_path)[0] + '.mp3'`, and update all corresponding unit and integration tests.
- **Fix 5**: Remove the `try...except` block in `tests/core/test_io.py`'s `test_integration_io` function so that test failures are not skipped.

## Verification Method
- Execute `pytest tests/core/` and ensure all tests pass (including updated adversarial tests).
- Manually inspect `src/core/io.py` to confirm the presence of `try/finally`, `os.makedirs`, `os.path.isfile`, and the corrected 1-argument signature.
- Manually inspect `tests/core/test_io.py` to verify the `try/except -> pytest.skip` construct has been removed.
