import pytest

def test_tiktok_style_auto_captioned_edit(engine, sample_video):
    # F1, F2, F3
    # 1. Ingest raw video
    vid = engine.ingest_video(sample_video)
    # 2. Extract audio
    aud = engine.extract_audio(vid)
    # 3. Generate subtitles
    sub = engine.generate_subtitles(aud)
    # Composite to ensure it renders correctly
    comp = engine.composite_layers([vid, sub])
    # Export
    engine.export(comp, 'tiktok_out.mp4')
    assert comp is not None

def test_speed_ramped_action_montage(engine, sample_video):
    # F1, F2, F4
    vid1 = engine.ingest_video(sample_video)
    vid2 = engine.ingest_video(sample_video)
    
    speed_vid1 = engine.apply_speed_curve(vid1, {'type': 'bezier', 'points': [(0, 1), (0.5, 3), (1, 1)]})
    speed_vid2 = engine.apply_speed_curve(vid2, {'type': 'linear', 'start': 0.5, 'end': 2.0})
    
    comp = engine.composite_layers([speed_vid1, speed_vid2])
    aud = engine.extract_audio(comp)
    
    engine.export(comp, 'montage_out.mp4')
    assert aud is not None

def test_complex_intro_with_masked_text_and_blend(engine, sample_video, sample_image):
    # F1, F5, F6, F7, F8
    bg_vid = engine.ingest_video(sample_video)
    overlay_img = engine.ingest_video(sample_image)
    
    # Masking
    masked_img = engine.apply_mask(overlay_img, 'polygon', {'points': [(0,0), (100,0), (50,100)]})
    # Blending
    blended_img = engine.apply_blend_mode(masked_img, 'screen')
    # Keyframing
    kf_img = engine.add_keyframe(blended_img, 'position', 0.0, (0, 0))
    kf_img = engine.add_keyframe(kf_img, 'position', 5.0, (100, 100))
    
    comp = engine.composite_layers([bg_vid, kf_img])
    engine.export(comp, 'intro_out.mp4')
    assert comp is not None

def test_picture_in_picture_stream_highlights(engine, sample_video):
    # F1, F5, F8
    main_gameplay = engine.ingest_video(sample_video)
    face_cam = engine.ingest_video(sample_video)
    
    # Keyframing face cam (scaling down and positioning in corner)
    face_cam = engine.add_keyframe(face_cam, 'scale', 0.0, 0.25)
    face_cam = engine.add_keyframe(face_cam, 'position', 0.0, (800, 600)) # bottom right
    
    comp = engine.composite_layers([main_gameplay, face_cam])
    engine.export(comp, 'pip_out.mp4')
    assert comp is not None

def test_full_cinematic_trailer(engine, sample_video):
    # F1, F2, F3, F4, F5, F6, F7, F8
    vid1 = engine.ingest_video(sample_video)
    vid2 = engine.ingest_video(sample_video)
    
    # Speed ramp on vid1
    vid1_ramped = engine.apply_speed_curve(vid1, {'type': 'constant', 'speed': 0.8})
    
    # Extract audio and subtitle vid2
    aud = engine.extract_audio(vid2)
    sub = engine.generate_subtitles(aud)
    
    # Masking and blending on vid2
    vid2_masked = engine.apply_mask(vid2, 'circle', {'cx': 50, 'cy': 50, 'r': 40, 'feather': 10})
    vid2_blended = engine.apply_blend_mode(vid2_masked, 'overlay')
    
    # Keyframe vid2
    vid2_kf = engine.add_keyframe(vid2_blended, 'opacity', 0.0, 0.0)
    vid2_kf = engine.add_keyframe(vid2_kf, 'opacity', 2.0, 1.0)
    
    # Composite all together
    comp = engine.composite_layers([vid1_ramped, vid2_kf, sub])
    
    engine.export(comp, 'trailer_out.mp4')
    assert comp is not None
