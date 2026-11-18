# Investigation Report: Fix Strategy for Engine Core & I/O Bugs

## 1. Observation
- **Missing Dependency Handling**: In `src/core/io.py:8-9`, the fallback `ImportError` block for `moviepy` uses `pass`. This leaves `VideoFileClip` undefined if `moviepy` is unavailable.
- **Resource Cleanup Leak**: In `src/core/io.py:57-60`, `extract_audio`'s `finally` block calls `audio.close()` followed immediately by `video.close()`. 
- **Unsafe Defaults & Concurrency**: In `src/core/io.py:48`, the default output path for `extract_audio` is `os.path.splitext(video_path)[0] + "_audio.mp3"`.
- **Non-atomic Writes**: In `src/core/io.py:27` (`export_video`) and `54` (`extract_audio`), the `write_videofile` and `write_audiofile` methods write directly to the final `path` and `output_audio_path`.
- **Test Resource Leak**: In `tests/core/test_io.py:106`, `test_integration_io` loads a video using `clip = load_video(input_video_path)` but never calls `clip.close()`.

## 2. Logic Chain
- The `pass` on `ImportError` hides the missing dependency, causing a `NameError` when `VideoFileClip` is referenced later. Raising an explicit `ImportError` instead fails fast with a clear message.
- If `audio.close()` raises an exception, the sequential `finally` block aborts before reaching `video.close()`. Nesting these in separate `try...finally` blocks guarantees both resources are released.
- The static default output path in `extract_audio` forces writes to the same directory as the input video (problematic in read-only environments) and risks race conditions if multiple processes extract the same file concurrently. Defaulting to a unique file in the system temp directory solves both.
- Writing directly to final destinations can leave corrupted or partial files if the process crashes or is killed mid-write. Writing to a `.tmp` file and atomically renaming it using `os.replace()` upon completion ensures the final file is always complete.
- `test_integration_io` keeps the video file handle open by not closing `clip`, which can cause test flakiness or file deletion errors on Windows. Explicitly calling `clip.close()` fixes this leak.

## 3. Caveats
- Atomic renames via `os.replace()` require the source and destination to be on the same filesystem. When writing the temporary file for the atomic swap, it should be created in the same directory as the target file.
- The `moviepy` import block modification will break test suites if they rely on `mock_video_file_clip` patching without `moviepy` being installed in the test environment (unless patched using a string path that resolves to the module). Tests that patch `src.core.io.VideoFileClip` must use `create=True` if `VideoFileClip` is not defined at all.

## 4. Conclusion
The following fix strategy should be implemented:
1. **Dependency Handling**: Replace `pass` in `src/core/io.py:9` with `raise ImportError("moviepy is required. Please install it.")`.
2. **Resource Cleanup**: Refactor `extract_audio`'s `finally` block to use a nested `try...finally` so `video.close()` executes even if `audio.close()` throws.
3. **Safe Defaults**: Modify `extract_audio` to use `tempfile.mktemp` or similar to generate a unique default path in `tempfile.gettempdir()` when `output_path` is `None`.
4. **Atomic Writes**: In both `export_video` and `extract_audio`, construct a temporary filename (e.g., `f"{path}.tmp"`), pass it to the write methods, and upon success call `os.replace(tmp_path, final_path)`.
5. **Test Leaks**: Add `clip.close()` in `test_integration_io` at the end of the test.

## 5. Verification Method
- Run `pytest tests/core/test_io.py` to ensure all tests pass and no file locks are left behind.
- Manually run a script that imports `io.py` without `moviepy` installed to verify the explicit `ImportError`.
- Interrupt `extract_audio` or `export_video` mid-write and verify that no partial target file is left in the destination directory (only the `.tmp` file).
