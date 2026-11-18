# Handoff: io.py and test_io.py Bug Fixes

## 1. Observation
- **Bug 1 (Race Condition)**: In `src/core/io.py` lines 32 and 68, temporary files are created as `tmp_path = path + ".tmp"` and `tmp_path = output_audio_path + ".tmp"`. Tests in `tests/core/test_io.py` mock assertions expecting exact `".tmp"` suffixes (e.g. `mock_clip.write_videofile.assert_called_once_with("out_path.mp4.tmp", ...)`).
- **Bug 2 (Exception Masking)**: In `src/core/io.py` lines 38 and 74, `os.remove(tmp_path)` is executed in a bare `except Exception:` block without its own error handling. On Windows, this raises `PermissionError` if the file handle is locked, overriding the initial exception.
- **Bug 3 (Test Mismatch)**: In `tests/core/test_io.py` lines 91 and 96, `from moviepy.editor import ColorClip` and `AudioClip` are explicitly imported. This crashes on MoviePy 2.0+ which removed the `editor` submodule (as correctly handled in the main code).
- **Bug 4 (Test Artifact Leaks)**: In `tests/core/test_io.py` line 123, `res = extract_audio(input_video_path)` writes to `tempfile.gettempdir()` by default. The file `res` is verified via assertions but never deleted, leaking it globally.

## 2. Logic Chain
1. **Fixing Bug 1**: Hardcoded `.tmp` extensions cause collision under concurrent access. We must append a unique UUID (e.g., `f".{uuid.uuid4().hex}.tmp"`). Because this changes the deterministic path, the corresponding unit tests (`test_export_video`, `test_extract_audio_success`, `test_extract_audio_with_output_path`) will fail unless we patch `uuid.uuid4` to return a predictable string in those tests.
2. **Fixing Bug 2**: When `os.remove` fails during exception cleanup, it raises a new `OSError` that hides the real error. Wrapping `os.remove(tmp_path)` in `try...except OSError: pass` safely swallows the cleanup failure and allows the original encoding exception to bubble up.
3. **Fixing Bug 3**: The integration test is completely broken for MoviePy 2.0+. We must replicate `io.py`'s fallback strategy inside `test_integration_io` by attempting to import from `moviepy.editor`, then falling back to `moviepy`, and finally using `pytest.skip` if neither works.
4. **Fixing Bug 4**: The global artifact leak is trivially fixed by ensuring that `res` is removed in a `finally` block after the assertions on the extracted audio.

## 3. Caveats
- Wrapping `os.remove` in `try...except OSError` will leave a zombie `.tmp` file on the filesystem if an error occurs and the file is locked. However, this is highly preferable to masking the root error and crashing unhelpfully.
- Patching `uuid.uuid4` in tests means adding an additional `@patch` decorator and an argument to the test method signature. Care must be taken to match decorator order with arguments.

## 4. Conclusion
Implement the following changes to resolve the 4 bugs:
1. Update `src/core/io.py` to use `f"{path}.{uuid.uuid4().hex}.tmp"` for temp files.
2. Update `src/core/io.py` `except Exception:` blocks to wrap `os.remove(tmp_path)` in a nested `try...except OSError: pass` block.
3. Update `tests/core/test_io.py` unit tests with `@patch('src.core.io.uuid.uuid4')` (mocking `.hex` to return a fixed string like `'1234'`) and update assertions accordingly (e.g., `.1234.tmp`).
4. Update `tests/core/test_io.py` `test_integration_io` to use a `try/except ImportError` block falling back to `from moviepy import ...` or skipping the test.
5. Update `tests/core/test_io.py` `test_integration_io` to wrap the `extract_audio` assertions in a `try...finally` block that removes the returned path.

## 5. Verification Method
1. Run unit tests to verify mocked paths: `pytest tests/core/test_io.py`
2. Validate MoviePy 2.0+ fallback: Temporarily run `pip install "moviepy>=2.0.0"` and run `pytest tests/core/test_io.py` to ensure it passes (or skips cleanly).
3. Validate Leak Fix: Run `pytest tests/core/test_io.py -k test_integration_io`, and verify that no new `audio_*.mp3` files are present in the system's `%TEMP%` directory.
