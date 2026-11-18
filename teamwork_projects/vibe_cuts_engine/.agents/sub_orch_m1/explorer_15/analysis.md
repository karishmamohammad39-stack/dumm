# Analysis of IO Core Bugs

## 1. Race Condition on Temporary Files
**File:** `src/core/io.py`
**Lines:** 32, 68
**Issue:** `tmp_path` is constructed deterministically as `path + ".tmp"` and `output_audio_path + ".tmp"`. Concurrent exports to the same file path will cause collisions and clobbering of the temporary files.
**Proposed Fix:** Append a UUID to the temporary file path, e.g., `tmp_path = f"{path}.{uuid.uuid4().hex}.tmp"`.

## 2. Exception Masking on Windows
**File:** `src/core/io.py`
**Lines:** 36-39, 72-75
**Issue:** `os.remove(tmp_path)` inside the `except Exception:` block may fail on Windows with `PermissionError: [WinError 32]` if background processes (like FFmpeg) have not fully released the file handles when an exception occurs. This unhandled `OSError` will mask the original exception.
**Proposed Fix:** Wrap `os.remove(tmp_path)` with a `try...except OSError: pass` block.

## 3. Test Dependency Mismatch
**File:** `tests/core/test_io.py`
**Lines:** 91, 96
**Issue:** The test `test_integration_io` explicitly imports `ColorClip` and `AudioClip` from `moviepy.editor`. This contradicts the fallback provided in `src/core/io.py` for MoviePy 2.0+ and causes an `ImportError`.
**Proposed Fix:** Update the imports in `test_integration_io` to use a `try...except ImportError` fallback structure identical to `src/core/io.py`, attempting to import from `moviepy.editor` and then falling back to `moviepy`. If both fail, call `pytest.skip("moviepy is required")`.

## 4. Test Artifact Leaks
**File:** `tests/core/test_io.py`
**Lines:** 122-125
**Issue:** The `extract_audio(input_video_path)` call without an explicit `output_path` generates an audio file in the system's global temporary directory (`tempfile.gettempdir()`). The test fails to clean this up, permanently leaking files in `%TEMP%`.
**Proposed Fix:** Explicitly remove the returned audio file (`os.remove(res)`) using a `try...finally` block or right after the assertions.
