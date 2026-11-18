import os
import json
import shutil
import subprocess
import uuid
import requests
from whisper_model import get_whisper_model
from vision import track_face_and_crop, detect_scene_cuts


def get_broll(keyword: str, output_path: str, duration: float = 3.0):
    """
    Subsystem 4: Auto B-Roll Generation
    Synthesizes a branded high-energy visual B-Roll segment matching the keyword.
    """
    print(f"Generating B-roll overlay for keyword: {keyword} ({duration}s)")
    # Generate an aesthetic animated motion background using FFmpeg color & testsrc
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x0f172a:s=1080x1920:d={duration}",
        "-vf", f"drawtext=text='[ B-ROLL: {keyword.upper()} ]':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264", "-preset", "ultrafast",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"B-roll generation notice: {e}")


def generate_kinetic_ass(segments: list, ass_path: str, sector: str):
    """
    Subsystem 2: Kinetic Captions with Animation (\t pop-ins)
    """
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,3,0,2,10,10,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for seg in segments:
            words = seg.get("words", [])
            if not words:
                # If word timestamps not extracted, use whole segment
                start = _ass_time(seg["start"])
                end = _ass_time(seg["end"])
                text = seg["text"].strip()
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{{\\c&H00FFFF&}}{text}{{\\r}}\n")
                continue

            for i, word in enumerate(words):
                start = _ass_time(word["start"])
                end = _ass_time(word["end"])
                
                line_text = ""
                for j, w in enumerate(words):
                    text = w["word"].strip()
                    if i == j:
                        # Pop-in highlight animation
                        line_text += f"{{\\c&H00FFFF&\\fscx120\\fscy120\\t(\\fscx100\\fscy100)}}{text}{{\\r}} "
                    else:
                        line_text += f"{text} "
                        
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{line_text.strip()}\n")


def _ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def execute_editing_plan(video_path: str, plan: dict, sector: str) -> str:
    """
    Pillar 3: Execution Engine
    Executes the 5 Automated Effect Categories based on the JSON plan.
    """
    model = get_whisper_model()
    base_dir = os.path.dirname(video_path)
    job_id = str(uuid.uuid4())[:8]
    final_output = os.path.join(base_dir, f"{job_id}_final.mp4")

    clips = plan.get("clips", [])

    # If no clips were planned (e.g. silent video), fall back to scene-cut boundaries
    if not clips:
        scene_cuts = detect_scene_cuts(video_path)
        if len(scene_cuts) >= 2:
            clips = [{"start": scene_cuts[i], "end": scene_cuts[i + 1], "type": "talking_head", "apply_zoom": False}
                     for i in range(min(len(scene_cuts) - 1, 6))]
        else:
            raise ValueError("No clips found in editing plan and no scene cuts detected.")

    concat_file = os.path.join(base_dir, f"{job_id}_concat.txt")
    clip_files = []

    for i, clip in enumerate(clips):
        clip_out = os.path.join(base_dir, f"{job_id}_clip_{i}.mp4")
        start = clip["start"]
        end = clip["end"]
        clip_type = clip.get("type", "talking_head")

        # ── B-Roll: generate a keyword placeholder if no real b-roll source ──
        if clip_type == "b_roll":
            keyword = clip.get("b_roll_keyword", "highlight")
            dur = max(0.5, end - start)
            get_broll(keyword, clip_out, duration=dur)
            clip_files.append(clip_out)
            continue

        vf_chain = []
        af_chain = []

        if sector == "reels":
            vf_chain.append(track_face_and_crop(video_path, target_aspect=9/16))

        mood = plan.get("color_lut", "vibrant")
        if mood == "vibrant":
            vf_chain.append("eq=contrast=1.15:saturation=1.3:gamma=0.95")

        vf_chain.append("vignette=PI/4")

        if clip_type == "speed_ramp":
            speed = clip.get("speed_multiplier", 2.0)
            vf_chain.append(f"setpts={1.0/speed}*PTS")
            af_chain.append(f"atempo={min(speed, 2.0)}")  # atempo max is 2.0 per filter

        if clip.get("apply_zoom", False):
            vf_chain.append("zoompan=z='min(zoom+0.0015,1.15)':d=1")

        vf_str = ",".join(vf_chain) if vf_chain else "null"
        af_str = ",".join(af_chain) if af_chain else "anull"

        cmd = [
            "ffmpeg", "-y", "-ss", str(start), "-to", str(end),
            "-i", video_path,
            "-vf", vf_str, "-af", af_str,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac",
            clip_out
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        clip_files.append(clip_out)

    concat_out = os.path.join(base_dir, f"{job_id}_concat.mp4")
    # P0 fix: write absolute paths so FFmpeg can find the files regardless of CWD
    with open(concat_file, "w") as f:
        for cf in clip_files:
            f.write(f"file '{os.path.abspath(cf)}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
        "-c", "copy", concat_out
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    print("Generating Kinetic Captions...")
    transcription = model.transcribe(concat_out, word_timestamps=True)
    ass_path = os.path.join(base_dir, f"{job_id}_subs.ass")
    generate_kinetic_ass(transcription.get("segments", []), ass_path, sector)

    print("Applying Final Master FX Chain...")
    abs_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")

    final_v_filter = f"[0:v]ass='{abs_ass}'[v_out]"
    final_a_filter = "[0:a]loudnorm[a_out]"

    cmd_final = [
        "ffmpeg", "-y", "-i", concat_out,
        "-filter_complex", f"{final_v_filter};{final_a_filter}",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "aac",
        final_output
    ]

    try:
        subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # Fallback if ASS filter fails (e.g. no libass on this system)
        shutil.copyfile(concat_out, final_output)

    for f in clip_files + [concat_file, concat_out, ass_path]:
        try:
            os.remove(f)
        except Exception:
            pass

    return final_output

