import os
import tempfile
import uuid

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    # Fallback for moviepy 2.0+ or different structures if needed
    try:
        from moviepy import VideoFileClip
    except ImportError:
        VideoFileClip = None

def load_video(path: str):
    """
    Load a video file from the given path.
    """
    if VideoFileClip is None:
        raise ImportError("moviepy is required")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Video file not found at {path}")
    return VideoFileClip(path)

def export_video(clip, path: str) -> None:
    """
    Export the given video clip to the specified path.
    The caller is responsible for managing the clip's lifecycle and closing it.
    """
    root, ext = os.path.splitext(path)
    if not ext or ext == ".":
        ext = ".mp4"
        path = f"{root}{ext}"
        
    if hasattr(clip, 'filename') and clip.filename:
        if os.path.abspath(clip.filename) == os.path.abspath(path):
            raise ValueError("Output path cannot be the same as input path.")
            
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    with tempfile.TemporaryDirectory(dir=dir_name or '.') as temp_dir:
        tmp_path = os.path.join(temp_dir, f"temp{ext}")
        clip.write_videofile(tmp_path, codec="libx264", audio_codec="aac")
        os.replace(tmp_path, path)

def extract_audio(video_path: str, output_path: str = None) -> str:
    """
    Extract audio from a video and save it to output_path.
    Returns the path to the saved audio file.
    """
    if VideoFileClip is None:
        raise ImportError("moviepy is required")
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")
    
    if output_path is not None:
        output_audio_path = output_path
        root, ext = os.path.splitext(output_audio_path)
        if not ext or ext == ".":
            ext = ".mp3"
            output_audio_path = f"{root}{ext}"
    else:
        ext = ".mp3"
        output_audio_path = os.path.join(tempfile.gettempdir(), f"audio_{uuid.uuid4().hex}.mp3")
        
    if os.path.abspath(video_path) == os.path.abspath(output_audio_path):
        raise ValueError("Output path cannot be the same as input path.")
        
    video = None
    audio = None
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        if audio is None:
            raise ValueError(f"No audio found in {video_path}")
        
        dir_name = os.path.dirname(output_audio_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        with tempfile.TemporaryDirectory(dir=dir_name or '.') as temp_dir:
            tmp_path = os.path.join(temp_dir, f"temp{ext}")
            audio.write_audiofile(tmp_path)
            os.replace(tmp_path, output_audio_path)
            
        return output_audio_path
    finally:
        try:
            if audio is not None:
                audio.close()
        finally:
            if video is not None:
                video.close()
