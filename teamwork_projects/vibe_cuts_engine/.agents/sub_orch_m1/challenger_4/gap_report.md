# Gap Report: `src/core/io.py`

## Overview
This report identifies gaps in edge case handling, API flexibility, and resource management within the `src/core/io.py` module. 

## Identified Gaps

### 1. Resource Management Gap
- **Gap**: `export_video(clip, path)` unconditionally closes the `clip` object.
- **Impact**: The caller cannot reuse the `clip` object for further edits, rendering, or operations after exporting. This violates the principle of least astonishment for a utility function.

### 2. Output Path Flexibility Gap
- **Gap**: `extract_audio(video_path)` hardcodes the output path to the same directory as the input video.
- **Impact**: The function will fail with a `PermissionError` if the source video resides on a read-only volume or a network drive without write access.

### 3. Path Collision Edge Case Gap
- **Gap**: `extract_audio` constructs the output path using `os.path.splitext(video_path)[0] + ".mp3"`. If the input video itself is an `.mp3` file (e.g. an audio file passed by mistake) or named `video.mp3.mp4`, path collisions can occur. In the case of `.mp3`, the output path equals the input path.
- **Impact**: Overwriting the input file while it is open for reading, causing corruption or file-lock exceptions (especially on Windows).

### 4. Codec Flexibility Gap
- **Gap**: `export_video` hardcodes `codec="libx264"` and `audio_codec="aac"`.
- **Impact**: Users cannot export to other formats (e.g. WebM, ProRes, uncompressed) without modifying core engine code.
