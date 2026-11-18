## Observation
1. The auditor report confirms `src/api/vibe_engine.py` does not exist and `e2e_tests/conftest.py` uses a `MockEngine` facade to intercept `ImportError` and return string literals for all API methods.
2. The `conftest.py` mock implementation provides the following methods: `ingest_video`, `extract_audio`, `generate_subtitles`, `apply_speed_curve`, `composite_layers`, `apply_mask`, `apply_blend_mode`, `add_keyframe`, and `export`.
3. The tests across `test_tier1_feature.py` and `test_tier2_boundary.py` only perform weak assertions (e.g., `assert res is not None`), meaning any return value satisfies the tests.
4. Furthermore, some tests in `test_tier2_boundary.py` pass unexpected kwargs (like `z_indices=[-1]` to `composite_layers`) which raise exceptions caught by bare `try ... except Exception: pass` blocks, artificially inflating the pass rate.
5. The `src/core/io.py` script already successfully imports `moviepy` and implements functions for loading, exporting, and extracting audio.

## Logic Chain
1. To resolve the integrity violation without relying on test-side hacks, the worker must physically implement the missing `VibeEngine` class in `src/api/vibe_engine.py` and remove the `MockEngine` fallback entirely.
2. Given that `ORIGINAL_REQUEST.md` asks for an engine architecture (backend library) and no complex AI libraries are included in `requirements.txt`, the most appropriate genuine implementation is a stateful Document-Model (or timeline) engine.
3. The engine should maintain an internal dictionary or data class representing the project state (the "Timeline"), assigning unique IDs (UUIDs) to ingested assets and recording effects (keyframes, masks, speed curves) as metadata on these entities.
4. When `export()` is called, the engine should ideally parse this internal state and use `moviepy` (via `src.core.io.py`) to render the result. If full rendering of complex masks/blend modes is beyond the scope of `moviepy`'s basic capabilities, a best-effort render (like compositing the clips and applying time remapping) is sufficient to prove the backend is not a facade.
5. The methods must accommodate all arguments and `**kwargs` used in the test suite (like `z_indices` in `composite_layers`) to prevent unexpected TypeErrors.

## Caveats
- Auto-generated subtitles and advanced masking/blending might not be natively simple in `moviepy`. The `generate_subtitles` method can genuinely return a struct representing parsed captions without utilizing a real speech-to-text model, provided the engine tracks it as a real asset rather than a string literal.
- Full parity with CapCut/Alight Motion effects is a massive undertaking; the primary goal is to establish a structurally sound API that tracks edits realistically and exports a genuine video, removing the mock violation.

## Conclusion
The fix requires replacing the mock in `conftest.py` with a real `VibeEngine` class that manages an internal timeline state. 

**Fix Strategy for the Worker:**
1. **Remove Mock**: Edit `e2e_tests/conftest.py` to remove the `try...except ImportError` block and unconditionally return `VibeEngine()` from `src.api.vibe_engine`.
2. **Implement VibeEngine**: Create `src/api/vibe_engine.py` containing `class VibeEngine:`.
3. **State Management**: Initialize `self.state = {}` in `__init__` to act as an Edit Decision List (EDL) or timeline.
4. **Implement API**:
   - `ingest_video(self, path)`: Validate path (unless it's a dummy text layer), generate a UUID, store it in `self.state`, and return the UUID.
   - `extract_audio(self, vid_id)`: Use `src.core.io.extract_audio` to generate an audio file, add it to state, and return the new audio ID.
   - `generate_subtitles(self, aud_id)`: Create and store a mock subtitle data structure in the state and return its ID.
   - `apply_speed_curve`, `apply_mask`, `apply_blend_mode`, `add_keyframe`: Update the respective layer's metadata in `self.state` with the effect parameters. Ensure methods accept all arguments present in tests (e.g., `composite_layers(self, layers, **kwargs)` to handle `z_indices`).
   - `composite_layers(self, layers, **kwargs)`: Create a composition entity in the state containing the layers.
   - `export(self, comp_id, out_path)`: Implement rendering logic that processes the timeline state and utilizes `src.core.io.export_video` to output a real video file.

## Verification Method
- Ensure `src/api/vibe_engine.py` exists.
- Ensure `e2e_tests/conftest.py` imports `VibeEngine` directly without a fallback class.
- Run `pytest e2e_tests/` and verify all tests still pass (or fail legitimately based on functionality instead of passing via mock).
