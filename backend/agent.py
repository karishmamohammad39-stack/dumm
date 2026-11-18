import os
import json
from typing import Dict, Any

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

def generate_editing_plan(video_path: str, transcript_data: list, user_prompt: str, sector: str, rules: dict) -> Dict[str, Any]:
    """
    Pillar 2: Agentic Logic Controller
    Acts as the "Brain". Cross-references the video, transcript, and rules to generate an execution plan.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "DUMMY_KEY")
    
    if HAS_GENAI and api_key != "DUMMY_KEY":
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            system_prompt = f"""
            You are an expert AI Video Editor. Your task is to output a strictly formatted JSON Editing Plan.
            
            Target Platform (Sector): {sector}
            User Request: {user_prompt}
            
            Current Trend Rules:
            - Rhythm: {rules.get('rhythm', 'fast')}
            - Auto-Zooms: {rules.get('auto_zooms', 'frequent')}
            - Captions: {rules.get('caption_style', 'kinetic')}
            
            Given the transcript, select the best timestamps to keep, and where to place B-Roll and SFX.
            
            JSON Format requirement:
            {{
              "clips": [
                {{"start": 0.0, "end": 5.0, "type": "talking_head"}},
                {{"start": 10.0, "end": 15.0, "type": "b_roll", "b_roll_keyword": "technology"}},
                {{"start": 15.0, "end": 17.0, "type": "speed_ramp", "speed_multiplier": 2.0}}
              ],
              "music_mood": "high_energy",
              "color_lut": "vibrant",
              "auto_zooms": [0.5, 3.2],
              "transitions": "xfade",
              "glitch_timestamps": [1.5, 4.2]
            }}
            """
            
            response = model.generate_content([
                system_prompt,
                f"Transcript: {json.dumps(transcript_data)}"
            ])
            
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text.strip())
        except Exception as e:
            print(f"Gemini generation notice ({e}), building dynamic transcript plan...")

    return _build_dynamic_transcript_plan(transcript_data, sector)


def _build_dynamic_transcript_plan(transcript_data: list, sector: str) -> Dict[str, Any]:
    """
    Builds a dynamic editing plan derived directly from actual Whisper transcript timestamps.
    """
    clips = []
    if transcript_data and len(transcript_data) > 0:
        for i, seg in enumerate(transcript_data[:6]):
            s_time = float(seg.get("start", 0.0))
            e_time = float(seg.get("end", s_time + 3.0))
            if e_time <= s_time:
                e_time = s_time + 2.5
            
            clip_type = "talking_head" if i % 2 == 0 else "speed_ramp"
            clips.append({
                "start": round(s_time, 2),
                "end": round(e_time, 2),
                "type": clip_type,
                "speed_multiplier": 1.5 if clip_type == "speed_ramp" else 1.0,
                "apply_zoom": (i % 2 == 1)
            })
    else:
        clips = [
            {"start": 0.0, "end": 4.0, "type": "talking_head", "apply_zoom": True},
            {"start": 4.0, "end": 7.5, "type": "speed_ramp", "speed_multiplier": 1.5},
            {"start": 7.5, "end": 11.0, "type": "talking_head", "apply_zoom": False}
        ]

    plan = {
        "clips": clips,
        "music_mood": "high_energy" if sector == "reels" else "cinematic",
        "color_lut": "vibrant" if sector == "reels" else "warm",
        "auto_zooms": [c["start"] + 0.5 for c in clips if c.get("apply_zoom")],
        "transitions": "xfade",
        "glitch_timestamps": [c["start"] for c in clips[1:]]
    }
    return plan
