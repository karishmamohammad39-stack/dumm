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
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    root, ext = os.path.splitext(path)
    tmp_path = f"{root}.{uuid.uuid4().hex}.tmp{ext}"
    try:
        clip.write_videofile(tmp_path, codec="libx264", audio_codec="aac")
        os.replace(tmp_path, path)
    except BaseException:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise

def extract_audio(video_path: str, output_path: str = None) -> str:
    """
    Extract audio from a video and save it to output_path.
    Returns the path to the saved audio file.
    """
    if VideoFileClip is None:
        raise ImportError("moviepy is required")
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")
    
    video = None
    audio = None
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        if audio is None:
            raise ValueError(f"No audio found in {video_path}")
        
        if output_path is not None:
            output_audio_path = output_path
        else:
            output_audio_path = os.path.join(tempfile.gettempdir(), f"audio_{uuid.uuid4().hex}.mp3")
            
        dir_name = os.path.dirname(output_audio_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        root, ext = os.path.splitext(output_audio_path)
        tmp_path = f"{root}.{uuid.uuid4().hex}.tmp{ext}"
        try:
            audio.write_audiofile(tmp_path)
            os.replace(tmp_path, output_audio_path)
        except BaseException:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            raise
        return output_audio_path
    finally:
        try:
            if audio is not None:
                audio.close()
        finally:
            if video is not None:
                video.close()
