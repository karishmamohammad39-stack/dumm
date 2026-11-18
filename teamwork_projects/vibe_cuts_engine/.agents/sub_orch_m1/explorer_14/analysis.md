# Analysis of `src/core/io.py` and `tests/core/test_io.py` bugs

## 1. Race Condition on Temporary Files

**Observation**: 
In `src/core/io.py`, both `export_video` and `extract_audio` create temporary files using a deterministic extension `.tmp`:
- `export_video`: `tmp_path = path + ".tmp"` (Line 32)
- `extract_audio`: `tmp_path = output_audio_path + ".tmp"` (Line 68)

**Logic Chain**:
Because the path is predictable, concurrent operations on the same target file path will attempt to write to the exact same `.tmp` file. This leads to data corruption, access denied errors, or corrupted final outputs. Using a unique identifier (like a UUID) per write operation guarantees isolated temporary paths even if the final target is the same.

**Strategy**:
Replace `.tmp` with a UUID-based suffix:
- `tmp_path = f"{path}.{uuid.uuid4().hex}.tmp"`
- `tmp_path = f"{output_audio_path}.{uuid.uuid4().hex}.tmp"`

Note: Updating this will break unit tests that strictly assert `mock_clip.write_videofile` and `mock_replace` with `".tmp"`. Tests `test_export_video`, `test_extract_audio_success`, and `test_extract_audio_with_output_path` will need to mock `@patch('src.core.io.uuid.uuid4')` to inject a stable UUID (e.g., `'1234'`) for their assertions.

## 2. Exception Masking on Windows

**Observation**:
In `src/core/io.py`, exception handling blocks for the temp file cleanup are:
```python
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
```
(Lines 36-39 and 72-75)

**Logic Chain**:
When `clip.write_videofile` or `audio.write_audiofile` fails, an exception is raised. On Windows, if the underlying process hasn't fully released its file handle by the time `os.remove(tmp_path)` executes, a `PermissionError (WinError 32)` is thrown. This unhandled `PermissionError` masks the original `Exception`, making debugging nearly impossible because the user sees "File in use" instead of the actual codec/ffmpeg error. 

**Strategy**:
Wrap the `os.remove` in a `try...except OSError:` block so that failure to clean up the temporary file doesn't override the primary exception:
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

**Observation**:
In `tests/core/test_io.py`, `test_integration_io` explicitly imports MoviePy 1.x classes from `moviepy.editor`:
```python
@pytest.mark.integration
def test_integration_io():
    # Only run this if moviepy is actually importable and works
    from moviepy.editor import ColorClip
```
(Line 91 and Line 96)

**Logic Chain**:
`src/core/io.py` already includes fallback logic for MoviePy 2.0+ (Lines 5-12), recognizing that `moviepy.editor` was deprecated/removed. But the test suite unconditionally imports from `moviepy.editor`. Running this on an environment with MoviePy 2.0+ will result in an immediate `ImportError`. 

**Strategy**:
Implement the same fallback logic inside the test, and skip if neither is available:
```python
    try:
        from moviepy.editor import ColorClip, AudioClip
    except ImportError:
        try:
            from moviepy import ColorClip, AudioClip
        except ImportError:
            pytest.skip("moviepy is required")
            return
```

## 4. Test Artifact Leaks

**Observation**:
In `test_integration_io`, the code calls `res = extract_audio(input_video_path)` (Line 123) without providing an output path. The `extract_audio` function naturally defaults to putting the output in `tempfile.gettempdir()`. The test asserts its presence but never deletes it.

**Logic Chain**:
Since the test doesn't use the `tmpdir` fixture context manager for this specific output file, the file remains in the system's global `%TEMP%` directory permanently. Over many test runs, this leads to artifact leaks and disk space consumption.

**Strategy**:
Wrap the assertions in a `try...finally` block that explicitly deletes the file:
```python
            res = extract_audio(input_video_path)
            try:
                assert res.endswith(".mp3")
                assert os.path.exists(res)
            finally:
                if os.path.exists(res):
                    os.remove(res)
```
