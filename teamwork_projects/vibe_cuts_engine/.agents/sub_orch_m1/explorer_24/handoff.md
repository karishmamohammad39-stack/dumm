# Handoff Report: Iteration 7 Investigation (M1 Engine Core & I/O)

## Observation
1. **BaseException Artifact Leaks (`src/core/io.py`)**: 
   - Both `export_video` and `extract_audio` use an `except BaseException:` block for cleanup. While it catches `KeyboardInterrupt`, it relies on catching and re-raising. If an exception escapes or execution exits early (e.g. an implicit return or `sys.exit`), the `except` block may be bypassed, causing the temporary artifact to leak. Python idiom strongly favors `try...finally` for guaranteed cleanup.
2. **Missing Error Path Unit Tests (`tests/core/test_io.py`)**:
   - The test suite only mocks `KeyboardInterrupt` to verify cleanup (`test_export_video_keyboard_interrupt`, `test_extract_audio_base_exception`).
   - There are no unit tests covering standard `Exception`s during video/audio writing.
   - Crucially, there are no tests verifying that an `OSError` raised during `os.remove(tmp_path)` is correctly swallowed (masked) and the original exception is preserved and re-raised. This branch (`except OSError: pass`) currently lacks coverage.
3. **Format Inference Crashes (`src/core/io.py`)**:
   - The current temporary file logic uses `root, ext = os.path.splitext(path)` and then `f"{root}.{uuid}.tmp{ext}"`. 
   - If the user provides a path with *no extension* (e.g., `export_video(clip, "output")`), `ext` evaluates to `""`. The resulting temporary path becomes `output.<uuid>.tmp`. MoviePy relies on file extensions to determine the container format and muxer. Without a valid extension (e.g., seeing `.tmp`), MoviePy fails to infer the format and crashes.

## Logic Chain
1. By switching from `except BaseException:` to a `try...finally` block, we guarantee that the cleanup logic (`os.remove(tmp_path)`) runs regardless of how the block exits (be it a standard Exception, KeyboardInterrupt, or successful execution). If `os.replace` succeeds, `tmp_path` no longer exists, and `finally` gracefully skips removal. This eliminates the artifact leak entirely.
2. By adding explicit unit tests for both standard `Exception`s and `OSError` masking (when `os.remove` fails), we satisfy the rigorous error path coverage required by the auditing gate.
3. By explicitly checking if `ext` is empty and providing a fallback (`.mp4` for video, `.mp3` for audio), the temporary file always has a valid media extension (e.g. `output.<uuid>.tmp.mp4`). MoviePy successfully infers the container, writes the file, and then `os.replace` atomically renames it back to the exact (extension-less) path requested by the user.

## Caveats
- Assuming `codec="libx264"` and `audio_codec="aac"` are sufficient for any extension provided by the user. 
- Assuming the test suite has no hidden state dependencies when `os.remove` is mocked with a side effect.

## Conclusion
The Iteration 7 gate failed because the previous worker did not fully resolve the root causes. The fixes require modifying `src/core/io.py` to use `try...finally` blocks and fallback extensions, and updating `tests/core/test_io.py` to explicitly mock and assert error paths (OSError during cleanup and standard Exceptions) as well as extension-less file exports. 

## Verification Method
1. **Implementation (`src/core/io.py`)**:
   - Update `export_video` and `extract_audio` to calculate a `tmp_ext`: `tmp_ext = ext if ext else ".mp4"` (and `.mp3` for audio).
   - Change `except BaseException:` block to `finally:`.
2. **Tests (`tests/core/test_io.py`)**:
   - Add `test_export_video_standard_exception` and `test_extract_audio_standard_exception`.
   - Add `test_export_video_cleanup_oserror` to assert that `OSError` in `os.remove` doesn't mask the original exception (mock `os.remove` with `side_effect=OSError`).
   - Add `test_export_video_no_extension` to ensure `write_videofile` is called with a `.mp4` temporary file when given an extension-less path.
3. **Run tests**:
   - Execute `pytest tests/core/test_io.py -v --cov=src.core.io --cov-report=term-missing`. Verify 100% coverage on error branches and no test failures.
