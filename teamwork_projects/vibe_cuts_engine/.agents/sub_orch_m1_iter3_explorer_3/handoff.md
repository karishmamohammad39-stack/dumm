# Handoff Report: Fix Strategy for `src/core/io.py`

## 1. Observation
- `src/core/io.py`, lines 26-29: `export_video` wraps `clip.write_videofile` in a `try...finally` block that forcefully calls `clip.close()`.
- `tests/core/test_io.py`, line 36: `mock_clip.close.assert_not_called()` expects `export_video` NOT to close the clip.
- `src/core/io.py`, line 31: `def extract_audio(video_path: str) -> str:` only takes one argument.
- `src/core/io.py`, line 47: `output_audio_path = os.path.splitext(video_path)[0] + ".mp3"` overwrites any existing file with the same name.
- `tests/core/test_io.py`, lines 65 and 123: Call `extract_audio` with a second argument for the custom output path.
- `tests/core/test_io.py`, lines 51 and 117: Expect the default output path to append `_audio.mp3` rather than just `.mp3`.

## 2. Logic Chain
- **Bug 1**: Calling `clip.close()` inside `export_video` destroys the caller's clip, preventing further downstream operations (like applying more effects or compositing). The test `test_export_video` explicitly verifies this behavior, leading to test failure. Removing the `try...finally` block fixes this. The clip creator is naturally responsible for closing it.
- **Bug 2**: Hardcoding the output path with a simple `.mp3` extension causes a risk of file overwriting and inflexibility for read-only environments. Providing an optional `output_path` parameter satisfies the test suite's expectations and allows callers to supply a safe location (e.g., a temporary directory). Defaulting to an `_audio.mp3` suffix matches test expectations and adds safety against overwriting the source file if it had an `.mp3` extension.

## 3. Caveats
- `os.makedirs` exists in both functions. In `extract_audio`, if `output_path` is provided, `os.makedirs` will ensure the parent directory exists.
- The `try...finally` block in `extract_audio` correctly closes the *locally instantiated* `video` and `audio` clips, so this must be kept intact to prevent resource leaks. Only `export_video` should have its `clip.close()` removed since the clip is passed in as an argument.

## 4. Conclusion
We should update `src/core/io.py` as follows:

**For Bug 1:**
Modify `export_video` to remove `clip.close()`:
```python
def export_video(clip, path: str) -> None:
    """
    Export the given video clip to the specified path.
    """
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    # Removed try...finally clip.close() so the caller manages lifecycle
    clip.write_videofile(path, codec="libx264", audio_codec="aac")
```

**For Bug 2:**
Update `extract_audio` signature and path logic:
```python
def extract_audio(video_path: str, output_path: str = None) -> str:
    """
    Extract audio from a video and save it to output_path.
    Returns the path to the saved audio file.
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")
    
    video = None
    audio = None
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        if audio is None:
            raise ValueError(f"No audio found in {video_path}")
        
        # Safe fallback: append _audio.mp3 if output_path is not specified
        if output_path is None:
            output_path = os.path.splitext(video_path)[0] + "_audio.mp3"
            
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        audio.write_audiofile(output_path)
        return output_path
    finally:
        if audio is not None:
            audio.close()
        if video is not None:
            video.close()
```

## 5. Verification Method
- Execute `pytest tests/core/test_io.py tests/core/test_io_adversarial.py` to ensure unit and adversarial tests pass.
- Verify `export_video` no longer raises errors or fails assertions about `mock_clip.close.assert_not_called()`.
- Verify `extract_audio` passes when given a custom output path, and successfully falls back to `_audio.mp3` when only 1 argument is provided.
