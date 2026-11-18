import os
import ffmpeg
import subprocess
from typing import Optional
from whisper_model import get_whisper_model
from director import analyze_audio_and_build_filters


def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp format HH:MM:SS,mmm"""
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_srt(segments: list, srt_path: str):
    """Generate an SRT file from Whisper segments"""
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")


def cut_video(video_path: str, start: float, end: float, output_path: str):
    """Cut a segment from a video file."""
    try:
        (
            ffmpeg
            .input(video_path, ss=start, to=end)
            .output(output_path, c="copy")
            .run(overwrite_output=True, quiet=True)
        )
    except ffmpeg.Error as e:
        print("FFmpeg Cut Error:", e.stderr.decode() if e.stderr else "")
        raise


def transcribe_only(video_path: str, start: float = 0.0, end: Optional[float] = None) -> list:
    """
    Transcribe audio from a video (optionally a slice). Returns list of segment dicts.
    """
    model = get_whisper_model()
    target_path = video_path
    temp_cut = None

    if start > 0 or (end is not None and end > 0):
        base_dir = os.path.dirname(video_path)
        name, ext = os.path.splitext(os.path.basename(video_path))
        temp_cut = os.path.join(base_dir, f"{name}_txcut{ext}")
        _end = end if end else 9999999
        cut_video(video_path, start, _end, temp_cut)
        target_path = temp_cut

    print("Transcribing with shared Whisper model...")
    result = model.transcribe(target_path)

    # Offset segment timestamps if we cut from a non-zero start
    offset = start if start > 0 else 0.0
    segments = [
        {
            "id": i,
            "start": round(seg["start"] + offset, 3),
            "end": round(seg["end"] + offset, 3),
            "text": seg["text"].strip(),
        }
        for i, seg in enumerate(result.get("segments", []))
    ]

    if temp_cut and os.path.exists(temp_cut):
        try:
            os.remove(temp_cut)
        except Exception:
            pass

    return segments


def process_video(video_path: str, start: float, end: float, caption_style: str) -> str:
    """
    Core processing loop:
    1. Cut the video segment.
    2. Transcribe the segment using Whisper.
    3. Burn the generated subtitles onto the video with robust Windows path escaping.
    """
    model = get_whisper_model()
    base_dir = os.path.dirname(video_path)
    filename = os.path.basename(video_path)
    name, ext = os.path.splitext(filename)
    
    cut_path = os.path.join(base_dir, f"{name}_cut{ext}")
    srt_path = os.path.join(base_dir, f"{name}_cut.srt")
    final_path = os.path.join(base_dir, f"{name}_final{ext}")

    print(f"1. Cutting video from {start} to {end}...")
    try:
        (
            ffmpeg
            .input(video_path, ss=start, to=end)
            .output(cut_path, c="copy")
            .run(overwrite_output=True, quiet=True)
        )
    except ffmpeg.Error as e:
        print("FFmpeg Error Output:", e.stderr.decode() if e.stderr else "")
        raise e

    print("2. Transcribing audio...")
    result = model.transcribe(cut_path)
    generate_srt(result.get("segments", []), srt_path)

    print("3. Analyzing audio for AI Director effects...")
    base_filter_complex = analyze_audio_and_build_filters(cut_path, end - start)

    print("4. Burning subtitles onto video...")
    
    # Fully escape Windows path delimiters (both forward slashes and colons: C\:/path)
    abs_srt = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")
    
    style = caption_style if caption_style else "FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,MarginV=50"
    
    try:
        # Append subtitles filter to the AI Director graph output
        final_filter_complex = f"{base_filter_complex};[styled]subtitles='{abs_srt}':force_style='{style}'[outv];[0:a]loudnorm[outa]"
        
        cmd = [
            "ffmpeg", "-y", "-i", cut_path,
            "-filter_complex", final_filter_complex,
            "-map", "[outv]", "-map", "[outa]",
            "-vcodec", "libx264", "-acodec", "aac",
            final_path
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
    except subprocess.CalledProcessError as e:
        print("FFmpeg Filter Error Output:", e.stderr.decode() if e.stderr else "")
        # Graceful fallback: render cut video with standard subtitles without complex filter if needed
        fallback_cmd = [
            "ffmpeg", "-y", "-i", cut_path,
            "-vf", f"subtitles='{abs_srt}':force_style='{style}'",
            "-c:v", "libx264", "-c:a", "aac",
            final_path
        ]
        subprocess.run(fallback_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Processing complete! Saved to {final_path}")
    return final_path
