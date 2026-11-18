# Analysis of Iteration 4 Bug Fixes for `io.py`

This document details the analysis and proposed implementation strategy for fixing the 4 remaining bugs in `src/core/io.py` and `tests/core/test_io.py`.

## 1. Race Condition on Temporary Files
**Problem**: The functions `export_video` and `extract_audio` use deterministic temporary file names (`path + ".tmp"`). Concurrent calls writing to the same destination will clash on the same `.tmp` file.
**Solution**: Inject a UUID into the temporary filename. 
- In `export_video`: `tmp_path = f"{path}.{uuid.uuid4().hex}.tmp"`
- In `extract_audio`: `tmp_path = f"{output_audio_path}.{uuid.uuid4().hex}.tmp"`
- **Test Adjustment**: Update `tests/core/test_io.py` (specifically `test_export_video`, `test_extract_audio_success`, and `test_extract_audio_with_output_path`) to match dynamic strings when asserting `write_videofile` and `os.replace` (e.g., retrieving `call_args` and using `startswith`/`endswith`).

## 2. Exception Masking on Windows
**Problem**: On Windows, when an exception occurs during export, the `except Exception:` block attempts `os.remove(tmp_path)`. If the background ffmpeg process has not yet released the file handle, this triggers a `PermissionError` (WinError 32), which masks the original exception and crashes the cleanup.
**Solution**: Wrap the `os.remove(tmp_path)` calls inside a `try...except OSError:` block so that the cleanup failure does not hide the actual export failure.
```python
except Exception:
    if os.path.exists(tmp_path):
        try:
            os.remove(tmp_path)
        except OSError:
            pass
    raise
```

## 3. Test Dependency Mismatch
**Problem**: `test_integration_io` in `tests/core/test_io.py` statically imports `ColorClip` and `AudioClip` from `moviepy.editor`. This crashes on MoviePy 2.0+ because the module structure changed.
**Solution**: Replicate the fallback logic in `test_integration_io` using `try...except ImportError`:
```python
try:
    from moviepy.editor import ColorClip, AudioClip
except ImportError:
    try:
        from moviepy import ColorClip, AudioClip
    except ImportError:
        pytest.skip("moviepy not installed or incompatible version")
```

## 4. Test Artifact Leaks
**Problem**: `test_integration_io` calls `res = extract_audio(input_video_path)`. Since no output path is passed, the MP3 is written to the global temp directory (`%TEMP%`). The test asserts the file exists but does not delete it, causing a permanent artifact leak.
**Solution**: Delete the file explicitly after asserting.
```python
res = extract_audio(input_video_path)
assert res.endswith(".mp3")
assert os.path.exists(res)
os.remove(res) # Clean up the globally scoped file
```
