import pytest

def test_speed_curve_and_subtitles(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    speed_vid = engine.apply_speed_curve(vid, {'type': 'constant', 'speed': 2.0})
    aud = engine.extract_audio(speed_vid)
    sub = engine.generate_subtitles(aud)
    assert sub is not None

def test_speed_curve_and_extract_audio(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    speed_vid = engine.apply_speed_curve(vid, {'type': 'bezier', 'points': [(0,1), (1,2)]})
    aud = engine.extract_audio(speed_vid)
    assert aud is not None

def test_masking_and_blend_modes(engine, sample_video):
    vid1 = engine.ingest_video(sample_video)
    vid2 = engine.ingest_video(sample_video)
    masked_vid2 = engine.apply_mask(vid2, 'circle', {'cx': 50, 'cy': 50, 'r': 25})
    blended_vid2 = engine.apply_blend_mode(masked_vid2, 'multiply')
    comp = engine.composite_layers([vid1, blended_vid2])
    assert comp is not None

def test_keyframing_and_masking(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    masked_vid = engine.apply_mask(vid, 'rectangle', {'x': 10, 'y': 10, 'w': 100, 'h': 100})
    keyframed_vid = engine.add_keyframe(masked_vid, 'position', 1.0, (50, 50))
    assert keyframed_vid is not None

def test_keyframing_and_blend_modes(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    blended_vid = engine.apply_blend_mode(vid, 'screen')
    keyframed_vid = engine.add_keyframe(blended_vid, 'opacity', 2.0, 0.5)
    assert keyframed_vid is not None

def test_composite_and_speed_curve(engine, sample_video):
    vid1 = engine.ingest_video(sample_video)
    vid2 = engine.ingest_video(sample_video)
    speed_vid1 = engine.apply_speed_curve(vid1, {'type': 'linear', 'start': 0, 'end': 5})
    comp = engine.composite_layers([speed_vid1, vid2])
    assert comp is not None

def test_composite_and_masking_and_blend(engine, sample_video):
    vid1 = engine.ingest_video(sample_video)
    vid2 = engine.ingest_video(sample_video)
    vid3 = engine.ingest_video(sample_video)
    masked_vid2 = engine.apply_mask(vid2, 'polygon', {'points': [(0,0), (10,0), (5,10)]})
    blended_vid3 = engine.apply_blend_mode(vid3, 'overlay')
    comp = engine.composite_layers([vid1, masked_vid2, blended_vid3])
    assert comp is not None

def test_subtitles_and_composite(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    aud = engine.extract_audio(vid)
    sub = engine.generate_subtitles(aud)
    comp = engine.composite_layers([vid, sub])
    assert comp is not None

def test_keyframed_speed_curve(engine, sample_video):
    # Depending on API, speed curve itself might have keyframes, or we apply keyframes on a sped-up video
    vid = engine.ingest_video(sample_video)
    speed_vid = engine.apply_speed_curve(vid, {'type': 'constant', 'speed': 1.5})
    keyframed_vid = engine.add_keyframe(speed_vid, 'scale', 1.0, 2.0)
    assert keyframed_vid is not None

def test_audio_extract_from_composited_video(engine, sample_video):
    vid1 = engine.ingest_video(sample_video)
    vid2 = engine.ingest_video(sample_video)
    comp = engine.composite_layers([vid1, vid2])
    aud = engine.extract_audio(comp)
    assert aud is not None

def test_masking_over_subtitles(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    aud = engine.extract_audio(vid)
    sub = engine.generate_subtitles(aud)
    masked_sub = engine.apply_mask(sub, 'rectangle', {'x': 0, 'y': 80, 'w': 100, 'h': 20})
    comp = engine.composite_layers([vid, masked_sub])
    assert comp is not None

def test_blend_mode_on_speed_ramped_clip(engine, sample_video):
    vid = engine.ingest_video(sample_video)
    speed_vid = engine.apply_speed_curve(vid, {'type': 'bezier', 'points': [(0,1), (1,2)]})
    blended_vid = engine.apply_blend_mode(speed_vid, 'darken')
    assert blended_vid is not None
