# Analysis of Iteration 8 Failures

## 1. Test Assertion Bug (`tests/core/test_io.py`)
**Observation**: 
In `tests/core/test_io.py`, line 192, `test_export_video_no_extension` calls `export_video(mock_clip, "out_path")`. 
Line 196 asserts: `mock_replace.assert_called_once_with("out_path.1234.tmp.mp4", "out_path")`.
**Analysis**: Because `export_video` now correctly appends `.mp4` to extensionless paths, `os.replace` is actually called with `"out_path.mp4"`. The test assertion is outdated and expects the incorrect old behavior.
**Fix**: Update the assertion on line 196 to: `mock_replace.assert_called_once_with("out_path.1234.tmp.mp4", "out_path.mp4")`.

## 2. Validation Sequence Bug (`src/core/io.py`)
**Observation**: 
In `export_video`, the same-path validation happens at lines 29-31:
```python
    if hasattr(clip, 'filename') and clip.filename:
        if os.path.abspath(clip.filename) == os.path.abspath(path):
            raise ValueError("Output path cannot be the same as input path.")
```
This is executed BEFORE lines 36-39 where `path` is updated with an `.mp4` extension if it lacks one.
**Analysis**: If the input clip is `"file.mp4"` and the user provides `"file"` as the output path, the check compares `"file.mp4"` with `"file"` and passes. Then `path` becomes `"file.mp4"`, which overwrites the input file, leading to corruption.
**Fix**: Move the validation block (lines 29-31) to line 40, immediately AFTER `path` is updated with the proper extension.

## 3. MoviePy Auxiliary File Leak (`src/core/io.py`)
**Observation**:
Both `export_video` and `extract_audio` use a manual temporary file with a `.tmp` extension, generated using `uuid.uuid4().hex`. A `try...finally` block removes only this primary temp file. MoviePy's `write_videofile` creates auxiliary files (e.g., `*TEMP_MPY_wvf_snd.mp3`).
**Analysis**: On early termination (e.g., `KeyboardInterrupt`), the auxiliary files remain on disk because the `finally` block only deletes the main temp file.
**Fix**: Replace the manual `tmp_path` creation and `try...finally` cleanup with Python's `tempfile.TemporaryDirectory()`. 
```python
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = os.path.join(tmpdir, f"tmp{ext}")
    clip.write_videofile(tmp_path, codec="libx264", audio_codec="aac")
    os.replace(tmp_path, path)
```
This ensures the directory and all its contents (including MoviePy's hidden files) are purged automatically.

## 4. Missing Extension Propagation (`src/core/io.py`)
**Observation**:
The current `export_video` and `extract_audio` do have the `path = f"{root}{ext}"` logic. However, the logic must be correctly integrated with the `TemporaryDirectory` approach and the tests. The reviewer's feedback notes that generating `.mp4` for the temp file but replacing to an extensionless path breaks downstream AI tools.
**Analysis**: By ensuring `path` (or `output_audio_path`) is updated *before* passing it to `os.replace(tmp_path, path)`, we propagate the extension. The validation move (Bug 2) and the test fix (Bug 1) complete this fix.

## Impact on Tests
Because we are switching to `tempfile.TemporaryDirectory()`, unit tests in `tests/core/test_io.py` that mock `uuid.uuid4` and `os.remove` will fail or become irrelevant.
**Fix Strategy for Tests**:
- Remove `mock_uuid4` and `mock_remove`.
- Mock `tempfile.TemporaryDirectory`. When testing the exception cases, ensure we simulate an exception inside the `with` block and assert that `TemporaryDirectory` was entered, which inherently guarantees cleanup.
- Alternatively, don't mock `tempfile.TemporaryDirectory` but use a real temporary directory and verify that files are removed (integration style), or mock `clip.write_videofile` to just raise an error and ensure the exception is caught, relying on Python's built-in `TemporaryDirectory` logic.
- Update expected paths in assertions from `"out_path.1234.tmp.mp4"` to `os.path.join("mocked_tmpdir", "tmp.mp4")` (or similar depending on the mock strategy).
