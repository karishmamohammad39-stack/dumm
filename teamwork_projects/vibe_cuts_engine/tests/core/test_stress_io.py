import os
import tempfile
import threading
import pytest
from src.core.io import export_video, extract_audio

def test_stress_concurrent_exports():
    """
    Stress test harness to verify thread safety and race conditions during concurrent video exports.
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

    num_threads = 5
    exceptions = []

    def export_task(idx, tmpdir):
        try:
            clip = ColorClip(size=(64, 64), color=(255, idx * 10, 0), duration=1)
            clip = clip.set_audio(AudioClip(make_frame, duration=1))
            clip.fps = 24

            out_path = os.path.join(tmpdir, f"out_{idx}.mp4")
            export_video(clip, out_path)
            
            # Extract audio from exported video
            audio_out = os.path.join(tmpdir, f"audio_{idx}.mp3")
            extract_audio(out_path, audio_out)
            
            clip.close()
        except Exception as e:
            exceptions.append(e)

    with tempfile.TemporaryDirectory() as tmpdir:
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=export_task, args=(i, tmpdir))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()

        assert not exceptions, f"Exceptions occurred during concurrent export: {exceptions}"
        
        for i in range(num_threads):
            assert os.path.exists(os.path.join(tmpdir, f"out_{i}.mp4"))
            assert os.path.exists(os.path.join(tmpdir, f"audio_{i}.mp3"))
