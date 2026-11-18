import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import pytest
from src.core.io import load_video, export_video, extract_audio

class TestIOUnit(unittest.TestCase):
    @patch('src.core.io.os.path.isfile')
    @patch('src.core.io.VideoFileClip')
    def test_load_video_success(self, mock_video_file_clip, mock_isfile):
        mock_isfile.return_value = True
        mock_clip = MagicMock()
        mock_video_file_clip.return_value = mock_clip
        
        result = load_video("fake_path.mp4")
        
        mock_isfile.assert_called_once_with("fake_path.mp4")
        mock_video_file_clip.assert_called_once_with("fake_path.mp4")
        self.assertEqual(result, mock_clip)
        
    @patch('src.core.io.os.path.isfile')
    def test_load_video_not_found(self, mock_isfile):
        mock_isfile.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            load_video("fake_path.mp4")

    @patch('src.core.io.os.replace')
    @patch('src.core.io.tempfile.TemporaryDirectory')
    def test_export_video(self, mock_tempdir, mock_replace):
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_clip = MagicMock()
        
        export_video(mock_clip, "out_path.mp4")
        
        expected_tmp = os.path.join('fake_temp', 'temp.mp4')
        mock_clip.write_videofile.assert_called_once_with(expected_tmp, codec="libx264", audio_codec="aac")
        mock_replace.assert_called_once_with(expected_tmp, "out_path.mp4")
        mock_clip.close.assert_not_called()

    @patch('src.core.io.tempfile.TemporaryDirectory')
    def test_export_video_keyboard_interrupt(self, mock_tempdir):
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_clip = MagicMock()
        mock_clip.write_videofile.side_effect = KeyboardInterrupt("Ctrl+C")
        
        with self.assertRaises(KeyboardInterrupt):
            export_video(mock_clip, "out_path.mp4")

    @patch('src.core.io.uuid.uuid4')
    @patch('src.core.io.os.replace')
    @patch('src.core.io.tempfile.TemporaryDirectory')
    @patch('src.core.io.os.path.isfile')
    @patch('src.core.io.VideoFileClip')
    def test_extract_audio_success(self, mock_video_file_clip, mock_isfile, mock_tempdir, mock_replace, mock_uuid4):
        mock_uuid4.return_value.hex = '1234'
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_isfile.return_value = True
        mock_video = MagicMock()
        mock_audio = MagicMock()
        mock_video.audio = mock_audio
        mock_video_file_clip.return_value = mock_video
        
        result = extract_audio("fake_vid.mp4")
        
        mock_isfile.assert_called_once_with("fake_vid.mp4")
        mock_video_file_clip.assert_called_once_with("fake_vid.mp4")
        self.assertTrue(result.endswith(".mp3"))
        
        expected_tmp = os.path.join('fake_temp', 'temp.mp3')
        
        mock_audio.write_audiofile.assert_called_once_with(expected_tmp)
        mock_replace.assert_called_once_with(expected_tmp, result)
        mock_video.close.assert_called_once()
        mock_audio.close.assert_called_once()

    @patch('src.core.io.os.replace')
    @patch('src.core.io.tempfile.TemporaryDirectory')
    @patch('src.core.io.os.path.isfile')
    @patch('src.core.io.VideoFileClip')
    def test_extract_audio_with_output_path(self, mock_video_file_clip, mock_isfile, mock_tempdir, mock_replace):
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_isfile.return_value = True
        mock_video = MagicMock()
        mock_audio = MagicMock()
        mock_video.audio = mock_audio
        mock_video_file_clip.return_value = mock_video
        
        result = extract_audio("fake_vid.mp4", "custom_out.mp3")
        
        expected_tmp = os.path.join('fake_temp', 'temp.mp3')
        mock_audio.write_audiofile.assert_called_once_with(expected_tmp)
        mock_replace.assert_called_once_with(expected_tmp, "custom_out.mp3")
        self.assertEqual(result, "custom_out.mp3")

    @patch('src.core.io.tempfile.TemporaryDirectory')
    @patch('src.core.io.os.path.isfile')
    @patch('src.core.io.VideoFileClip')
    def test_extract_audio_base_exception(self, mock_video_file_clip, mock_isfile, mock_tempdir):
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_isfile.return_value = True
        mock_video = MagicMock()
        mock_audio = MagicMock()
        mock_video.audio = mock_audio
        mock_video_file_clip.return_value = mock_video
        mock_audio.write_audiofile.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(KeyboardInterrupt):
            extract_audio("fake_vid.mp4", "custom_out.mp3")
            
        mock_video.close.assert_called_once()
        mock_audio.close.assert_called_once()


    @patch('src.core.io.os.path.isfile')
    @patch('src.core.io.VideoFileClip')
    def test_extract_audio_no_audio(self, mock_video_file_clip, mock_isfile):
        mock_isfile.return_value = True
        mock_video = MagicMock()
        mock_video.audio = None
        mock_video_file_clip.return_value = mock_video
        
        with self.assertRaises(ValueError):
            extract_audio("fake_vid.mp4")

    @patch('src.core.io.tempfile.TemporaryDirectory')
    def test_export_video_standard_exception(self, mock_tempdir):
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_clip = MagicMock()
        mock_clip.write_videofile.side_effect = Exception("General error")
        
        with self.assertRaisesRegex(Exception, "General error"):
            export_video(mock_clip, "out_path.mp4")

    @patch('src.core.io.tempfile.TemporaryDirectory')
    @patch('src.core.io.os.path.isfile')
    @patch('src.core.io.VideoFileClip')
    def test_extract_audio_standard_exception(self, mock_video_file_clip, mock_isfile, mock_tempdir):
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_isfile.return_value = True
        mock_video = MagicMock()
        mock_audio = MagicMock()
        mock_video.audio = mock_audio
        mock_video_file_clip.return_value = mock_video
        mock_audio.write_audiofile.side_effect = Exception("General error")
        
        with self.assertRaisesRegex(Exception, "General error"):
            extract_audio("fake_vid.mp4", "custom_out.mp3")

    @patch('src.core.io.os.replace')
    @patch('src.core.io.tempfile.TemporaryDirectory')
    def test_export_video_no_extension(self, mock_tempdir, mock_replace):
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = 'fake_temp'
        mock_tempdir.return_value = mock_temp
        
        mock_clip = MagicMock()
        
        export_video(mock_clip, "out_path")
        
        expected_tmp = os.path.join('fake_temp', 'temp.mp4')
        mock_clip.write_videofile.assert_called_once_with(expected_tmp, codec="libx264", audio_codec="aac")
        # Fix for Bug 1: assert "out_path.mp4" not "out_path"
        mock_replace.assert_called_once_with(expected_tmp, "out_path.mp4")

