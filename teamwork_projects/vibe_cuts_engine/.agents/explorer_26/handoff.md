# Handoff: IO Export Fixes & Test Strategy

## 1. Observation
1. **Mock Abuse & Test Circumvention**: In `tests/core/test_io.py` (e.g., lines 42-45, 57-61, 84-88, 102-107), filesystem methods like `os.replace`, `os.remove`, and `os.path.exists` are heavily mocked using `unittest.mock.patch`.
2. **In-place Overwrite Bug (Windows)**: In `src/core/io.py` lines 36 and 76, `os.replace(tmp_path, path)` is called. For `extract_audio` (line 76), this happens *before* `audio.close()` and `video.close()` are called (lines 85-91). On Windows, replacing a file while it (or its underlying temp handles) is locked by a process throws a `PermissionError`.
3. **Audio File Leak & UUID Usage**: `src/core/io.py` uses `f"{root}.{uuid.uuid4().hex}.tmp{ext}"` in the target directory for staging (lines 33, 73). In the `except BaseException:` block (lines 37-43), only this specific `tmp_path` is explicitly removed. MoviePy automatically creates intermediate audio files (e.g., `*TEMP_MPY_wvf_snd.mp3`) during `write_videofile`, which are left orphaned in the target directory upon interruption (e.g., `KeyboardInterrupt`).

## 2. Logic Chain
1. **Integrity Violation**: By mocking `os.replace` and `os.remove`, the unit tests bypass native filesystem operations. This circumvents genuine end-to-end testing of file locks, which is why the Windows `PermissionError` on open file replacements was never caught natively.
2. **Windows Locking Fix**: MoviePy components hold file locks until explicitly closed or garaged-collected. Calling `os.replace()` while the `AudioFileClip` or writer handles are still active guarantees failure on Windows. For `extract_audio`, moving the clips' `.close()` calls to happen *before* the filesystem move will release the locks. For `export_video`, we must use safer file transfers (like `shutil.move` with potential retries) if the caller maintains the clip open, but more securely, we should isolate the writing process.
3. **Atomic Scope & Leak Prevention**: Instead of manually formatting string UUIDs and trying to guess all MoviePy intermediate file names to clean them up, the entire write operation should be scoped within a `tempfile.TemporaryDirectory(dir=os.path.dirname(path))`.
   - MoviePy will write the video and its intermediate audio file entirely inside this isolated directory.
   - If a `KeyboardInterrupt` or `BaseException` occurs, the context manager automatically purges the entire directory, instantly fixing the MoviePy audio leak.
   - If successful, the final file is moved from the temp directory to the final destination, and the temp directory is cleaned up safely.

## 3. Caveats
- `shutil.move` will overwrite by default, but it relies on `os.rename` under the hood if on the same filesystem. On Windows, if the destination `path` exists and is currently locked by a separate program (e.g., an open media player), it will still raise a `PermissionError`. The tests should ensure the destination file isn't open.
- For `export_video`, the prompt specifies "The caller is responsible for managing the clip's lifecycle and closing it." This implies we cannot call `clip.close()` inside `export_video`. We must rely entirely on `TemporaryDirectory` to mask lock issues for the temp artifacts and rely on `shutil.move` for the atomic placement.

## 4. Conclusion
1. **Source Changes**: 
   - Refactor `export_video` and `extract_audio` to use `with tempfile.TemporaryDirectory(...) as tmpdir:`. 
   - Save the `clip` or `audio` to a `tmp_path` *inside* the `tmpdir`. 
   - For `extract_audio`, call `.close()` on both audio and video *before* calling `shutil.move(tmp_path, final_path)`.
   - Remove the unsafe `uuid` string formatting and the manual `except BaseException: os.remove` logic.
2. **Test Changes**: 
   - Remove `@patch` decorators for `os.replace`, `os.remove`, `os.path.exists`, and `uuid` in `tests/core/test_io.py`. 
   - Implement genuine filesystem tests using a local `tempfile.TemporaryDirectory` for the test fixture, letting the engine write real dummy clips (like `ColorClip` and `AudioClip`) and verifying real file creation and cleanup.
   - Add a test `test_integration_export_video_cleanup_on_interrupt` where `write_videofile` is mocked to raise `KeyboardInterrupt` *after* creating a dummy intermediate `TEMP_MPY_wvf_snd.mp3` file, and assert that neither the intermediate file nor the target `.mp4` remain on disk.

## 5. Verification Method
- **Implementation Validation**: Run `pytest tests/core/test_io.py` on a Windows host. The tests should execute actual filesystem commands without mocks.
- **Leak Validation**: Inject a `time.sleep` into `write_videofile` and trigger a `KeyboardInterrupt`. Inspect the destination directory to assert that NO `*TEMP_MPY*.mp3` or `*.tmp` directories/files exist.
- **Windows Lock Validation**: In the test suite, attempt to use the extracted audio file immediately after extraction to ensure `PermissionError` is not raised.
