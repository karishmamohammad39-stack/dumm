# Handoff Report: M1 Engine Core & I/O (Iteration 7 Investigation)

## Observation
1. **BaseException Artifact Leak**: In `src/core/io.py`, the `export_video` and `extract_audio` functions catch `BaseException` and explicitly remove `tmp_path`. However, MoviePy's `write_videofile` implicitly creates temporary audio files alongside the video file (typically appending `TEMP_MPY_wvf_snd.mp3`). If cancelled via `Ctrl+C`, the current `except BaseException` block deletes `tmp_path` but **leaks the hidden MoviePy audio temp files** on the disk.
2. **Missing Error Path Unit Tests**: In `tests/core/test_io.py`, `test_export_video_keyboard_interrupt` and `test_extract_audio_base_exception` successfully test standard `KeyboardInterrupt`. However, there are no tests for **exception masking**. Specifically, there is no test verifying that if `os.remove(tmp_path)` raises an `OSError` during cleanup, the original exception is re-raised rather than masked.
3. **Format Inference Crash**: The current Iteration 7 fix in `src/core/io.py` uses `f"{root}.{uuid.uuid4().hex}.tmp{ext}"` for the temp file. If the `path` argument lacks an extension entirely (e.g., `"output_video"`), `ext` evaluates to `""`. The resulting temporary path becomes `output_video.1234.tmp`, which forces MoviePy to infer the format from `.tmp`, leading to a crash.

## Logic Chain
1. The artifact leak persists because the current cleanup logic is hardcoded to only remove `tmp_path`. Since MoviePy spawns auxiliary files in the same directory, a manual `os.remove(tmp_path)` is insufficient to guarantee total cleanup.
2. The missing unit tests mean the CI gate cannot verify whether exceptions in the cleanup block mask the primary `KeyboardInterrupt`. Python will replace the exception context if a cleanup exception isn't explicitly caught and ignored.
3. The format inference fix is incomplete because it relies on the user providing an extension. While valid paths (like `.mp4`) work, extensionless paths silently degenerate into `.tmp` extensions, re-triggering the exact bug Iteration 5 tried to fix. 
4. **Unified Solution**: Wrapping the export process in a `tempfile.TemporaryDirectory(dir=os.path.dirname(path) or '.')` natively resolves all three issues:
   - The directory automatically cleans up *all* contents (including MoviePy's hidden audio files) on `BaseException`.
   - The temporary file can use the exact `os.path.basename(path)` without any `.tmp` injection, flawlessly matching MoviePy's format inference.
   - It simplifies the logic, removing the need for manual `os.remove()` and its associated masking risks.

## Caveats
- `tempfile.TemporaryDirectory` context managers naturally handle cleanup even on `BaseException` (like `KeyboardInterrupt`). However, on Windows, if FFmpeg doesn't release the file handle in time, directory cleanup might raise `PermissionError`. The implementation should use `ignore_cleanup_errors=True` (if Python >= 3.10) or catch/pass `OSError` during cleanup.

## Conclusion
The Iteration 7 code remains broken because manual cleanup (`os.remove(tmp_path)`) leaks MoviePy's auxiliary files and lacks exception masking unit tests, while the `tmp` injection still crashes on extensionless paths. 

**Fix Strategy for Implementer:**
1. **Refactor `io.py`:** Remove manual `uuid` appending and `except BaseException` blocks. Instead, use a `with tempfile.TemporaryDirectory(dir=os.path.dirname(path) or '.') as temp_dir:` block. Write the file to `os.path.join(temp_dir, os.path.basename(path))`, and upon success, use `os.replace` to move it to the final destination.
2. **Expand `test_io.py`:** Add unit tests simulating an `OSError` during the cleanup phase (e.g. `mock_cleanup.side_effect = OSError()`) while a `KeyboardInterrupt` is raised by MoviePy, asserting that the `KeyboardInterrupt` is properly propagated.

## Verification Method
1. `pytest tests/core/test_io.py` to ensure all existing and new exception masking tests pass.
2. Manually trigger a mock `KeyboardInterrupt` during `export_video` and assert that no `*TEMP_MPY*` files remain in the target directory.
3. Call `export_video(clip, "no_extension_path")` and assert it does not crash on `.tmp` inference.
