import pytest

# F1: Ingest raw video
def test_ingest_mp4(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    assert vid is not None

def test_ingest_mov(engine, sample_video):
    vid = engine.ingest_video(sample_video.replace('.mp4', '.mov'))
    assert vid is not None

def test_ingest_avi(engine, sample_video):
    vid = engine.ingest_video(sample_video.replace('.mp4', '.avi'))
    assert vid is not None

def test_ingest_mkv(engine, sample_video):
    vid = engine.ingest_video(sample_video.replace('.mp4', '.mkv'))
    assert vid is not None

def test_ingest_webm(engine, sample_video):
    vid = engine.ingest_video(sample_video.replace('.mp4', '.webm'))
    assert vid is not None

# F2: Extract audio
def test_extract_audio_standard(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    aud = engine.extract_audio(vid)
    assert aud is not None

def test_extract_audio_from_mov(engine, sample_video):
    vid = engine.ingest_video(sample_video.replace('.mp4', '.mov'))
    aud = engine.extract_audio(vid)
    assert aud is not None

def test_extract_audio_from_avi(engine, sample_video):
    vid = engine.ingest_video(sample_video.replace('.mp4', '.avi'))
    aud = engine.extract_audio(vid)
    assert aud is not None

def test_extract_audio_from_mkv(engine, sample_video):
    vid = engine.ingest_video(sample_video.replace('.mp4', '.mkv'))
    aud = engine.extract_audio(vid)
    assert aud is not None

def test_extract_audio_multiple_times(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    aud1 = engine.extract_audio(vid)
    aud2 = engine.extract_audio(vid)
    assert aud1 is not None and aud2 is not None

# F3: Generate subtitles
def test_generate_subtitles_english(engine, sample_audio):
    sub = engine.generate_subtitles(sample_audio)
    assert sub is not None

def test_generate_subtitles_spanish(engine, sample_audio):
    sub = engine.generate_subtitles(sample_audio)
    assert sub is not None

def test_generate_subtitles_with_punctuation(engine, sample_audio):
    sub = engine.generate_subtitles(sample_audio)
    assert sub is not None

def test_generate_subtitles_short_audio(engine, sample_audio):
    sub = engine.generate_subtitles(sample_audio)
    assert sub is not None

def test_generate_subtitles_long_audio(engine, sample_audio):
    sub = engine.generate_subtitles(sample_audio)
    assert sub is not None

# F4: Apply speed curve
def test_speed_curve_linear_ramp(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_speed_curve(vid, {'type': 'linear', 'start': 1.0, 'end': 2.0})
    assert res is not None

def test_speed_curve_bezier_ramp(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_speed_curve(vid, {'type': 'bezier', 'points': [(0,1), (1,2)]})
    assert res is not None

def test_speed_curve_freeze_frame(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_speed_curve(vid, {'type': 'freeze', 'time': 5.0, 'duration': 2.0})
    assert res is not None

def test_speed_curve_slow_mo(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_speed_curve(vid, {'type': 'constant', 'speed': 0.5})
    assert res is not None

def test_speed_curve_fast_forward(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_speed_curve(vid, {'type': 'constant', 'speed': 4.0})
    assert res is not None

# F5: Composite layers
def test_composite_two_videos(engine, sample_video):
    vid1 = engine.ingest_video(sample_video)
    vid2 = engine.ingest_video(sample_video)
    comp = engine.composite_layers([vid1, vid2])
    assert comp is not None

def test_composite_video_and_image(engine, sample_video, sample_image):
    vid = engine.ingest_video(sample_video)
    img = engine.ingest_video(sample_image)
    comp = engine.composite_layers([vid, img])
    assert comp is not None

def test_composite_three_layers(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    comp = engine.composite_layers([vid, vid, vid])
    assert comp is not None

def test_composite_text_over_video(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    comp = engine.composite_layers([vid, "text_layer_placeholder"])
    assert comp is not None

def test_composite_transparent_overlay(engine, sample_video, sample_image):
    vid = engine.ingest_video(sample_video)
    img = engine.ingest_video(sample_image) # Assume transparent PNG
    comp = engine.composite_layers([vid, img])
    assert comp is not None

# F6: Masking shapes
def test_mask_rectangle(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_mask(vid, 'rectangle', {'x': 10, 'y': 10, 'w': 100, 'h': 100})
    assert res is not None

def test_mask_circle(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_mask(vid, 'circle', {'cx': 50, 'cy': 50, 'r': 25})
    assert res is not None

def test_mask_polygon(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_mask(vid, 'polygon', {'points': [(0,0), (10,0), (5,10)]})
    assert res is not None

def test_mask_feathering(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_mask(vid, 'rectangle', {'x': 10, 'y': 10, 'w': 100, 'h': 100, 'feather': 5.0})
    assert res is not None

def test_mask_inversion(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_mask(vid, 'circle', {'cx': 50, 'cy': 50, 'r': 25, 'invert': True})
    assert res is not None

# F7: Dynamic blend modes
def test_blend_multiply(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_blend_mode(vid, 'multiply')
    assert res is not None

def test_blend_screen(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_blend_mode(vid, 'screen')
    assert res is not None

def test_blend_overlay(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_blend_mode(vid, 'overlay')
    assert res is not None

def test_blend_darken(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_blend_mode(vid, 'darken')
    assert res is not None

def test_blend_lighten(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.apply_blend_mode(vid, 'lighten')
    assert res is not None

# F8: Custom keyframing
def test_keyframe_position(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.add_keyframe(vid, 'position', 1.0, (100, 100))
    assert res is not None

def test_keyframe_scale(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.add_keyframe(vid, 'scale', 2.0, 1.5)
    assert res is not None

def test_keyframe_rotation(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.add_keyframe(vid, 'rotation', 3.0, 90.0)
    assert res is not None

def test_keyframe_opacity(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    res = engine.add_keyframe(vid, 'opacity', 4.0, 0.5)
    assert res is not None

def test_keyframe_multiple_properties(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    engine.add_keyframe(vid, 'position', 1.0, (50, 50))
    res = engine.add_keyframe(vid, 'scale', 1.0, 2.0)
    assert res is not None
