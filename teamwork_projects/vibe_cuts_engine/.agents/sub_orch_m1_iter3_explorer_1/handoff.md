# Handoff Report: `src/core/io.py` Bug Fix Strategy

## 1. Observation
- `PROJECT.md` details the overarching architecture where `src/core/io.py` manages basic media ingestion and export for the engine core. (Note: `SCOPE.md` was not found in the project root).
- In `src/core/io.py`, `export_video` is implemented as:
  ```python
  def export_video(clip, path: str) -> None:
      ...
      try:
          clip.write_videofile(path, codec="libx264", audio_codec="aac")
      finally:
          clip.close()
  ```
- In `src/core/io.py`, `extract_audio` is implemented as:
  ```python
  def extract_audio(video_path: str) -> str:
      ...
      output_audio_path = os.path.splitext(video_path)[0] + ".mp3"
      ...
  ```

## 2. Logic Chain
- **Bug 1 (`clip.close()` in `export_video`)**: The current implementation explicitly closes the `clip` in a `finally` block. Since the clip is provided by the caller (likely loaded via `load_video`), destroying it here prevents the caller from reusing it for further processing or compositing (a core requirement of M2/M4). Removing the `try...finally` block entirely shifts the lifecycle management back to the caller, who can safely manage it via context managers (`with` statements) or explicit `.close()` calls.
- **Bug 2 (unsafe `extract_audio` path)**: The statically computed path `os.path.splitext(video_path)[0] + ".mp3"` risks overwriting any existing `.mp3` source files and forces writing into the source directory. By adding an optional `output_path` parameter, we give callers the flexibility to define safe output locations (e.g. temporary directories). For safety when `output_path` is not provided, changing the suffix to `_audio.mp3` prevents overwriting the original file (if it was an mp3 to begin with).

## 3. Caveats
- I assumed backward compatibility is somewhat necessary, hence keeping the default path generation in `extract_audio` but modifying it to be safer (`_audio.mp3`).
- I did not review calling modules to verify if they depend on `export_video` automatically closing the clip. The implementer should ensure tests are updated so that any caller that relied on this side effect is now managing the clip closing themselves.
- `SCOPE.md` was not available for review, but the issues and files were explicitly specified, so this did not block analysis.

## 4. Conclusion
The recommended fix strategy for `src/core/io.py` is as follows:

1. **Modify `export_video`**:
   Remove the `try...finally` block and leave just the write function.
   ```python
   def export_video(clip, path: str) -> None:
       """
       Export the given video clip to the specified path.
       """
       dir_name = os.path.dirname(path)
       if dir_name:
           os.makedirs(dir_name, exist_ok=True)
       clip.write_videofile(path, codec="libx264", audio_codec="aac")
   ```

2. **Modify `extract_audio` signature and path generation**:
   Change the signature to accept an optional `output_path` and update the fallback string to append `_audio.mp3`.
   ```python
   def extract_audio(video_path: str, output_path: str = None) -> str:
       """
       Extract audio from a video and save it to output_path.
       If output_path is None, defaults to <video_basename>_audio.mp3.
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
- **Static Analysis**: Verify `src/core/io.py` no longer contains `clip.close()` in `export_video` and that `extract_audio` has the updated signature.
- **Unit Testing**: Run `pytest tests/test_io.py` (or the equivalent test suite). The tests should ensure:
  1. A video exported via `export_video` can still have attributes read from the original clip instance post-export.
  2. `extract_audio` writes to the specified `output_path` when provided.
  3. `extract_audio` safely appends `_audio.mp3` when `output_path` is not provided.
