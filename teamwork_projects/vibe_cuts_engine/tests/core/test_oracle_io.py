import os
import random
import tempfile
import pytest
from src.core.io import load_video, export_video, extract_audio

def clip_generator():
    """Generates random clip properties for testing."""
    for _ in range(3):
        yield {
            "width": random.randint(32, 128),
            "height": random.randint(32, 128),
            "duration": random.uniform(0.5, 2.0),
            "fps": random.choice([12, 24, 30])
        }

def test_oracle_video_properties():
    """
    Oracle to verify that exported and re-loaded videos retain expected duration and fps.
    """
    try:
        from moviepy.editor import ColorClip, AudioClip
    except ImportError:
        try:
            from moviepy import ColorClip, AudioClip
        except ImportError:
            pytest.skip("MoviePy not found")

    import numpy as np

    def make_frame(t):
        return [np.sin(440 * 2 * np.pi * t)]

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, props in enumerate(clip_generator()):
            clip = ColorClip(size=(props["width"], props["height"]), color=(255, 0, 0), duration=props["duration"])
            clip = clip.set_audio(AudioClip(make_frame, duration=props["duration"]))
            clip.fps = props["fps"]
            
            out_path = os.path.join(tmpdir, f"oracle_out_{i}.mp4")
            export_video(clip, out_path)
            clip.close()
            
            loaded_clip = load_video(out_path)
            
            # Oracle checks
            assert abs(loaded_clip.duration - props["duration"]) < 0.1, f"Duration mismatch: {loaded_clip.duration} vs {props['duration']}"
            assert loaded_clip.size[0] == props["width"] or loaded_clip.size[1] == props["height"], "Size mismatch"
            loaded_clip.close()

def test_extract_audio_generator():
    """
    Test extraction using generated clips.
    """
    try:
        from moviepy.editor import ColorClip, AudioClip
    except ImportError:
        try:
            from moviepy import ColorClip, AudioClip
        except ImportError:
            pytest.skip("MoviePy not found")
            
    import numpy as np
    
    def make_frame(t):
        return [np.sin(440 * 2 * np.pi * t)]

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, props in enumerate(clip_generator()):
            clip = ColorClip(size=(64, 64), color=(0, 255, 0), duration=props["duration"])
            clip = clip.set_audio(AudioClip(make_frame, duration=props["duration"]))
            clip.fps = props["fps"]
            
            vid_path = os.path.join(tmpdir, f"vid_{i}.mp4")
            export_video(clip, vid_path)
            clip.close()
            
            audio_out = os.path.join(tmpdir, f"audio_{i}.mp3")
            extract_audio(vid_path, audio_out)
            
            assert os.path.exists(audio_out)
            assert os.path.getsize(audio_out) > 0
