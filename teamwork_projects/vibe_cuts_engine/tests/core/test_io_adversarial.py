import os
import tempfile
import pytest
from src.core.io import load_video, export_video, extract_audio
from moviepy.editor import ColorClip

def test_load_video_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(Exception):
            load_video(tmpdir)

def test_load_video_invalid_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(b"Not a video")
        tmpfile_path = tmpfile.name
    
    try:
        with pytest.raises(Exception):
            load_video(tmpfile_path)
    finally:
        os.remove(tmpfile_path)

def test_export_video_invalid_dir():
    # Attempt to export to a directory that does not exist
    clip = ColorClip(size=(64, 64), color=(255, 0, 0), duration=1)
    clip.fps = 24
    with pytest.raises(Exception):
        export_video(clip, "/this/path/does/not/exist/out.mp4")
    clip.close()

def test_extract_audio_invalid_dir():
    # Attempt to extract audio to a directory that doesn't exist
    with tempfile.TemporaryDirectory() as tmpdir:
        input_video_path = os.path.join(tmpdir, "input.mp4")
        clip = ColorClip(size=(64, 64), color=(255, 0, 0), duration=1)
        clip.fps = 24
        # we need audio to not fail early for "no audio"
        from moviepy.editor import AudioClip
        import numpy as np
        def make_frame(t): return [np.sin(440 * 2 * np.pi * t)]
        clip = clip.set_audio(AudioClip(make_frame, duration=1))
        clip.write_videofile(input_video_path, codec="libx264", audio_codec="aac", fps=24, logger=None)
        
        with pytest.raises(Exception):
            extract_audio(input_video_path, "/this/path/does/not/exist/out.mp3")
        clip.close()
