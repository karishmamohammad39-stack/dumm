import os

try:
    import cv2
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False

try:
    from scenedetect import detect, ContentDetector
    HAS_SCENEDETECT = True
except ImportError:
    HAS_SCENEDETECT = False


def track_face_and_crop(video_path: str, target_aspect: float = 9/16) -> str:
    """
    Subsystem 1: Camera & Framing FX
    Uses MediaPipe Face Detection to find the subject's face and calculate FFmpeg crop coordinates 
    to dynamically pan and keep the subject centered when converting widescreen to vertical.
    """
    if not HAS_MEDIAPIPE:
        return f"crop=ih*({target_aspect}):ih"

    try:
        mp_face_detection = mp.solutions.face_detection
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return f"crop=ih*({target_aspect}):ih"

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        face_x_centers = []
        
        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            for _ in range(0, min(total_frames, 300), 30):
                ret, frame = cap.read()
                if not ret:
                    break
                results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if results.detections:
                    for detection in results.detections:
                        bbox = detection.location_data.relative_bounding_box
                        x_center = bbox.xmin + bbox.width / 2
                        face_x_centers.append(x_center * width)
                        break
                        
        cap.release()
        
        if not face_x_centers:
            return f"crop=ih*({target_aspect}):ih"
            
        median_x = sorted(face_x_centers)[len(face_x_centers)//2]
        target_width = int(height * target_aspect)
        crop_x = int(median_x - target_width / 2)
        crop_x = max(0, min(crop_x, width - target_width))
        return f"crop={target_width}:{height}:{crop_x}:0"
    except Exception as e:
        print(f"Face tracking fallback: {e}")
        return f"crop=ih*({target_aspect}):ih"


def detect_scene_cuts(video_path: str) -> list[float]:
    """
    Subsystem 1: Camera & Framing FX
    Uses PySceneDetect to identify natural cut points in the raw video.
    """
    if not HAS_SCENEDETECT:
        return []

    try:
        scene_list = detect(video_path, ContentDetector(threshold=27.0))
        return [scene[0].get_seconds() for scene in scene_list]
    except Exception as e:
        print(f"Error detecting scenes: {e}")
        return []
