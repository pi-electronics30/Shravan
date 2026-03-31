import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import os

class VisionManager:
    def __init__(self, model_name):
        # Professional way to get model path from 'models' folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", model_name)
        
        self.model = YOLO(model_path)
        self.cam = Picamera2()
        config = self.cam.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
        self.cam.configure(config)
        self.cam.start()

    def get_frame(self):
        frame = self.cam.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return cv2.rotate(frame, cv2.ROTATE_180)

    def detect_objects(self, frame, threshold=0.5):
        results = self.model(frame, verbose=False, imgsz=320)[0]
        return results
