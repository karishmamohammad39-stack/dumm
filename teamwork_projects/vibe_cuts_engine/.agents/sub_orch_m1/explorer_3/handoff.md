# Handoff Report: M1 Testing Strategy

## Observation
I have reviewed the project specifications in `PROJECT.md` and `SCOPE.md`. 
For Milestone 1 (M1), the scope is "Engine Core & I/O" which involves ingesting video files, extracting audio, and performing basic exports.
The specific interface contract defined in `SCOPE.md` for `src/core/io.py` includes:
- `load_video(path: str) -> VideoClip/Any`
- `export_video(clip: Any, path: str) -> None`
- `extract_audio(video_path: str, output_audio_path: str) -> str`

It is also noted that the implementation will likely utilize libraries like `moviepy` or `ffmpeg-python`.

## Logic Chain
1. **Nature of the Code**: The module `src/core/io.py` primarily acts as a wrapper around heavy external libraries (`moviepy` or `ffmpeg-python`) to interact with the file system.
2. **Testing Needs**: 
   - We must test the business logic (correct arguments passed to libraries, handling of return values).
   - We must test exception handling (e.g., missing input files, invalid formats, un-writable output paths).
   - We must verify the actual IO boundaries to ensure the chosen underlying library correctly reads and writes real files on disk.
3. **Efficiency constraints**: Video files are large and video processing is slow. Relying entirely on real video files for all tests will make the test suite slow and bloated.
4. **Proposed Testing Strategy**:
   - **Unit Tests with Mocks**: Use `unittest.mock` (or `pytest-mock`) to mock the underlying media library (`moviepy.VideoFileClip`, etc.). This allows fast testing of our wrapper logic, verifying that the correct file paths and parameters are passed to the external dependencies without performing any actual file I/O.
   - **IO Boundary Tests with Small Fixtures**: Create a separate integration test suite that tests the actual I/O. To keep this fast and lightweight, we should programmatically generate a very short (e.g., 1-second, low-resolution) blank video and audio fixture during test setup (or include minimal `< 10KB` dummy files in a `tests/fixtures/` folder). The integration tests will run `load_video`, `export_video`, and `extract_audio` against these fixtures.

## Caveats
- The exact mocking strategy depends on whether the implementer chooses `moviepy` or `ffmpeg-python`. Mocks will need to be tailored to the specific library's API.
- If programmatic generation of test fixtures is complex, static minimal test files must be checked into the repository under `tests/fixtures/`, which slightly increases repo size.

## Conclusion
To ensure a robust and fast test suite for M1, adopt a dual testing strategy:
1. **Mocked Unit Tests**: Test `src/core/io.py` by patching the underlying media libraries to ensure paths and configurations are handled correctly, testing success paths and error states (like missing file exceptions) quickly.
2. **Integration IO Tests**: Test the true IO boundaries using minimal dummy video files (either generated dynamically during test setup or stored in `tests/fixtures/`) to verify that the wrapper actually produces readable/writable outputs without hanging or crashing.

## Verification Method
1. Inspect `tests/core/test_io.py` to ensure it contains tests that utilize mocks for the underlying video library.
2. Inspect `tests/core/test_io_integration.py` (or similar) to ensure real file reads/writes are tested against small fixtures.
3. Run `pytest tests/` and verify that the tests pass quickly (under a few seconds).
