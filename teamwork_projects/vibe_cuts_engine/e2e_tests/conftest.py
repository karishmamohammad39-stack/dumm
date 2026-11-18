import pytest
import os
import tempfile
from pathlib import Path

@pytest.fixture
def sample_video():
    fd, path = tempfile.mkstemp(suffix='.mp4')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def sample_audio():
    fd, path = tempfile.mkstemp(suffix='.wav')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def sample_image():
    fd, path = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def engine():
    from src.api.vibe_engine import VibeEngine
    return VibeEngine()
