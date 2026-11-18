# Handoff Report: Iteration 4 IO Bug Fixes

## 1. Observation
- **Observation 1**: `src/core/io.py` lines 32 and 68 use static tmp paths: `tmp_path = path + ".tmp"` and `tmp_path = output_audio_path + ".tmp"`.
- **Observation 2**: `src/core/io.py` lines 38 and 74 attempt `os.remove(tmp_path)` within an `except Exception:` block without catching subsequent filesystem errors.
- **Observation 3**: `tests/core/test_io.py` lines 91 and 96 explicitly and statically import from `moviepy.editor`.
- **Observation 4**: `tests/core/test_io.py` line 123 assigns `res = extract_audio(input_video_path)`. The function stores this in `tempfile.gettempdir()`, and the test finishes without calling `os.remove(res)`.

## 2. Logic Chain
1. Static `.tmp` paths mean concurrent tasks exporting to the same destination path will write to identical temporary files, corrupting data. A unique UUID suffix prevents this race condition.
2. In the event of an error, `os.remove(tmp_path)` can fail with `PermissionError` (an `OSError`) on Windows if the file handle is not cleanly released. If unhandled, this error overrides the original task exception. Suppressing `OSError` here prevents this masking.
3. MoviePy 2.0 removed the `moviepy.editor` module. Hardcoding this import causes an `ImportError` on new versions and crashes the test runner. Implementing a fallback `try/except` block mirroring the main source avoids this.
4. Using `tempfile.gettempdir()` places files outside the context manager's controlled `tmpdir`. Failing to explicitly remove `res` leads to leaked MP3 files accumulating in the global temp directory after every run.

## 3. Caveats
- By randomizing the `.tmp` path generation, unit tests asserting on mock calls (specifically `test_export_video`, `test_extract_audio_success`, and `test_extract_audio_with_output_path`) will break since they check for exact file paths (e.g. `"out_path.mp4.tmp"`). The implementation must refactor the assertions to inspect the dynamic mock arguments (using `startswith` or `unittest.mock.ANY`).

## 4. Conclusion
To fully resolve the remaining gate failures:
1. Inject `.{uuid.uuid4().hex}.tmp` into the temporary paths in `export_video` and `extract_audio`. Update test mock assertions to validate dynamic strings.
2. Wrap `os.remove(tmp_path)` in `try: ... except OSError: pass` in both `src/core/io.py` error handlers.
3. Update `test_integration_io` to try importing from `moviepy.editor`, falling back to `moviepy`, or skipping the test entirely if neither succeeds.
4. Append `os.remove(res)` in `test_integration_io` immediately after the assertions to clean up the leaked audio file.

## 5. Verification Method
- **Race Condition & Unit Tests**: Run `pytest tests/core/test_io.py`. Ensure mocks correctly handle dynamic string checking and pass.
- **Dependency Mismatch**: Run `pytest tests/core/test_io.py` in an environment with MoviePy 2.0+ installed. The integration test should pass or skip.
- **Artifact Leak**: Check the system's temporary directory (`tempfile.gettempdir()`) before and after running the integration test. No new `audio_*.mp3` files should be leaked.
