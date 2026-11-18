# Handoff Report: Iteration 6 M1 Engine Core & I/O

## 1. Observation
- `src/core/io.py:36` and `src/core/io.py:75` use `except Exception:`.
- `src/core/io.py:32` and `src/core/io.py:71` generate temporary filenames using simple string concatenation: `f"{path}.{uuid.uuid4().hex}.tmp"`.
- `tests/core/test_io.py` (lines 38-39, 59-60, 78-79) contains hardcoded assertions checking for filenames ending exactly in `.tmp`.
- `tests/core/test_io.py` lacks any tests verifying the exception-handling cleanup logic in `export_video` or `extract_audio`.

## 2. Logic Chain
1. **Artifact Leak (`KeyboardInterrupt`)**: `except Exception:` in Python does not catch `BaseException` subclasses like `KeyboardInterrupt` or `SystemExit`. If execution is aborted during video or audio writing, the temporary file is skipped in cleanup and left orphaned. Switching to `except BaseException:` ensures cleanup runs on any abort.
2. **Format Inference Crash**: MoviePy relies on the final file extension to determine how to encode the media. Appending `.tmp` creates filenames like `output.mp4.1234.tmp`. The `.tmp` extension crashes MoviePy's inference. Using `os.path.splitext(path)` to separate the base from the original extension and appending the extension at the very end (`{base}.{uuid}.tmp{ext}`) resolves this.
3. **Missing & Broken Unit Tests**: 
   - Fixing the temp filename logic will cause the existing `test_io.py` assertions (which expect `.tmp`) to fail. They must be updated to expect the `.tmp{ext}` format.
   - To prevent regression of the artifact leak issue, we must add error-path unit tests. By mocking `write_videofile`/`write_audiofile` to raise an exception, we can explicitly assert that `os.remove(tmp_path)` is called and the exception is propagated.

## 3. Caveats
- Using `os.path.splitext` on filenames without extensions will return an empty string for the extension. This is perfectly fine, as MoviePy would fail anyway without an extension.
- The `except BaseException:` block currently re-raises the exception (`raise`). This is correct and should be maintained so callers are aware of failures.

## 4. Conclusion
To resolve the Iteration 5 failures, the Implementer must:
1. **Fix Artifact Leaks**: Change `except Exception:` to `except BaseException:` in `src/core/io.py` (lines 36 and 75).
2. **Fix Inference Crash**: In `src/core/io.py` (lines 32 and 71), replace the `tmp_path` assignment with:
   ```python
   base, ext = os.path.splitext(path)
   tmp_path = f"{base}.{uuid.uuid4().hex}.tmp{ext}"
   ```
   *(Apply similar logic for `output_audio_path`)*.
3. **Fix and Expand Tests**: In `tests/core/test_io.py`:
   - Update existing temp file path assertions to match the new format.
   - Add new tests (`test_export_video_error_cleanup` and `test_extract_audio_error_cleanup`) that patch `os.remove`, configure `write_videofile`/`write_audiofile` to raise an error, and assert that `os.remove` is called with the expected `tmp_path`.

## 5. Verification Method
1. Inspect `src/core/io.py` to confirm the presence of `os.path.splitext` and `except BaseException:`.
2. Inspect `tests/core/test_io.py` to confirm the updated assertions and new error cleanup tests.
3. Run `pytest tests/core/test_io.py -v` to verify that all unit tests pass.
4. Run `pytest tests/core/test_io.py --cov=src.core.io` to ensure the cleanup blocks are fully covered.
