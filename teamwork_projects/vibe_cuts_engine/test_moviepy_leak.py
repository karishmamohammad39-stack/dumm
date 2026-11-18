import os
import tempfile
import time
from moviepy.editor import ColorClip, AudioClip
import numpy as np

def make_frame(t):
    return [np.sin(440 * 2 * np.pi * t)]

dummy_audio = AudioClip(make_frame, duration=5)
dummy_video = ColorClip(size=(64, 64), color=(255, 0, 0), duration=5)
dummy_video = dummy_video.set_audio(dummy_audio)
dummy_video.fps = 24

def test_leak():
    # simulate exception inside write_videofile
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "output.mp4")
        root, ext = os.path.splitext(out_path)
        tmp_path = f"{root}.1234.tmp{ext}"
        
        try:
            # We'll use a mocked audio write that raises an exception
            original_write = dummy_video.audio.write_audiofile
            def buggy_write(*args, **kwargs):
                original_write(*args, **kwargs)
                raise KeyboardInterrupt("Simulated Ctrl+C")
            
            dummy_video.audio.write_audiofile = buggy_write
            dummy_video.write_videofile(tmp_path, codec="libx264", audio_codec="aac")
        except BaseException:
            # The cleanup block from io.py
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
        
        # Check what files are left
        leftover = os.listdir(tmpdir)
        print("Leftover files:", leftover)

if __name__ == "__main__":
    test_leak()
