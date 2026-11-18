import os
import pytest
from unittest.mock import MagicMock
from src.core.io import load_video, export_video, extract_audio

class MockClip:
    def __init__(self):
        self.audio = MagicMock()
        self.closed = False
        self.written_video = None

    def close(self):
        self.closed = True

    def write_videofile(self, path, codec=None, audio_codec=None):
        self.written_video = path

@pytest.fixture
def mock_video_file(tmp_path):
    video_path = tmp_path / "test_video.mp4"
    video_path.write_text("dummy content")
    return str(video_path)

@pytest.fixture
def mock_no_audio_file(tmp_path):
    video_path = tmp_path / "no_audio.mp4"
    video_path.write_text("dummy content")
    return str(video_path)

def test_load_video_not_found():
    with pytest.raises(FileNotFoundError):
        load_video("non_existent_file.mp4")

def test_export_video_closes_clip(tmp_path):
    """
    BUG IDENTIFIED: export_video takes a clip and closes it in a finally block. 
    This means the caller cannot use the clip after exporting it, breaking the principle 
    that the creator of a resource should close it, or at least breaking subsequent compositing steps.
    """
    clip = MockClip()
    output_path = str(tmp_path / "output.mp4")
    
    export_video(clip, output_path)
    
    assert clip.written_video == output_path
    # This assert demonstrates the behavior: the clip is closed by the export function.
    # In a pipeline, we might want to export and then do something else, which would now fail.
    assert clip.closed is True 

def test_extract_audio_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_audio("non_existent_file.mp4")

# Note: Further tests require actual moviepy VideoFileClip mocking or real video files.
# The main logical bug found statically is `clip.close()` in `export_video`.
