import sys
import os
import glob
from moviepy.editor import ColorClip, AudioClip
import numpy as np
import threading
import time

def make_frame(t):
    return [np.sin(440 * 2 * np.pi * t)]

dummy_audio = AudioClip(make_frame, duration=5)
dummy_video = ColorClip(size=(64, 64), color=(255, 0, 0), duration=5)
dummy_video = dummy_video.set_audio(dummy_audio)
dummy_video.fps = 24

def run_export():
    try:
        dummy_video.write_videofile("test_out.mp4", codec="libx264", audio_codec="aac")
    except BaseException as e:
        print(f"Exception caught: {type(e)}")

# Patch os.replace or something in moviepy to simulate a crash, or just interrupt it
# Instead of interrupting, we can monkeypatch moviepy's audio write to raise KeyboardInterrupt
import moviepy.video.io.VideoFileClip
import moviepy.audio.io.AudioFileClip

original_write = dummy_video.audio.write_audiofile
def mock_write(*args, **kwargs):
    print("Simulating KeyboardInterrupt in write_audiofile")
    raise KeyboardInterrupt()

dummy_video.audio.write_audiofile = mock_write

run_export()

print("Files in dir:")
for f in os.listdir('.'):
    if f.endswith('.mp3') or f.endswith('.mp4'):
        print(f)