@pytest.mark.integration
def test_integration_io():
    try:
        from moviepy.editor import ColorClip, AudioClip
    except ImportError:
        try:
            from moviepy import ColorClip, AudioClip
        except ImportError:
            pytest.skip("MoviePy not found")
        
    with tempfile.TemporaryDirectory() as tmpdir:
        import numpy as np
        
        def make_frame(t):
            return [np.sin(440 * 2 * np.pi * t)]
            
        dummy_audio = AudioClip(make_frame, duration=1)
        dummy_video = ColorClip(size=(64, 64), color=(255, 0, 0), duration=1)
        dummy_video = dummy_video.set_audio(dummy_audio)
        
        input_video_path = os.path.join(tmpdir, "input.mp4")
        dummy_video.fps = 24
        dummy_video.write_videofile(input_video_path, codec="libx264", audio_codec="aac", fps=24, logger=None)
        
        clip = load_video(input_video_path)
        try:
            assert clip.duration >= 0.9
            
            output_video_path = os.path.join(tmpdir, "output.mp4")
            export_video(clip, output_video_path)
            assert os.path.exists(output_video_path)
            
            res = extract_audio(input_video_path)
            try:
                assert res.endswith(".mp3")
                assert os.path.exists(res)
            finally:
                if os.path.exists(res):
                    os.remove(res)
            
            custom_audio_path = os.path.join(tmpdir, "custom.mp3")
            res2 = extract_audio(input_video_path, custom_audio_path)
            assert res2 == custom_audio_path
            assert os.path.exists(custom_audio_path)
        finally:
            clip.close()
