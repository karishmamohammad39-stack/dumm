# Handoff Report: Fix Strategy for `io.py` and `test_io.py`

## 1. Observation
1. **Cryptic Dependency Error:** In `src/core/io.py:2-9`, the fallback for importing `VideoFileClip` catches `ImportError` and executes `pass`. This leaves `VideoFileClip` completely undefined if `moviepy` is absent, causing `NameError` at runtime and `AttributeError` when tests attempt to patch it.
2. **Resource Leak in `extract_audio`:** In `src/core/io.py:56-60`, the `finally` block sequentially calls `audio.close()` and `video.close()`. If `audio.close()` raises an exception, the execution halts, and `video.close()` is never called, leaking the video file handle.
3. **Concurrency Risk & Unsafe Defaults:** In `src/core/io.py:48`, the default `output_audio_path` is hardcoded to `os.path.splitext(video_path)[0] + "_audio.mp3"`. This risks race conditions if multiple threads/processes extract audio from the same video. It also fails if the source directory is read-only.
4. **Non-atomic Writes:** In both `export_video` (`io.py:27`) and `extract_audio` (`io.py:54`), the functions write directly to the final destination path. If the process is interrupted, corrupted or partial files will remain.
5. **Test Resource Leak:** In `tests/core/test_io.py:82-126`, `test_integration_io` loads a video via `clip = load_video(...)` but never calls `clip.close()`. This leaves open file handles, which can cause the test's `tempfile.TemporaryDirectory` cleanup to fail on Windows.

## 2. Logic Chain
1. If `moviepy` is missing, `VideoFileClip` must be explicitly defined as `None` (or a mock) so that `@patch('src.core.io.VideoFileClip')` works in tests without `create=True`, and runtime code can gracefully raise an `ImportError` or `RuntimeError` rather than a cryptic `NameError`.
2. In `finally` blocks containing multiple resource cleanup calls, each `close()` must be wrapped in its own `try...except Exception: pass` block to ensure that a failure in closing one resource does not preclude the closing of subsequent resources.
3. To resolve concurrency and read-only directory issues, the default `output_path` for `extract_audio` should use `tempfile.mktemp()` or `tempfile.NamedTemporaryFile` placed in the OS temporary directory, rather than beside the source video.
4. To ensure atomic writes, `export_video` and `extract_audio` must write to a randomly generated temporary file first. Upon successful completion of the `.write_videofile` or `.write_audiofile` call, `os.replace(temp_path, final_path)` should be used to atomically move the complete file to the final destination.
5. `test_integration_io` must explicitly close the `clip` object (and ideally use a `try...finally` block) to ensure file handles are released before the temporary directory attempts cleanup.

## 3. Caveats
- Atomic writes via `os.replace` require the temporary file and the final file to be on the same filesystem. If `tempfile.gettempdir()` is on a different drive than the output path, `os.replace` will fail with an `OSError` (Cross-device link). To be completely robust, the temporary file for the atomic write should be created in the same directory as the final destination path.
- The `VideoFileClip = None` approach means that `load_video` and `extract_audio` must add an explicit check `if VideoFileClip is None: raise ImportError(...)` at the beginning of the functions.

## 4. Conclusion
Implement the following fixes:
- **`src/core/io.py` Imports:** Set `VideoFileClip = None` if both `moviepy` import attempts fail. Add a check in functions to raise `ImportError("moviepy is required")` if `VideoFileClip is None`.
- **`src/core/io.py` Atomic Writes:** For `export_video` and `extract_audio`, write the media to a temporary file created in the `os.path.dirname(final_path)`. Once writing is complete, use `os.replace()` to move it to `final_path`.
- **`src/core/io.py` Safe Defaults:** Change `extract_audio` to use a temporary path in `tempfile.gettempdir()` with a unique suffix (e.g., using `uuid` or `tempfile.mktemp`) if `output_path` is `None`.
- **`src/core/io.py` Robust Cleanup:** Wrap `audio.close()` and `video.close()` in separate `try...except Exception` blocks inside the `finally` clause.
- **`tests/core/test_io.py` Cleanup:** Add `clip.close()` to the end of `test_integration_io` (using `try...finally`).

## 5. Verification Method
1. Run `pytest tests/core/test_io.py` after applying the changes. Tests should pass.
2. In a Python shell, verify `import src.core.io` doesn't crash when `moviepy` is uninstalled, and that `mock.patch('src.core.io.VideoFileClip')` succeeds.
3. Simulate an exception in `audio.close()` during `extract_audio` and verify `video.close()` is still executed (can be done via mock in tests).
4. Verify that `test_integration_io` cleans up its temporary directory successfully on Windows (no `PermissionError` from open file handles).
