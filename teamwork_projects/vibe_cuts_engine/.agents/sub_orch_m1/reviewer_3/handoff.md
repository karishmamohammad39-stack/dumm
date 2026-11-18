# Handoff Report

## Observation
- In `src/core/io.py`, `export_video(clip, path: str)` contains a `try/finally` block that calls `clip.close()`.
- In `src/core/io.py`, `extract_audio(video_path: str)` dynamically generates the output path as `os.path.splitext(video_path)[0] + ".mp3"`.
- `tests/core/test_io.py` asserts that `mock_clip.close.assert_called_once()` in `test_export_video`.
- The integration test does not attempt to use `clip` after passing it to `export_video`.

## Logic Chain
- `export_video` accepts an instantiated `clip` object as an argument. By calling `clip.close()` in the `finally` block, it takes ownership of the resource and forcefully closes it. This prevents the caller from reusing the clip (e.g., exporting to multiple resolutions, continuing to use it in a compositing pipeline, or previewing it). Resource ownership dictates that the entity that opens the resource (like `load_video` or the caller) should be responsible for closing it.
- In `extract_audio`, if `video_path` happens to end in `.mp3` (e.g., a misnamed video file), `output_audio_path` will be identical to `video_path`. Writing to `output_audio_path` while the input is open will lead to file corruption.
- Because `test_integration_io` does not test the state of `clip` post-export, the aggressive closing behavior was not caught by tests.

## Caveats
- `moviepy` clips do sometimes release file handles upon `close()`, which is important for avoiding leaks. However, the responsibility lies with the caller of `load_video` or a top-level pipeline manager, not the utility function `export_video`.
- The adversarial case of a video file ending in `.mp3` is rare but represents a critical file corruption vulnerability. Appending a suffix like `_audio.mp3` or checking if `input == output` would mitigate this.

## Conclusion
**Verdict**: REQUEST_CHANGES
**Critical Finding (Bug)**: `export_video` destroys the `clip` object by closing it. It should not close a clip it did not open. Remove the `try/finally` and `clip.close()` from `export_video`.
**Major Finding (Vulnerability)**: `extract_audio` can overwrite and corrupt the input file if the input file has an `.mp3` extension. Add a guard to ensure `output_audio_path != video_path` or use a distinct suffix (e.g. `_audio.mp3`).
**Test Fixes**: Update `test_export_video` to remove `mock_clip.close.assert_called_once()`. Optionally, enhance `test_integration_io` to verify the clip is still usable (e.g., check `clip.duration`) after export.

## Verification Method
- Manually inspect `src/core/io.py` to ensure `export_video` does not call `clip.close()`.
- Check `extract_audio` for output path collision handling.
- Verify unit tests using `pytest tests/core/test_io.py`.
