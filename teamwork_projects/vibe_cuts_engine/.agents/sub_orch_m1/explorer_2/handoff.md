# Handoff Report: M1 Architecture & Dependency Analysis

## 1. Observation
- **`PROJECT.md`** specifies that the engine will eventually need to handle:
  - "Layer Compositing System: Manages stacking of multiple media layers, custom keyframing, masking shapes, and dynamic blend modes." (M2)
  - "AI Automation System: Handles audio-synced speed curves, audio extraction, and auto-generated subtitles." (M3)
- **`SCOPE.md`** for M1 defines the interface contracts for `src/core/io.py`:
  - `load_video(path: str) -> VideoClip/Any`
  - `export_video(clip: Any, path: str) -> None`
  - `extract_audio(video_path: str, output_audio_path: str) -> str`
- Both documents suggest utilizing libraries like `moviepy` or `ffmpeg-python`.

## 2. Logic Chain
1. **M1 requirements** (ingest, extract audio, export) are trivial for either `moviepy` or `ffmpeg-python`. Therefore, the dependency choice should be driven by downstream requirements (M2 & M3).
2. **`ffmpeg-python`** operates by constructing FFmpeg filtergraphs. While highly performant (processing runs entirely in C/C++), dynamic programmatic edits (custom keyframing, arbitrary masking shapes, and dynamic blend modes) are notoriously difficult to implement and debug using raw filtergraphs.
3. **`moviepy`** represents video as sequences of numpy arrays and provides built-in abstractions for compositing (`CompositeVideoClip`), masking, and time transformations (`fl_time` for speed curves). This paradigm aligns perfectly with the Python-driven custom keyframing and layering required in M2 and M3.
4. **Architecture**: To decouple the engine from the underlying library, `src/core/io.py` should serve as a boundary. The `VideoClip/Any` type specified in `SCOPE.md` should internally wrap or directly expose a `moviepy.editor.VideoClip` (or `VideoFileClip`), ensuring that the rest of the application can leverage Python-based compositing.

## 3. Caveats
- **Performance**: `moviepy` processes frames in Python (numpy), which is slower than raw FFmpeg filtergraphs, particularly for high-resolution video exports.
- **Resource Management**: `moviepy` clips must be explicitly closed to avoid file handle leaks.
- Alternative approach: A hybrid model where `ffmpeg-python` is used for fast, simple operations (like `extract_audio`), while `moviepy` is reserved for complex compositing. For M1, sticking to a single dependency (`moviepy`) keeps the architecture simple.

## 4. Conclusion
- **Primary Dependency**: Select `moviepy` as the core engine dependency. Its Pythonic abstractions for masking, layering, and time-manipulation are essential for achieving M2 and M3 goals within a reasonable development timeframe.
- **Implementation Strategy for M1**:
  - `load_video(path)`: Instantiate and return `moviepy.editor.VideoFileClip(path)`.
  - `export_video(clip, path)`: Call `clip.write_videofile(path)`.
  - `extract_audio(video_path, output_audio_path)`: Load video, access `clip.audio`, and call `write_audiofile(output_audio_path)`, returning the path.
- **Project Structure**: Implement these in `src/core/io.py`.

## 5. Verification Method
- Implement the code in `src/core/io.py` and unit tests in `tests/test_io.py`.
- Run the project test command (e.g., `pytest tests/test_io.py`) to confirm that videos can be loaded, audio can be extracted to a separate file, and the output video can be exported successfully.
- Manually inspect the output files to ensure they are valid media files.
