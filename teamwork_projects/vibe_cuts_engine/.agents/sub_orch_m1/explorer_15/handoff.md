# Handoff: IO Core Bug Fixes

## 1. Observation
- **Race Condition**: `src/core/io.py` constructs temporary paths using `tmp_path = path + ".tmp"` (line 32) and `tmp_path = output_audio_path + ".tmp"` (line 68).
- **Exception Masking**: In `src/core/io.py` (lines 36-39 and 72-75), `os.remove(tmp_path)` is called within an `except Exception:` block without catching potential `OSError`s.
- **Dependency Mismatch**: `tests/core/test_io.py` (lines 91, 96) hardcodes `from moviepy.editor import ColorClip` and `from moviepy.editor import AudioClip`, while `src/core/io.py` handles MoviePy 2.0+ via fallback imports.
- **Artifact Leak**: `tests/core/test_io.py` (lines 123-125) tests `extract_audio(input_video_path)`, which creates an mp3 file in the system temp directory, but the test does not delete it.

## 2. Logic Chain
- Deterministic `.tmp` paths mean concurrent processes exporting to the same location overwrite each other's temporary files, leading to corrupted exports. A UUID-based suffix will make the writes atomic.
- On Windows, if FFmpeg or MoviePy crashes but holds onto the file descriptor, `os.remove` will raise a `PermissionError`, hiding the true cause of the crash. Swallowing `OSError` ensures the original exception propagates.
- Because `moviepy.editor` was deprecated/restructured in MoviePy 2.0+, tests relying solely on the old import path will fail instantly. Introducing a fallback mechanism identical to the source code ensures compatibility across versions.
- Since `extract_audio()` without an output path returns an auto-generated file in `%TEMP%`, calling it in tests without explicit cleanup leaves junk files on the developer's system. Deleting the returned path fixes the leak.

## 3. Caveats
- The UUID suffix solution assumes that `os.replace` on the same file system is atomic, which is true for local drives but might not be strictly true for all network filesystems.
- Ignoring `OSError` during temporary file cleanup means a temporary file might be left behind on error. This is a standard trade-off to prioritize error visibility over complete cleanup.

## 4. Conclusion
The four bugs can be resolved with localized code changes. 
1. `io.py`: Update `tmp_path` variables to include `uuid.uuid4().hex`.
2. `io.py`: Wrap `os.remove(tmp_path)` in `try...except OSError: pass`.
3. `test_io.py`: Implement try/except import logic for `ColorClip` and `AudioClip`.
4. `test_io.py`: Add cleanup (`os.remove(res)`) for the default path artifact.

## 5. Verification Method
- Run `pytest tests/core/test_io.py` to ensure tests pass and the dependency mismatch is fixed.
- Check the system's temporary directory before and after running the test to ensure no `.mp3` files are leaked.
- Code review the implementation of UUIDs and `OSError` catch blocks in `src/core/io.py`.
