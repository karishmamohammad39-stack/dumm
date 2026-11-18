# Handoff Report: Review of io.py and test_io.py

## Observation
Worker 6 correctly implemented fixes for two out of the three issues, but missed a few error path unit tests.

1. **BaseException Artifact Leak in io.py**: 
   - `export_video` (lines 37-43) and `extract_audio` (lines 77-83) now correctly catch `BaseException`, check `if os.path.exists(tmp_path)`, and run `os.remove(tmp_path)` before re-raising the exception. 
   - This cleanly handles `KeyboardInterrupt` and other exceptions.

2. **Format Inference Crash**:
   - `tmp_path` is correctly formatted in both functions using `root, ext = os.path.splitext(path)` and `f"{root}.{uuid.uuid4().hex}.tmp{ext}"` (lines 32-33 and 72-73). This preserves the original extension (e.g., `.mp4`), allowing MoviePy's format inference to work properly.

3. **Missing Error Path Unit Tests**:
   - Tests were added for `KeyboardInterrupt` handling in both functions, and for "no audio" in `extract_audio`.
   - However, several error paths in `src/core/io.py` remain entirely untested in `tests/core/test_io.py`:
     - `ImportError` raised when `VideoFileClip is None` (lines 18-19 in `load_video`, lines 50-51 in `extract_audio`).
     - `FileNotFoundError` raised when `os.path.isfile(video_path)` is false in `extract_audio` (lines 52-53).
     - The `except OSError: pass` fallback during `tmp_path` cleanup in both `export_video` (lines 41-42) and `extract_audio` (lines 81-82).

## Logic Chain
- The artifact leak and format inference crash bugs were addressed correctly because the implementation handles `BaseException` to delete the temp file, and formats the `.tmp` extension safely before the actual file extension.
- The unit test bug was only partially resolved. A comprehensive fix for "Missing Error Path Unit Tests" requires 100% coverage on explicit `raise` statements and `except` blocks.
- The lack of tests for `ImportError` (when `moviepy` is unavailable), `FileNotFoundError` in `extract_audio`, and `OSError` during cleanup leaves these explicit error paths uncovered.

## Caveats
- I was unable to run `pytest --cov` directly due to terminal permission timeouts, but static analysis of the source vs. test files clearly shows these branches are not mocked or tested in `tests/core/test_io.py`.

## Conclusion
The implementation of the fixes in `io.py` is correct and robust, but there are remaining issues with the test suite (Bug 2). **Implementation changes are needed in `tests/core/test_io.py` to add the missing tests.** 

### Proposed Fix Strategy for Next Worker:
Add the following unit tests to `tests/core/test_io.py`:
1. `test_load_video_import_error`: Patch `src.core.io.VideoFileClip` with `None` and assert `ImportError` is raised.
2. `test_extract_audio_import_error`: Patch `src.core.io.VideoFileClip` with `None` and assert `ImportError` is raised.
3. `test_extract_audio_not_found`: Patch `src.core.io.os.path.isfile` to return `False` and assert `FileNotFoundError` is raised in `extract_audio`.
4. `test_export_video_cleanup_oserror`: Duplicate the `test_export_video_keyboard_interrupt` test, but configure `mock_remove.side_effect = OSError()` to verify the `pass` block executes safely and the `KeyboardInterrupt` is still raised.
5. `test_extract_audio_cleanup_oserror`: Duplicate `test_extract_audio_base_exception`, configure `mock_remove.side_effect = OSError()`, and verify correct propagation.

## Verification Method
- **Implementation**: The next worker should implement the proposed tests in `tests/core/test_io.py`.
- **Validation**: Run `pytest tests/core/test_io.py --cov=src.core.io --cov-report=term-missing`. The coverage for `src/core/io.py` must reach 100%, with no missing lines shown in the report.
