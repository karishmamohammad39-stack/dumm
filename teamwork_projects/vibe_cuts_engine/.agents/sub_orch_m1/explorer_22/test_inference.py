import os
import sys

def mock_moviepy():
    class VideoFileClip:
        def __init__(self, path):
            self.path = path
        def write_videofile(self, filename, **kwargs):
            ext = os.path.splitext(filename)[1]
            if ext == '.tmp':
                raise ValueError("MoviePy couldn't find the codec associated with the filename")
            print(f"Writing to {filename} with ext {ext}")
            
    return VideoFileClip

VideoFileClip = mock_moviepy()

def test_inference():
    clip = VideoFileClip("test.mp4")
    path = "output"
    import uuid
    root, ext = os.path.splitext(path)
    tmp_path = f"{root}.{uuid.uuid4().hex}.tmp{ext}"
    try:
        clip.write_videofile(tmp_path, codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"CRASH: {e}")

test_inference()
