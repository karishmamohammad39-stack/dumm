# Handoff Report: Fix Strategy for Core I/O Bugs

## 1. Observation
- **Bug 1 (Undefined Fallback & Cryptic Error)**: In `src/core/io.py:2-9`, the fallback logic catches `ImportError` but uses `pass`, leaving `VideoFileClip` undefined if `moviepy` is missing. This causes `AttributeError` when tests patch it, and cryptic `NameError` at runtime instead of a clear dependency error.
- **Bug 2 (File Handle Leak)**: In `src/core/io.py:56-60`, the `finally` block calls `audio.close()` followed by `video.close()`. If `audio.close()` raises an exception, it prevents `video.close()` from executing.
- **Bug 3 (Concurrency Risk & Unsafe Defaults)**: In `src/core/io.py:47-48`, the default `output_path` is statically defined in the same directory as the video (`..._audio.mp3`). This causes race conditions on concurrent extractions and fails in read-only directories.
- **Bug 4 (Non-atomic Writes)**: Both `export_video` and `extract_audio` write directly to their final destinations. A crash during write leaves a corrupt file at the target path.
- **Bug 5 (Test Resource Leak)**: In `tests/core/test_io.py:105-112`, `clip = load_video(input_video_path)` is executed in `test_integration_io`, but `clip.close()` is never called, leaving a dangling handle.

## 2. Logic Chain
- **Bug 1**: To prevent `AttributeError` during mocking and provide clear runtime errors, `VideoFileClip` must be explicitly set to `None` if imports fail. The consuming functions (`load_video`, `extract_audio`) must explicitly check if it is `None` and raise an `ImportError("moviepy is required")`.
- **Bug 2**: To ensure both resources are closed, nest them: a `try...finally` for `audio.close()` inside the main `finally` that guarantees `video.close()`.
- **Bug 3**: Using a combination of `tempfile.gettempdir()` and `uuid.uuid4().hex` ensures the default output path is both writable (handling read-only environments) and completely unique (handling concurrency).
- **Bug 4**: Writing data to a `.tmp` suffix file first and then utilizing `os.replace(tmp_path, final_path)` guarantees that the final file only appears once writing is fully complete, preventing corrupt files.
- **Bug 5**: In `test_integration_io`, wrap the returned `clip` usage in a `try...finally` block that invokes `clip.close()`, or explicitly call it at the end.

## 3. Caveats
- Using a `.tmp` file and `os.replace` means there needs to be enough disk space to hold the temporary file alongside the target destination during the write process (if they are on different filesystems, `os.replace` might fail, though `shutil.move` is safer).
- Generating default paths in the system temp directory implies they might be cleaned up by the OS, which is standard for temporary extraction, but callers expecting the file to persist indefinitely should explicitly provide `output_path`.

## 4. Conclusion
The implementation should apply the following changes:
1. **Module Fallback**:
   ```python
   try:
       from moviepy.editor import VideoFileClip
   except ImportError:
       try:
           from moviepy import VideoFileClip
       except ImportError:
           VideoFileClip = None
   ```
   In `load_video` and `extract_audio`: `if VideoFileClip is None: raise ImportError(...)`
2. **Atomic Writes**:
   In `export_video` and `extract_audio`, write to `path + ".tmp"` first, then use `os.replace(tmp_path, final_path)` (or `shutil.move`).
3. **Safe Defaults & Concurrency**:
   In `extract_audio`, change the fallback path generation:
   ```python
   import tempfile, uuid
   output_audio_path = os.path.join(tempfile.gettempdir(), f"audio_{uuid.uuid4().hex}.mp3")
   ```
4. **Safe Resource Cleanup**:
   In `extract_audio`:
   ```python
   finally:
       try:
           if audio is not None: audio.close()
       finally:
           if video is not None: video.close()
   ```
5. **Test Fixes**:
   Add `clip.close()` to the end of `test_integration_io` in `tests/core/test_io.py`.

## 5. Verification Method
- **Bug 1**: Run `pytest` without `moviepy` installed to verify that `AttributeError` is not raised during test collection, and that `ImportError` is correctly raised at runtime.
- **Bug 2 & 5**: Run tests with a file handle leak detector (e.g. `pytest -W error::ResourceWarning`) to ensure all `VideoFileClip` instances are properly closed.
- **Bug 3**: Verify `extract_audio` without `output_path` runs successfully on a read-only source directory and outputs to the temp dir.
- **Bug 4**: Terminate the process during a write artificially (mocking `write_videofile` to raise an exception) and verify the final target file is not created, but the `.tmp` file is cleaned up or left behind.
