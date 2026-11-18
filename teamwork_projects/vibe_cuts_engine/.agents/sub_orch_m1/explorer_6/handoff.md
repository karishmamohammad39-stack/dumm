# Handoff Report: M1 Iteration 2 Issues Analysis

## Observation
I investigated the 5 reported issues in `src/core/io.py`, `tests/core/test_io.py`, and `tests/core/test_io_adversarial.py`.
1. **Missing try/finally:** In `src/core/io.py:33-42`, `extract_audio` opens `VideoFileClip` and retrieves `audio` but relies on sequential `.close()` calls at the end, meaning exceptions during `.write_audiofile()` will cause resource leaks.
2. **Missing parent directory creation:** In `src/core/io.py`, both `export_video` and `extract_audio` write files without calling `os.makedirs` on the parent directory.
3. **`load_video` validates poorly:** In `src/core/io.py:15`, `load_video` uses `os.path.exists(path)`, which incorrectly permits directory paths.
4. **Interface mismatch:** In `src/core/io.py:25`, `extract_audio` is defined as `def extract_audio(video_path: str, output_audio_path: str) -> str:`, conflicting with `PROJECT.md` which requires `extract_audio(video_path: str) -> str`.
5. **Integration test cheated:** In `tests/core/test_io.py:111-112`, `test_integration_io` wraps its core logic in `except Exception as e: pytest.skip(...)`, silently masking failures.

## Logic Chain
- **Issue 1:** To prevent resource leaks, we need nested `try...finally` blocks in `extract_audio` to guarantee `.close()` is called on both `video` and `audio` objects regardless of whether `write_audiofile` succeeds.
- **Issue 2:** To ensure file writes succeed, `export_video` and `extract_audio` must use `os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)` before writing.
- **Issue 3:** To validate inputs strictly, `load_video` must use `os.path.isfile(path)` instead of `os.path.exists(path)`.
- **Issue 4:** To adhere to `PROJECT.md` contracts, `extract_audio` must be updated to accept only `video_path`. The output path can be safely derived by replacing the input file's extension with `.mp3` (e.g. using `os.path.splitext(video_path)[0] + ".mp3"`).
- **Issue 5:** The broad `except Exception` in `test_integration_io` must be removed so that true failures propagate and fail the test run.
- **Test Impacts:** The signature change for `extract_audio` requires updating tests in `test_io.py` and `test_io_adversarial.py` to pass only one argument.

## Caveats
- Since the new `extract_audio` derives the output path from the input path, and the input path is validated to exist as a file, the output directory is practically guaranteed to exist. Thus, the adversarial test `test_extract_audio_invalid_dir` in `tests/core/test_io_adversarial.py` (which intentionally passes a bad output directory) will no longer apply and should be removed or completely refactored.
- Deriving the output audio path assumes that appending or replacing the extension with `.mp3` is acceptable.

## Conclusion
We must patch `src/core/io.py` to fix the implementation flaws, specifically:
- Update `extract_audio` signature and derive `output_audio_path`.
- Wrap `.write_audiofile()` in `try...finally` structures.
- Add `os.makedirs` before any file write operations.
- Update `load_video` to use `os.path.isfile()`.

We must also patch the test suite:
- Remove the `try...except...pytest.skip` block in `test_integration_io`.
- Update `test_extract_audio_success` and `test_extract_audio_no_audio` in `test_io.py` to use a single argument.
- Remove or refactor `test_extract_audio_invalid_dir` in `test_io_adversarial.py`.

## Verification Method
- **Implementation:** Inspect `src/core/io.py` to ensure `try/finally` blocks and `os.makedirs` calls are present.
- **Tests:** Run `pytest tests/core/test_io.py` and `pytest tests/core/test_io_adversarial.py`. The tests should execute without skipping, and all integration tests should pass successfully.
