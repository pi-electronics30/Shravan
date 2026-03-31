import RPi.GPIO as GPIO

class ModeManager:
    def __init__(self, pin):
        self.pin = pin
        self.modes = ["CAMERA + ULTRASONIC", "ULTRASONIC ONLY", "CAMERA ONLY"]
        self.current_idx = 0
        # GPIO Setup logic in main to avoid conflicts
        
    def switch_mode(self):
        self.current_idx = (self.current_idx + 1) % len(self.modes)
        return self.modes[self.current_idx]

    def get_mode(self):
        return self.modes[self.current_idx]
