# Handoff Report: I/O Core Improvements & Integrity Fixes

## 1. Observation
1. **Audio Leak**: In `src/core/io.py`, `export_video` and `extract_audio` do not specify the `temp_audiofile` parameter for MoviePy operations. When an exception occurs (e.g. `KeyboardInterrupt`), MoviePy's default intermediate audio files (e.g., `*TEMP_MPY_wvf_snd.mp3`) are left orphaned because the `finally` cleanup block only removes the video `tmp_path`.
2. **Temp Naming**: The application manually constructs temporary file paths using `f"{root}.{uuid.uuid4().hex}.tmp{ext}"`, which is predictable and non-atomic, risking race conditions.
3. **Windows Overwrite Bug**: As demonstrated by `tests/core/test_io_adversarial_extra.py::test_export_overwrite_open_file`, attempting to `export_video` to the same path as the loaded clip raises a `PermissionError` on Windows because `os.replace` cannot overwrite a file actively held open by the clip's reader.
4. **Integrity Violation**: The unit tests in `tests/core/test_io.py` (e.g., `test_export_video`, `test_extract_audio_success`) heavily mock `uuid.uuid4`, `os.replace`, `os.remove`, and `os.path.exists`. These hardcoded mock checks circumvent actual file system testing, violating test integrity and locking the tests to the flawed implementation details.

## 2. Logic Chain
1. **Fixing the Leak**: By explicitly generating a secure temporary path for the audio track and passing it as `temp_audiofile=...` to `clip.write_videofile()`, we gain control over the intermediate file. We can then add it to the `finally` block to ensure guaranteed cleanup under all exception scenarios.
2. **Fixing Temp Naming**: We can replace the `uuid` manual path generation with `fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=ext)`. To avoid cross-platform regressions (MoviePy/FFmpeg failing to open the file on Windows due to locks), we must immediately release the handle via `os.close(fd)` before passing `tmp_path` to MoviePy.
3. **Fixing Windows Overwrite**: When exporting, if the destination `path` matches `clip.filename`, we are performing an in-place overwrite. Since MoviePy completes its read operations before `write_videofile` finishes, we can safely invoke `clip.close()` immediately before calling `os.replace()`. This explicitly releases the Windows file lock, allowing the overwrite to succeed. A small retry loop can safeguard against lingering FFMPEG subprocess locks.
4. **Fixing Integrity Violations**: To test the genuine logic, the unit tests must be refactored to use `tempfile.TemporaryDirectory`. By removing the `patch` decorators for `os` and `uuid`, the tests will perform actual filesystem I/O, ensuring that temp files are created securely, replaced atomically, and cleaned up correctly without test circumvention.

## 3. Caveats
- Closing the clip early for in-place overwrites assumes the caller doesn't plan to reuse the `clip` instance for further processing. This is a standard and acceptable limitation, as the underlying file contents are being fundamentally replaced anyway.
- The `os.close(fd)` workaround for `mkstemp` is strictly necessary on Windows; otherwise `write_videofile` will throw a `PermissionError` internally when it tries to open the locked temp file.

## 4. Conclusion
The comprehensive strategy is:
1. Update `export_video` and `extract_audio` to use `tempfile.mkstemp` followed by `os.close()` for atomic and secure temporary file creation.
2. Define explicit `temp_audiofile` paths and incorporate them into the `finally` block for deterministic cleanup.
3. Check for in-place overwrites (`os.path.abspath(getattr(clip, 'filename', '')) == os.path.abspath(path)`) and proactively call `clip.close()` before `os.replace()` to resolve Windows locking bugs.
4. Rewrite `tests/core/test_io.py` to eliminate `os` and `uuid` mocks, validating genuine file system behavior.

## 5. Verification Method
- Run `pytest tests/core/test_io.py` to confirm the un-mocked tests pass with genuine file operations.
- Run `pytest tests/core/test_io_adversarial_extra.py` on Windows (or an equivalent CI runner) to verify the in-place overwrite `PermissionError` is resolved.
- Manually or programmatically inject an exception (e.g., `KeyboardInterrupt`) during `write_videofile` and inspect the target directory with `ls`/`dir` to assert no intermediate `.mp3` or `.tmp` files are left behind.
