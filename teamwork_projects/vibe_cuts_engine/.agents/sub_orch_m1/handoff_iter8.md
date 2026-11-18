# Handoff Report: Iteration 8 Failures

The Iteration 8 gate failed due to the following bugs identified by Reviewer 17 and Challenger 17:

1. **Test Assertion Bug (`tests/core/test_io.py`)**: `test_export_video_no_extension` incorrectly asserts that `mock_replace` receives `"out_path"` instead of `"out_path.mp4"`.
2. **Validation Sequence Bug (`src/core/io.py`)**: In `export_video`, the check preventing the input path from being the same as the output path (lines 29-31) happens BEFORE the extension is normalized/appended. Thus, `export_video(clip, "file")` bypasses the check but eventually overwrites `"file.mp4"`. The same-path check must be moved AFTER extension normalization.
3. **MoviePy Auxiliary File Leak (`src/core/io.py`)**: `write_videofile` implicitly creates a secondary audio extraction file (`*TEMP_MPY_wvf_snd.mp3`). A `KeyboardInterrupt` leaves this file orphaned on disk because our `try...finally` block only deletes the primary `tmp_path`. We should switch to using `tempfile.TemporaryDirectory` to isolate and automatically clean up all generated files (including MoviePy's hidden auxiliary files) on failure or exit.
4. **Missing Extension Propagation (`src/core/io.py`)**: If the user provides an extensionless path (e.g., `"output"`), we generate `.mp4` for the temp file but `os.replace` renames it back to `"output"`. This creates a valid media file missing an extension, breaking downstream AI tools. The fix is to modify the output `path` variable itself (e.g., `path = path + ".mp4"`) so the final file retains the extension.

The Forensic Auditor returned a CLEAN verdict for Iteration 8.

**Your Task**: Provide a cohesive fix strategy for these 4 bugs in `src/core/io.py` and `tests/core/test_io.py`.
