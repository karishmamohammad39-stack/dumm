# Handoff Report: Fix Strategy for M1 Engine Core & I/O Iteration 8 Failures

## Observation
1. **Test Assertion Bug**: `test_export_video_no_extension` (line 188 of `tests/core/test_io.py`) incorrectly expects `mock_replace` to be called with `"out_path"` instead of the corrected `"out_path.mp4"`.
2. **Validation Sequence Bug**: In `src/core/io.py` (lines 29-40), the input/output path collision check occurs before the path extension (`.mp4`) is appended. This allows `"file"` (no extension) to bypass the check against `"file.mp4"`.
3. **MoviePy Auxiliary File Leak**: `src/core/io.py` creates a temp file via `uuid4().hex` and cleans it up via a `try...finally` block. However, MoviePy's `write_videofile` creates side-car files (like `*TEMP_MPY_wvf_snd.mp3`) that are missed by this explicit cleanup.
4. **Missing Extension Propagation**: When an extensionless path is provided to `export_video` or `extract_audio`, the file gets an `.mp4` or `.mp3` extension for the temporary file, but the final renamed file currently may not keep the intended extension correctly based on the failing tests context (although the source code currently reassigns `path`, the test expects otherwise).

## Logic Chain
1. To address the **Validation Sequence Bug**, we must swap the order in `export_video` and `extract_audio`. The `os.path.abspath(clip.filename) == os.path.abspath(path)` check must be performed *after* the `ext` defaulting logic modifies `path` (and similarly for `output_audio_path`).
2. To address the **MoviePy Auxiliary File Leak**, the `try...finally` single-file remove must be replaced with `with tempfile.TemporaryDirectory() as temp_dir:`. The primary output file should be written into `temp_dir` (e.g., `os.path.join(temp_dir, f"temp{ext}")`). Upon exiting the context manager, python will recursively delete all files in the directory, including MoviePy's auxiliary files.
3. This change breaks the existing unit tests (`test_export_video_keyboard_interrupt`, `test_export_video_standard_exception`, `test_export_video_cleanup_oserror`, etc.) which mock `os.remove` and `uuid.uuid4`. 
4. To fix the unit tests, we will update the mocks to `@patch('src.core.io.tempfile.TemporaryDirectory')`, set `mock_tempdir.return_value.__enter__.return_value = '/fake_temp'`, and adjust assertions to check `os.path.join('/fake_temp', f'temp{ext}')` instead of `uuid4`. We can remove all tests verifying `os.remove` or `os.path.exists` on cleanup, since `TemporaryDirectory` handles it natively.
5. To fix the **Test Assertion Bug** and verify **Extension Propagation**, `test_export_video_no_extension` must assert `mock_replace.assert_called_once_with(expected_tmp, "out_path.mp4")` instead of `"out_path"`.

## Caveats
- `tempfile.TemporaryDirectory` cleans up on garbage collection or context exit. If `os.replace` throws an exception, the directory still gets cleaned up. This makes the `test_export_video_cleanup_oserror` test obsolete, as there is no longer a manual `os.remove` inside our code to trigger an `OSError` on.
- Path joining in tests should use `os.path.join` to be OS-agnostic instead of string formatting, ensuring it passes on Windows where the tests currently run.

## Conclusion
The fixes require structural changes to `src/core/io.py` and significant rewrites to the test file `tests/core/test_io.py`. 
- **`src/core/io.py` changes**: Move path extension appending above the same-path validation. Replace `uuid.uuid4()` temp path generation and `try...finally` cleanup with `with tempfile.TemporaryDirectory() as temp_dir:`. 
- **`tests/core/test_io.py` changes**: Remove `uuid.uuid4` and `os.remove` patches. Patch `src.core.io.tempfile.TemporaryDirectory` to yield a controlled path (e.g. `'/fake_temp'`). Update write/replace assertions to expect `os.path.join('/fake_temp', 'temp.mp4')`. Update `test_export_video_no_extension` to assert the target path is `"out_path.mp4"`. Drop explicit cleanup tests.

## Verification Method
- Execute the test suite using `pytest tests/core/test_io.py`.
- Run the full end-to-end integration tests using `pytest e2e_tests/` to ensure no auxiliary files are leaked during realistic workflow scenarios and that extensionless paths are correctly written as `.mp4`/`.mp3` files.
