import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Attempt to import the module
import src.core.io as core_io

class TestCoreIO(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('src.core.io.VideoFileClip')
    def test_extract_audio_same_file_overwrite_bug(self, mock_vfc):
        # Bug: If input is a file like "test.mp3", extract_audio will try to write "test.mp3"
        # while it's potentially open, or it will just blindly overwrite it.
        mock_clip = MagicMock()
        mock_clip.audio = MagicMock()
        mock_vfc.return_value = mock_clip

        input_path = os.path.join(self.temp_dir_path, "test.mp3")
        with open(input_path, "w") as f:
            f.write("fake file")

        # Call extract_audio
        out_path = core_io.extract_audio(input_path)

        # It should try to write to test.mp3
        self.assertEqual(out_path, input_path)
        mock_clip.audio.write_audiofile.assert_called_once_with(input_path)

    @patch('src.core.io.VideoFileClip')
    def test_export_video_closes_clip(self, mock_vfc):
        # Bug: export_video closes the clip, making it unusable for the caller
        mock_clip = MagicMock()
        
        output_path = os.path.join(self.temp_dir_path, "out.mp4")
        core_io.export_video(mock_clip, output_path)

        mock_clip.write_videofile.assert_called_once_with(output_path, codec="libx264", audio_codec="aac")
        mock_clip.close.assert_called_once() # This proves the side-effect bug!

    @patch('src.core.io.VideoFileClip')
    def test_extract_audio_read_only_dir(self, mock_vfc):
        # Bug: extract_audio assumes it can write to the same directory as the input video.
        # It should probably accept an optional output path.
        pass

if __name__ == '__main__':
    unittest.main()
