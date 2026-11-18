# Handoff Report: Iteration 6 - M1 Engine Core & I/O

## 1. Observation
- `src/core/io.py:36` and `src/core/io.py:75` use `except Exception:` during `clip.write_videofile` and `audio.write_audiofile`.
- `KeyboardInterrupt` inherits from `BaseException`, not `Exception`, so if a user hits Ctrl+C, the exception propagates unhandled, leaving the temporary file on disk.
- `src/core/io.py:32` generates temp paths as `f"{path}.{uuid.uuid4().hex}.tmp"`. MoviePy/FFmpeg use the file extension to infer the format. Since it ends with `.tmp` instead of `.mp4` (or similar), format inference crashes.
- `tests/core/test_io.py` currently tests the success path for `export_video` and `extract_audio` but lacks any tests that raise an exception during the write phase to verify the cleanup logic.

## 2. Logic Chain
- To prevent artifact leaks on Ctrl+C, the `except Exception:` blocks must be updated to `except BaseException:`. This will catch `KeyboardInterrupt` and `SystemExit`, ensuring the cleanup block `os.remove(tmp_path)` runs before the exception is re-raised. Alternatively, a `try...finally` block can handle this.
- To resolve the format inference crash, the temporary file must preserve the original file extension. It should be constructed by splitting the base name and extension, inserting `.uuid.tmp` before the extension: `base + "." + uuid_str + ".tmp" + ext`.
- To validate the error path and cleanup in unit tests:
  1. We must mock the underlying write functions (`mock_clip.write_videofile` and `mock_audio.write_audiofile`).
  2. Assign a `side_effect = KeyboardInterrupt("Ctrl+C")` to these mocked write functions to simulate an interrupt during execution.
  3. We must mock `os.path.exists` to return `True` so the cleanup block enters the removal branch.
  4. We must mock `os.remove` to verify it was called.
  5. The test should use `pytest.raises(KeyboardInterrupt)` (or `self.assertRaises(KeyboardInterrupt)`) to ensure the exception is correctly re-raised to the caller.
  6. The assertions must verify that `os.remove` was called exactly once with the correctly formatted temporary file path (e.g., `out_path.1234.tmp.mp4`).

## 3. Caveats
- The changes proposed for `io.py` are straightforward, but test coverage must also mock `os.path.exists` and `os.remove` carefully to avoid deleting real files if the mocks fail.
- `pytest.raises` and `unittest.TestCase.assertRaises` are both valid depending on whether the test suite uses `pytest` tests or `unittest.TestCase`. Currently, `test_io.py` uses `unittest.TestCase`, so `self.assertRaises` should be used for consistency with existing tests.

## 4. Conclusion
The implementer needs to:
1. Update `src/core/io.py` to use `except BaseException:` and fix the temp file string formatting (using `os.path.splitext(path)`).
2. Add new unit tests to `tests/core/test_io.py` (e.g., `test_export_video_keyboard_interrupt_cleanup` and `test_extract_audio_keyboard_interrupt_cleanup`).
3. In these tests, use `@patch` to mock `os.path.exists`, `os.remove`, and `uuid.uuid4`. Use `side_effect = KeyboardInterrupt()` on the mocked clip's write methods, and assert that `os.remove` is called with the properly extended temp file path before the interrupt is re-raised.

## 5. Verification Method
1. Implement the tests and run `pytest tests/core/test_io.py`.
2. Inspect the test output to verify that `KeyboardInterrupt` triggers `os.remove` and re-raises properly.
3. Validate manually by attempting to export a video and hitting `Ctrl+C`, then checking the directory to ensure no `.tmp` or `.tmp.mp4` files are orphaned.
