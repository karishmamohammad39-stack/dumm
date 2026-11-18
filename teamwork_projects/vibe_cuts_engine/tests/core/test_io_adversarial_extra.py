import os
import tempfile
import pytest
from src.core.io import load_video, export_video

try:
    from moviepy.editor import ColorClip
except ImportError:
    pass

def test_export_overwrite_open_file():
    """
    On Windows, replacing an open file raises PermissionError.
    If a user loads a video and exports to the same path, os.replace will fail 
    because the original file handle is held by the clip.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "in_out.mp4")
        
        # Create a dummy video
        clip = ColorClip(size=(64, 64), color=(255, 0, 0), duration=1)
        clip.fps = 24
        clip.write_videofile(input_path, codec="libx264", fps=24, logger=None)
        clip.close()
        
        # Load the video (this opens a file handle to input_path)
        loaded_clip = load_video(input_path)
        
        # Try to export to the SAME path
        # On Windows, os.replace(..., input_path) will raise PermissionError because input_path is open
        try:
            export_video(loaded_clip, input_path)
        except PermissionError:
            # Expected on Windows
            pytest.fail("export_video failed to overwrite the file because it is open by the clip (PermissionError on Windows).")
        finally:
            loaded_clip.close()
