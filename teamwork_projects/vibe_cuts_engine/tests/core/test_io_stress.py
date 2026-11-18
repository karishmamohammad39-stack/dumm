import os
import tempfile
import threading
import time
import pytest
from src.core.io import load_video, export_video, extract_audio

try:
    from moviepy.editor import ColorClip, AudioClip
    import numpy as np
except ImportError:
    pass

def generate_video(duration=1, fps=24, size=(64, 64), path="temp.mp4"):
    def make_frame(t):
        return [np.sin(440 * 2 * np.pi * t)]
    clip = ColorClip(size=size, color=(255, 0, 0), duration=duration)
    clip = clip.set_audio(AudioClip(make_frame, duration=duration))
    clip.fps = fps
    clip.write_videofile(path, codec="libx264", audio_codec="aac", fps=fps, logger=None)
    clip.close()
    return path

def test_stress_export_video():
    # Stress testing export_video under concurrent load
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mp4")
        generate_video(duration=2, path=input_path)
        
        exceptions = []
        
        def worker(idx):
            try:
                clip = load_video(input_path)
                out_path = os.path.join(tmpdir, f"out_{idx}.mp4")
                export_video(clip, out_path)
                clip.close()
                assert os.path.exists(out_path)
            except Exception as e:
                exceptions.append(e)
                
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        assert len(exceptions) == 0, f"Exceptions occurred during concurrent export: {exceptions}"

def test_stress_extract_audio():
    # Stress testing extract_audio under concurrent load
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mp4")
        generate_video(duration=2, path=input_path)
        
        exceptions = []
        
        def worker(idx):
            try:
                out_path = os.path.join(tmpdir, f"audio_{idx}.mp3")
                extract_audio(input_path, out_path)
                assert os.path.exists(out_path)
            except Exception as e:
                exceptions.append(e)
                
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        assert len(exceptions) == 0, f"Exceptions occurred during concurrent extract: {exceptions}"

def test_oracle_extract_audio():
    # Oracle test to verify audio is successfully extracted and of expected duration
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mp4")
        generate_video(duration=3, path=input_path)
        
        out_path = os.path.join(tmpdir, "audio.mp3")
        start = time.time()
        extracted_path = extract_audio(input_path, out_path)
        duration = time.time() - start
        
        assert extracted_path == out_path
        assert os.path.exists(out_path)
        assert os.path.getsize(out_path) > 0

        # Verify the extracted file can be loaded
        from moviepy.editor import AudioFileClip
        audio = AudioFileClip(out_path)
        assert abs(audio.duration - 3.0) < 0.5
        audio.close()
