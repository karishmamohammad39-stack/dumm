# Synthesis: Iteration 9 Fix Strategy

## Consensus
The Iteration 8 implementation failed due to test assertion bugs, validation sequence bypassing, and incomplete cleanup of MoviePy's auxiliary files. We will use `tempfile.TemporaryDirectory` to solve the cleanup completely and adjust the logic order.

## 1. Validation Sequence Bug
- **Fix**: In `src/core/io.py` (`export_video` and `extract_audio`), move the extension normalization (e.g., `path = path + ".mp4"`) *above* the collision check (where it prevents `clip.filename == path`). This prevents bypassing the check with extensionless inputs.

## 2. MoviePy Auxiliary File Leak
- **Fix**: Replace `uuid4()` and `try...finally: os.remove(...)` with a `with tempfile.TemporaryDirectory(dir=os.path.dirname(path) or '.') as temp_dir:` context manager.
- Create the temporary path inside the tempdir (e.g., `tmp_path = os.path.join(temp_dir, f"temp{ext}")`).
- All MoviePy auxiliary files created alongside `tmp_path` will be automatically deleted when the `with` block exits (even on `KeyboardInterrupt` or standard exceptions).

## 3. Extension Propagation Bug
- **Fix**: Ensure that the target path is modified (e.g., `path = path + ".mp4"` if there is no extension) before it is passed to `os.replace(tmp_path, path)`. 

## 4. Test Assertion Bug & Test Updates
- **Fix**: In `tests/core/test_io.py`:
  - `test_export_video_no_extension`: Update the mock assertion to expect `os.replace` to be called with `"out_path.mp4"` instead of `"out_path"`.
  - Update all tests patching `uuid.uuid4` and `os.remove` to instead patch `src.core.io.tempfile.TemporaryDirectory`. Set it up to yield a known mock path (e.g. `'/fake_temp'`).
  - Update assertions to expect `os.path.join('/fake_temp', 'temp.mp4')`.
  - Remove tests that solely verify `os.remove` handling (like `test_export_video_cleanup_oserror`), as `TemporaryDirectory` handles it natively.
