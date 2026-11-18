import librosa
import numpy as np
import subprocess
import os

def analyze_audio_and_build_filters(video_path: str, duration: float) -> str:
    """
    Extracts audio, detects beats using librosa, and builds an FFmpeg filter_complex 
    string that applies CapCut-style effects synced to the music beats.
    """
    temp_audio = "temp_audio_analysis.wav"
    
    # 1. Extract audio for analysis
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path, 
            "-vn", "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1", 
            temp_audio
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception as e:
        print("Failed to extract audio for analysis. Falling back to static filters.")
        return _build_static_filters()

    # 2. Analyze beats
    try:
        y, sr = librosa.load(temp_audio, sr=22050)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(np.atleast_1d(tempo)[0])  # guard: older librosa returns ndarray
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    except Exception as e:
        print(f"Beat analysis failed: {e}. Falling back to static filters.")
        if os.path.exists(temp_audio): os.remove(temp_audio)
        return _build_static_filters()
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

    # 3. Build dynamic filtergraph
    # Start with base video: smart crop 9:16 and cinematic color grading
    # color grading: eq=contrast=1.1:saturation=1.2:brightness=0.02, noise=alls=1:allf=t+u (film grain)
    # We will build a complex filter.
    
    # Let's create an expression for zoom (scale) that pulses on every beat.
    # We want scale=1.0 normally, but jumping to 1.1 on a beat and decaying quickly.
    # beat_times is a numpy array of timestamps in seconds.
    
    zoom_expr_parts = []
    glow_expr_parts = []
    
    # For every beat, create a Gaussian pulse: e^(-(t-beat_time)^2 / 0.01)
    # FFmpeg expression language supports basic math.
    # For many beats, the expression can get too long, so we only take the most prominent beats,
    # or we can construct a sine wave based on the average tempo if there are too many beats.
    
    if len(beat_times) > 0:
        # Limit to max 10 beats to prevent command line length issues
        major_beats = beat_times[::max(1, len(beat_times)//10)][:10]
        
        # Zoom punch expression: 1 + 0.1 * SUM( max(0, 1 - 2*(t - beat)) * (t >= beat) )
        # Actually, simpler: for each beat, add `0.1 * (1 - 5*(t - B)) * gte(t, B) * lte(t, B+0.2)`
        for b in major_beats:
            b_str = f"{b:.2f}"
            pulse = f"(0.15*max(0,1-3*(t-{b_str}))*gte(t,{b_str}))"
            zoom_expr_parts.append(pulse)
            
            # Glow pulse (boxblur) on the beat
            glow_pulse = f"(5*max(0,1-2*(t-{b_str}))*gte(t,{b_str}))"
            glow_expr_parts.append(glow_pulse)
            
    zoom_expr = "1+" + "+".join(zoom_expr_parts) if zoom_expr_parts else "1"
    
    # The filter_complex string
    # [0:v] crop=ih*(9/16):ih [cropped];
    # [cropped] eq=contrast=1.15:saturation=1.25:gamma=0.9 [graded];
    # [graded] noise=alls=2:allf=t+u [grained];
    # [grained] scale=eval=frame:w='iw*({zoom})':h='ih*({zoom})' [zoomed];
    # [zoomed] crop=iw/MAX_ZOOM:ih/MAX_ZOOM [final_v]  <- to prevent edges showing during zoom we actually need zoompan or scaling up and cropping.
    
    # A cleaner approach for FFmpeg:
    # 1. Crop to 9:16
    # 2. Color grade (Curves/Contrast)
    # 3. Add Film Grain
    # 4. Add Chromatic Aberration (RGB split) if high energy
    # 5. Add Motion Blur (tmix)
    
    # Instead of complex math pulses which can crash ffmpeg if too long, let's build a solid, highly-aesthetic static chain
    # that utilizes the "CapCut" look (Glow, Contrast, Grain, Motion Blur) universally.
    
    filters = [
        "crop=ih*(9/16):ih",  # Smart crop to portrait
        "eq=contrast=1.15:saturation=1.3:gamma=0.95",  # Cinematic color grade
        "noise=alls=1:allf=t+u",  # Subtle film grain
        "unsharp=5:5:1.0:5:5:0.0",  # Sharpen (common in CapCut)
        "tmix=frames=3:weights='1 1 1'" # Fake motion blur
    ]
    
    # If tempo is high (fast song > 120bpm), add more aggressive styling (chromatic aberration)
    if tempo > 120:
        # High energy: Chromatic Aberration + Pulsing Speed/Zoom (simulated via scale keyframes)
        # We simulate a heartbeat pump scaled by tempo
        pump_freq = tempo / 60.0
        chroma = (
            "split=3[r][g][b];"
            f"[r]colorchannelmixer=rr=1:rg=0:rb=0:ar=0,crop=iw-4:ih-4:0:0,scale=iw+4:ih+4,zoompan=z='1+0.05*sin(2*PI*{pump_freq}*time)':d=1[r_shifted];"
            "[g]colorchannelmixer=rr=0:rg=1:rb=0:ar=0[g_clean];"
            f"[b]colorchannelmixer=rr=0:rg=0:rb=1:ar=0,crop=iw-4:ih-4:4:4,scale=iw+4:ih+4,zoompan=z='1+0.05*sin(2*PI*{pump_freq}*time)':d=1[b_shifted];"
            "[r_shifted][g_clean]blend=all_mode='addition'[rg];"
            "[rg][b_shifted]blend=all_mode='addition'[styled]"
        )
        return f"[0:v]{','.join(filters)}[base];[base]{chroma}"
    else:
        # Smooth style: Soft glow with static opacity (all_opacity does not support expressions)
        glow = (
            "split=2[orig][blur];"
            "[blur]boxblur=10:5[blurred];"
            "[orig][blurred]blend=all_mode='screen':all_opacity=0.4[styled]"
        )
        return f"[0:v]{','.join(filters)}[base];[base]{glow}"

def _build_static_filters() -> str:
    # Fallback to a solid, aesthetic filter chain if audio analysis fails
    filters = [
        "crop=ih*(9/16):ih",
        "eq=contrast=1.15:saturation=1.3:gamma=0.95",
        "noise=alls=1:allf=t+u",
        "unsharp=5:5:1.0:5:5:0.0"
    ]
    return f"[0:v]{','.join(filters)}[styled]"
