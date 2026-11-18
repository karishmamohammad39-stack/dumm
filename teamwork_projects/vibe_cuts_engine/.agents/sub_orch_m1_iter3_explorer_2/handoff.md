# Handoff Report: `src/core/io.py` Bug Analysis and Fix Strategy

## Observation
1. In `src/core/io.py` at line 29, `export_video(clip, path: str)` forcefully calls `clip.close()` inside a `finally` block after executing `clip.write_videofile(...)`.
2. In `src/core/io.py` at line 47, `extract_audio(video_path: str)` dynamically creates the output path as: `output_audio_path = os.path.splitext(video_path)[0] + ".mp3"`.
3. The file `SCOPE.md` could not be found in the workspace root, but `PROJECT.md` dictates the interface contract for `extract_audio(video_path: str) -> str`.
4. MoviePy's `clip.close()` destroys the clip's underlying resources (file handles, audio decoders, etc.), rendering the `clip` instance unusable for any subsequent operations.

## Logic Chain
1. **Bug 1 (`export_video` resource destruction):** 
   - When `export_video` closes the `clip`, it incorrectly takes ownership of a resource it didn't create. 
   - If the caller needs to reuse the `clip` after exporting (e.g., rendering a different resolution, extracting a subclip, or applying another layer), the program will crash because the clip's internal readers are closed.
   - **Fix Logic:** The component that instantiates the `clip` should be responsible for closing it. `export_video` should only handle the rendering process (`write_videofile`).
2. **Bug 2 (`extract_audio` unsafe path generation):**
   - By hardcoding the output to the same directory as `video_path`, the function will fail with a `PermissionError` if the input directory is read-only.
   - Furthermore, simply replacing the extension with `.mp3` risks overwriting an existing `.mp3` file that shares the exact same base name.
   - **Fix Logic:** Allowing the caller to provide a specific `output_path` circumvents the read-only directory issue entirely. If omitted, modifying the generated name to append a distinctive suffix (e.g., `_audio.mp3`) avoids immediate overwrite collisions.

## Caveats
- `SCOPE.md` was missing, so assumptions are based on `PROJECT.md` and standard API design principles.
- Removing `clip.close()` from `export_video` shifts the burden of resource cleanup entirely to the caller. Callers MUST ensure they use a context manager (`with VideoFileClip(...) as clip:`) or manually call `clip.close()` to avoid memory/file descriptor leaks.
- Altering the fallback filename in `extract_audio` from `.mp3` to `_audio.mp3` may break hardcoded assumptions in caller code if they do not rely on the string returned by the function. Since the function returns the generated path, compliant callers will adapt seamlessly.

## Conclusion
**Strategy to fix Bug 1 (`export_video`):**
- Remove the `try...finally` block and the `clip.close()` call.
- Update the function's docstring to state clearly: "The caller is responsible for managing the clip's lifecycle and closing it."

**Strategy to fix Bug 2 (`extract_audio`):**
- Update the function signature to include an optional argument: `def extract_audio(video_path: str, output_path: str = None) -> str:`.
- Add logic: if `output_path` is provided, use it directly. 
- If `output_path` is `None`, use a safer fallback: `output_audio_path = os.path.splitext(video_path)[0] + "_audio.mp3"`.

## Verification Method
1. **Build/Test:** Run `pytest tests/` after applying the fixes.
2. **Verify Bug 1:** Write a test that calls `export_video(clip, path)` and subsequently queries `clip.duration` or attempts a second `export_video` call. It should succeed without throwing a "file closed" or "reader closed" error.
3. **Verify Bug 2:** 
   - Call `extract_audio` with a specific `output_path` (e.g., in a temporary directory) and assert the file is written exactly there.
   - Call `extract_audio` on `foo.mp4` without an `output_path` and assert the returned path is `foo_audio.mp3` rather than `foo.mp3`.
