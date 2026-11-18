from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import uuid
import json
import subprocess
from typing import Optional
from processor import process_video, transcribe_only
from agent import generate_editing_plan
from scout import get_current_rules
from agentic_processor import execute_editing_plan

app = FastAPI(title="Vibe-Cuts API")

# CORS must be added BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_processing"
os.makedirs(TEMP_DIR, exist_ok=True)


def cleanup_files(paths: list[str]):
    for path in paths:
        if path and os.path.exists(path):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
            except Exception as e:
                print(f"Error cleaning up {path}: {e}")


def has_audio_stream(file_path: str) -> bool:
    try:
        res = subprocess.run([
            "ffprobe", "-i", file_path,
            "-show_streams", "-select_streams", "a",
            "-loglevel", "error"
        ], capture_output=True, text=True)
        return bool(res.stdout.strip())
    except Exception:
        return False


@app.get("/")
def redirect_to_ui():
    return RedirectResponse(url="/ui/")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    trim_start: float = Form(...),
    trim_end: float = Form(...),
    caption_style: str = Form(default=""),
):
    """
    Receive a video, cut it, transcribe it (Whisper), and burn subtitles.
    Returns the processed video file.
    """
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    input_path = os.path.join(TEMP_DIR, f"{job_id}{ext}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    print(f"Received job {job_id} for file {video.filename}")

    try:
        final_path = process_video(
            video_path=input_path,
            start=trim_start,
            end=trim_end,
            caption_style=caption_style,
        )

        intermediate_files = [
            input_path,
            input_path.replace(ext, f"_cut{ext}"),
            input_path.replace(ext, "_cut.srt"),
        ]
        background_tasks.add_task(cleanup_files, intermediate_files)

        return FileResponse(
            path=final_path,
            filename=f"reel_{video.filename}",
            media_type="video/mp4",
        )

    except Exception as e:
        cleanup_files([input_path])
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/transcribe")
async def transcribe_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    trim_start: float = Form(default=0.0),
    trim_end: float = Form(default=0.0),
):
    """
    Transcribe a video using Whisper. Returns caption segments as JSON.
    Does NOT burn subtitles or produce a video file.
    """
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    input_path = os.path.join(TEMP_DIR, f"{job_id}{ext}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    try:
        start = trim_start if trim_start > 0 else 0.0
        end = trim_end if trim_end > 0 else None
        segments = transcribe_only(input_path, start=start, end=end)
        background_tasks.add_task(cleanup_files, [input_path])
        return JSONResponse(content={"segments": segments})

    except Exception as e:
        cleanup_files([input_path])
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/agentic-edit")
async def agentic_edit_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    prompt: str = Form(default="Make a fast-paced viral reel"),
    sector: str = Form(default="reels")
):
    """
    The 4-Pillar Architecture Endpoint.
    1. Scout gets current trends.
    2. Transcription (multimodal mock).
    3. Agentic Logic Controller generates plan.
    4. Execution Engine processes video.
    """
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    input_path = os.path.join(TEMP_DIR, f"{job_id}_raw{ext}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    print(f"Agentic Edit Job {job_id} started for {video.filename}...")

    try:
        rules = get_current_rules()
        transcript_data = transcribe_only(input_path)
        plan = generate_editing_plan(input_path, transcript_data, prompt, sector, rules)
        print("Generated Editing Plan:", plan)
        final_video_path = execute_editing_plan(input_path, plan, sector)

        background_tasks.add_task(cleanup_files, [input_path, final_video_path])

        return FileResponse(
            path=final_video_path,
            filename=f"ai_edited_{video.filename}",
            media_type="video/mp4",
        )

    except Exception as e:
        cleanup_files([input_path])
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/export-reel")
async def export_reel(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    clips: str = Form(default="[]"),
    cinematic_mode: bool = Form(default=False),
    aspect_ratio: str = Form(default="16:9"),
    exposure: float = Form(default=0.0),
    contrast: float = Form(default=0.0),
    saturation: float = Form(default=0.0),
    bgm: Optional[UploadFile] = File(None),
):
    """
    High-performance native FFmpeg export engine.
    Handles ANY video size (100MB, 3GB, 10GB+) via streaming disk I/O.
    """
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    input_path = os.path.join(TEMP_DIR, f"{job_id}_raw{ext}")
    temp_files = [input_path]

    print(f"Export-Reel job {job_id} started for {video.filename}...")

    # Stream video to disk in 1MB chunks (supports 10GB+ without memory spike)
    with open(input_path, "wb") as buffer:
        while chunk := await video.read(1024 * 1024):
            buffer.write(chunk)

    bgm_path = None
    if bgm and bgm.filename:
        bext = os.path.splitext(bgm.filename)[1] or ".mp3"
        bgm_path = os.path.join(TEMP_DIR, f"{job_id}_bgm{bext}")
        temp_files.append(bgm_path)
        with open(bgm_path, "wb") as buffer:
            while chunk := await bgm.read(1024 * 1024):
                buffer.write(chunk)

    try:
        parsed_clips = json.loads(clips)
    except Exception:
        parsed_clips = []

    try:
        # Build video filters based on options
        vf_filters = []
        if cinematic_mode:
            vf_filters.append("crop=ih*(9/16):ih,scale=1080:1920")
        elif aspect_ratio == "9:16":
            vf_filters.append("crop=ih*(9/16):ih,scale=1080:1920")
        elif aspect_ratio == "1:1":
            vf_filters.append("crop=min(iw\\,ih):min(iw\\,ih),scale=1080:1080")
        elif aspect_ratio == "4:5":
            vf_filters.append("crop=ih*(4/5):ih,scale=1080:1350")

        if exposure != 0.0 or contrast != 0.0 or saturation != 0.0:
            b = (exposure / 100.0) * 0.5
            c = 1.0 + (contrast / 100.0) * 0.8
            s = 1.0 + (saturation / 100.0) * 0.8
            vf_filters.append(f"eq=brightness={b:.2f}:contrast={c:.2f}:saturation={s:.2f}")

        vf_args = ["-vf", ",".join(vf_filters)] if vf_filters else []

        clip_files = []
        # Cut each clip using fast seeking (-ss before -i)
        if parsed_clips:
            for idx, c in enumerate(parsed_clips):
                start = max(0.0, float(c.get("start", 0.0)))
                end = float(c.get("end", start + 3.0))
                dur = max(0.2, end - start)
                clip_out = os.path.join(TEMP_DIR, f"{job_id}_clip_{idx}.mp4")
                temp_files.append(clip_out)

                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.3f}",
                    "-t", f"{dur:.3f}",
                    "-i", input_path,
                    *vf_args,
                    "-c:v", "libx264",
                    "-preset", "veryfast",
                    "-crf", "23",
                    "-c:a", "aac",
                    "-pix_fmt", "yuv420p",
                    clip_out
                ]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0 and os.path.exists(clip_out):
                    clip_files.append(clip_out)
                else:
                    print(f"Clip {idx} warning:", res.stderr[-200:] if res.stderr else "")

        # If no clips or clips failed, process whole video / single cut
        if not clip_files:
            whole_clip = os.path.join(TEMP_DIR, f"{job_id}_whole.mp4")
            temp_files.append(whole_clip)
            cmd = [
                "ffmpeg", "-y",
                "-i", input_path,
                *vf_args,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                whole_clip
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            clip_files.append(whole_clip)

        # Concatenate clips
        joined_path = os.path.join(TEMP_DIR, f"{job_id}_joined.mp4")
        temp_files.append(joined_path)
        if len(clip_files) == 1:
            joined_path = clip_files[0]
        else:
            concat_txt = os.path.join(TEMP_DIR, f"{job_id}_concat.txt")
            temp_files.append(concat_txt)
            with open(concat_txt, "w", encoding="utf-8") as f:
                for cf in clip_files:
                    f.write(f"file '{os.path.abspath(cf)}'\n")
            cmd_concat = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_txt,
                "-c", "copy",
                joined_path
            ]
            subprocess.run(cmd_concat, check=True, capture_output=True)

        final_path = joined_path

        # Mix BGM if provided
        if bgm_path and os.path.exists(bgm_path):
            bgm_mixed_path = os.path.join(TEMP_DIR, f"{job_id}_final_bgm.mp4")
            temp_files.append(bgm_mixed_path)

            has_audio = has_audio_stream(joined_path)
            if has_audio:
                mix_cmd = [
                    "ffmpeg", "-y",
                    "-i", joined_path,
                    "-i", bgm_path,
                    "-filter_complex", "[0:a][1:a]amix=inputs=2:weights='1 0.4':duration=first[aout]",
                    "-map", "0:v",
                    "-map", "[aout]",
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-shortest",
                    bgm_mixed_path
                ]
            else:
                mix_cmd = [
                    "ffmpeg", "-y",
                    "-i", joined_path,
                    "-i", bgm_path,
                    "-map", "0:v",
                    "-map", "1:a",
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-shortest",
                    bgm_mixed_path
                ]
            res = subprocess.run(mix_cmd, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(bgm_mixed_path):
                final_path = bgm_mixed_path

        background_tasks.add_task(cleanup_files, temp_files)

        return FileResponse(
            path=final_path,
            filename=f"vibe_cuts_export_{video.filename}",
            media_type="video/mp4",
        )

    except Exception as e:
        cleanup_files(temp_files)
        print("Export reel error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})


# Mount static UI AFTER API routes so API routes take precedence
if os.path.isdir("static"):
    app.mount("/ui", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
