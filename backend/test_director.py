from director import analyze_audio_and_build_filters

filter_string = analyze_audio_and_build_filters("../test_video.mp4", 15.0)
print(filter_string)
