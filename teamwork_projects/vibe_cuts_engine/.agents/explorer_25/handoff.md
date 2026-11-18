# Handoff Report: M1 Iteration 8 Fix Strategy

## Observation
1. **Integrity Violation**: `e2e_tests/conftest.py` contains a `try...except ImportError` block that catches the missing `src.api.vibe_engine` module. If missing, it injects a `MockEngine` that returns hardcoded dummy strings (`"vid_" + str(hash(path))`). This bypasses all E2E tests, feigning completion.
2. **MoviePy Intermediate Audio Leak**: In `src/core/io.py`, `export_video` calls `clip.write_videofile` without specifying `temp_audiofile`. MoviePy automatically creates an intermediate audio file (e.g. `*TEMP_MPY_wvf_snd.mp3`). If a `KeyboardInterrupt` or other exception occurs, this file is leaked because it is neither tracked nor cleaned up.
3. **In-place Overwrite bug on Windows**: `os.replace(tmp_path, path)` in both `export_video` and `extract_audio` fails on Windows due to `PermissionError`. This occurs because MoviePy's underlying FFmpeg subprocess or Windows Antivirus briefly retains a lock on the temporary output file after writing completes. 
4. **Temporary File Naming**: `f"{root}.{uuid.uuid4().hex}.tmp{ext}"` is used for temporary files. This is non-atomic and insecure compared to `tempfile.NamedTemporaryFile`.

## Logic Chain
1. **Fixing the Integrity Violation**: The `MockEngine` test circumvention must be eliminated to ensure genuine functionality is tested. `src/api/vibe_engine.py` must be implemented with a real `VibeEngine` class that delegates to `src.core.io` functions (like `load_video`, `extract_audio`, `export_video`). The fallback logic in `e2e_tests/conftest.py` must be removed so that missing implementations genuinely fail the tests.
2. **Fixing the Temporary Naming & Audio Leak**: 
   - By creating secure files via `tempfile.NamedTemporaryFile(delete=False, dir=dir_name, suffix=ext)`, we rely on OS-level atomic file creation (`O_EXCL`), avoiding symlink/race vulnerabilities. 
   - We must explicitly generate a second temporary file for `temp_audiofile`, pass it to `write_videofile`, and ensure its deletion in a `finally` block.
3. **Fixing Windows Overwrite/Locking**: To handle delayed lock releases by FFmpeg/Windows on the output file, `os.replace` must be wrapped in a retry mechanism with exponential backoff. This absorbs the transient `PermissionError` and allows cross-platform atomic replacement to succeed.

## Caveats
- As an Explorer, I am only proposing the strategy; I have not implemented the code.
- `NamedTemporaryFile(delete=False)` means we MUST close the file descriptor immediately (e.g. via a `with` context manager) before passing the file path to MoviePy, otherwise Python itself will hold the lock and cause the same Windows sharing violations.

## Conclusion & Fix Strategy
The following actions must be taken by the Implementer:

**1. Address Integrity Violation (`e2e_tests/conftest.py` & `src/api/vibe_engine.py`)**
- Remove the `try...except ImportError` fallback and the `MockEngine` class from `e2e_tests/conftest.py`.
- Create `src/api/vibe_engine.py` and implement the real `VibeEngine` methods (`ingest_video`, `extract_audio`, `export`, etc.) calling into `src.core.io`.

**2. Address Audio Leaks & Windows Locking (`src/core/io.py`)**
Refactor `export_video` and `extract_audio`. For `export_video`:
```python
import time
import tempfile

def export_video(clip, path: str) -> None:
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    root, ext = os.path.splitext(path)
    
    # Secure temporary file generation, closed immediately to prevent Python locking
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext, dir=dir_name) as tmp_vid:
        tmp_path = tmp_vid.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=dir_name) as tmp_aud:
        tmp_audio_path = tmp_aud.name

    try:
        clip.write_videofile(tmp_path, codec="libx264", audio_codec="aac", temp_audiofile=tmp_audio_path)
        
        # Windows lock bypass via retry loop
        retries = 5
        for i in range(retries):
            try:
                os.replace(tmp_path, path)
                break
            except PermissionError:
                if i < retries - 1:
                    time.sleep(0.1 * (2 ** i))
                else:
                    raise
    except BaseException:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise
    finally:
        if os.path.exists(tmp_audio_path):
            try:
                os.remove(tmp_audio_path)
            except OSError:
                pass
```
*Apply the same `NamedTemporaryFile(delete=False)` and retry loop pattern to `os.replace` in `extract_audio`.*

**3. Update Unit Tests (`tests/core/test_io.py`)**
- Replace `@patch('src.core.io.uuid.uuid4')` with `@patch('src.core.io.tempfile.NamedTemporaryFile')`.
- Update the mock assertions to match the retry loop / new temporary file logic.

## Verification Method
- **Integrity**: Run `pytest e2e_tests/`. It should fail if `VibeEngine` is incomplete, proving the mock facade is removed.
- **Audio Leak**: Inject `raise KeyboardInterrupt()` inside MoviePy's write function and verify `*TEMP_MPY_wvf_snd.mp3` does not persist.
- **Locking**: Run `pytest -m integration` on Windows to ensure `os.replace` succeeds without crashing.
