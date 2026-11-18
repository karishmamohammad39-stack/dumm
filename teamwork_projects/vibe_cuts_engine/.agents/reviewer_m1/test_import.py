import os
import sys

# Add the src directory to the path so we can import src.core.io
sys.path.insert(0, os.path.abspath('.'))

try:
    from src.core.io import load_video, export_video, extract_audio
    print("Imports successful!")
    print(load_video)
except Exception as e:
    print(f"Error importing: {e}")

