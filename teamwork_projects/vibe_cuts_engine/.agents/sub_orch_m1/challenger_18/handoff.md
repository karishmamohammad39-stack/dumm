# Handoff Report: M1: Engine Core & I/O (Iteration 8)

## 1. Observation
- The user environment is actively timing out on permission prompts, rendering `run_command` completely unusable for empirical test execution (attempts to run `pytest` and `mkdir` timed out after waiting for user approval).
- Despite this limitation, a deep static adversarial review of `src/core/io.py` and `tests/core/test_io.py` was conducted.
- In `tests/core/test_io.py` at line 196, `mock_replace.assert_called_once_with("out_path.1234.tmp.mp4", "out_path")` is asserted in `test_export_video_no_extension`.
- In `src/core/io.py` inside `export_video` (lines 37-39), if the path has no extension, the `path` variable is mutated to include `.mp4` (e.g. `path = f"{root}{ext}"` where `ext = ".mp4"`). `os.replace(tmp_path, path)` uses this mutated path.
- In `export_video` (lines 29-31) and `extract_audio` (lines 63-64), there is a safeguard: `os.path.abspath(clip.filename) == os.path.abspath(path)`.

## 2. Logic Chain
1. **Broken Unit Test**: The unit test `test_export_video_no_extension` calls `export_video(mock_clip, "out_path")`. Because the function mutates the output path string to `"out_path.mp4"` and calls `os.replace` with `"out_path.mp4"`, the mock assertion expecting `"out_path"` will strictly fail. The worker claimed the tests are correct, but this is a guaranteed unit test failure.
2. **Adversarial Input (Safeguard Bypass)**: The safeguard comparing input and output paths happens *before* the missing-extension fallback is applied. 
   - Attack scenario: An attacker or user passes an input file named `"video.mp4"` and provides the output path as `"video"` (without extension).
   - The safeguard compares `"video.mp4"` and `"video"`, which don't match, so it passes.
   - The path is then mutated to `"video.mp4"`.
   - The function writes a temp file and replaces `"video.mp4"`. 
   - Blast radius: Because the input clip is still actively open and being read from `"video.mp4"`, `os.replace` will either raise a `PermissionError` on Windows (due to file locks) or corrupt the input file on Unix systems, completely bypassing the safety check. The exact same vulnerability exists in `extract_audio`.

## 3. Caveats
- **Lack of Execution**: I could not run empirical verification or tests because all `run_command` executions timed out waiting for user approval in the environment. Thus, I am relying exclusively on static logic tracing.
- The `test_integration_io` uses a `make_frame` returning a Python list `[np.sin(...)]`, which may raise Numpy broadcasting errors inside MoviePy, but this could not be empirically confirmed.

## 4. Conclusion
- **CRITICAL**: The worker's unit test `test_export_video_no_extension` is syntactically invalid regarding its mock assertion and will fail when executed.
- **HIGH**: There is an adversarial bypass in the input/output path safeguard. If the output path lacks an extension but logically defaults to the exact same file as the input, the safeguard is bypassed and can corrupt the input file or crash.

## 5. Verification Method
- **Verify Test Failure**: Once permissions are restored, run `pytest tests/core/test_io.py -k test_export_video_no_extension` to observe the mock assertion failure.
- **Verify Bypass**: Run `python -c "from src.core.io import export_video; from moviepy.editor import VideoFileClip; clip = VideoFileClip('test.mp4'); export_video(clip, 'test')"` to observe the PermissionError or file corruption.
- To fix, move the missing-extension fallback logic *above* the input/output path safeguard check.
