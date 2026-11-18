# Handoff Report: Iteration 8 Fix Strategy

## 1. Observation
- **Test Assertion (`tests/core/test_io.py:192-196`)**: `test_export_video_no_extension` calls `export_video(mock_clip, "out_path")` and asserts `mock_replace` is called with destination `"out_path"`, which contradicts the required behavior of defaulting to `.mp4`.
- **Validation Sequence (`src/core/io.py:29-39`)**: The check preventing input and output paths from being identical executes before `path` defaults to `.mp4`. Calling `export_video(clip, "file")` bypasses the check but eventually replaces `"file.mp4"`.
- **Temp File Leaks (`src/core/io.py:41-51, 88-98`)**: Manual `uuid` based temp files are used. `try...finally` blocks only `os.remove(tmp_path)`. MoviePy creates hidden audio temp files (`*TEMP_MPY_wvf_snd.mp3`) which are leaked on exceptions (like `KeyboardInterrupt`).
- **Extension Propagation**: While `path = f"{root}{ext}"` is present in the current iteration of the code, its effect is nullified by the test bug and misplaced validation sequence.

## 2. Logic Chain
1. The test assertion expects `"out_path"`, but the correct behavior is to append the extension. We must update the test to expect `"out_path.mp4"`.
2. To prevent overwriting the input file when an extensionless output is provided, the same-path validation must run *after* the output path has its extension appended.
3. MoviePy generates auxiliary files that our code is unaware of. Manually removing `tmp_path` is insufficient. Using a `tempfile.TemporaryDirectory` context manager offloads cleanup to the OS/Python, guaranteeing all files in the directory are wiped on block exit, solving the leak.
4. Implementing `TemporaryDirectory` requires updating the tests: removing `mock_uuid4` and `mock_remove`, and updating `mock_replace` assertions to match paths generated within the temporary directory.

## 3. Caveats
- Moving to `tempfile.TemporaryDirectory` requires overhauling multiple unit tests in `tests/core/test_io.py` because they explicitly mock `uuid.uuid4`, `os.remove`, and `os.path.exists`.
- Care must be taken to ensure `os.replace(tmp_path, path)` still works across devices if `tempfile.gettempdir()` is on a different filesystem than `path` (though Python 3.3+ `os.replace` generally handles this, or falls back, wait—actually `os.replace` on Windows may fail across drives; however, the original code used `os.replace` and it was accepted. We should stick to `os.replace` or `shutil.move`).

## 4. Conclusion
The fix requires four synchronized changes:
1. **`src/core/io.py`**: Refactor `export_video` and `extract_audio` to use `with tempfile.TemporaryDirectory() as tmpdir:`. Place the temporary files inside `tmpdir`.
2. **`src/core/io.py`**: In `export_video`, move the `clip.filename == path` validation block to *after* the `path = f"{root}{ext}"` extension normalization.
3. **`tests/core/test_io.py`**: Update `test_export_video_no_extension` to assert `mock_replace` receives `"out_path.mp4"`.
4. **`tests/core/test_io.py`**: Refactor the mocked unit tests (`test_export_video`, `test_extract_audio_success`, exception tests, etc.) to mock `tempfile.TemporaryDirectory` (or avoid mocking it and use real temp dirs) instead of mocking `uuid` and `os.remove`.

## 5. Verification Method
1. Run `pytest tests/core/test_io.py`. All unit tests must pass.
2. Specifically run the integration test `test_integration_io` to ensure actual MoviePy behavior works with `TemporaryDirectory`.
3. Manually trace `export_video(clip, "my_video")` (where `clip.filename` is `"my_video.mp4"`) and verify it raises a `ValueError`.
