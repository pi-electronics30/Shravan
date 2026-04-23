# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import cv2

# Internal Modules Import
from src.speech import VoiceEngine
from src.ultrasonic import UltrasonicManager                    
from src.vision import VisionManager
from src.fan_control import FanManager

# ================== CONFIGURATION ==================
ULTRA_CONFIG = {
    "left":   {"trig": 5,  "echo": 6},
    "center": {"trig": 13, "echo": 19},
    "right":  {"trig": 20, "echo": 21}
}
BUTTON_PIN = 16
FAN_PIN = 12          
REFLEX_THRESHOLD = 80 # 100cm boundary
DANGER_ZONE = 50        # Near By Danger
SPEECH_DELAY = 3.5

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    voice = VoiceEngine()
    ultra = UltrasonicManager(ULTRA_CONFIG)
    vision = VisionManager("yolov8n.pt")
    fan = FanManager(pin=FAN_PIN)
    
    voice.say("System Shravan Online. Master Hybrid Mode Active.")

    last_voice_time = 0
    print("\n" + "="*60)
    print("      SHRAVAN v5.0: BUTTON PRIORITY + AUTO-HYBRID")
    print("      Button: Force Scan | <100cm: Sensors | >100cm: Auto-Scan")
    print("="*60 + "\n")
    
    try:
        while True:
            now = time.time()
            cpu_temp, _ = fan.update_speed()

            # --- 1. DATA COLLECTION ---
            dist_L = ultra.get_distance("left")
            dist_C = ultra.get_distance("center")
            dist_R = ultra.get_distance("right")
            curr_btn = GPIO.input(BUTTON_PIN)

            print(f"Temp: {cpu_temp}'C | L:{int(dist_L)} C:{int(dist_C)} R:{int(dist_R)}      ", end="\r")

            # --- 2. THE LOGIC ENGINE (PRIORITY BASED) ---
            advice = ""

            # PRIORITY 1: MANUAL BUTTON SCAN (Sab rok kar camera on)
            if curr_btn == GPIO.LOW:
                if (now - last_voice_time) > 3.0:
                    print("\n[MANUAL SCAN]: Priority Camera Active...")
                    frame = vision.get_frame()
                    results = vision.detect_objects(frame)
                    if results and len(results.boxes) > 0:
                        box = results.boxes[0]
                        label = vision.model.names[int(box.cls[0])]
                        x_center = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
                        direction = "left" if x_center < 213 else "right" if x_center > 426 else "ahead"
                        advice = f"I see {label} {direction}"
                    else:
                        advice = "Scan Completed, NO object found"
                    last_voice_time = now

            # PRIORITY 2: REFLEX SENSORS (Inside 100cm)
            elif dist_L < REFLEX_THRESHOLD or dist_C < REFLEX_THRESHOLD or dist_R < REFLEX_THRESHOLD:
                if (now - last_voice_time) > 4.0:
                    # Multiside Logic
                    if dist_L < DANGER_ZONE and dist_C < DANGER_ZONE and dist_R < DANGER_ZONE:
                        advice = "Path Blocked. Turn back."
                    elif dist_L < DANGER_ZONE and dist_C < DANGER_ZONE:
                        advice = "Obstacle ahead and Left. Move Right."
                    elif dist_R < DANGER_ZONE and dist_C < DANGER_ZONE:
                        advice = "Obstacle ahead and Right. Move Left."
                    elif dist_C < DANGER_ZONE:
                        advice = "Obstacle ahead. Move " + ("Left" if dist_L > dist_R else "Right")
                    elif dist_L < DANGER_ZONE and dist_R < DANGER_ZONE:
                        advice = "Obstacle Left and Right. Move Forward."
                    elif dist_L < DANGER_ZONE: advice = "Object on your left"
                    elif dist_R < DANGER_ZONE: advice = "Object on your right"
                    
                    if advice: last_voice_time = now

            # PRIORITY 3: AUTO-VISION (Outside 100cm)
            elif dist_C >= REFLEX_THRESHOLD:
                if (now - last_voice_time) > SPEECH_DELAY:
                    frame = vision.get_frame()
                    results = vision.detect_objects(frame)
                    if results and len(results.boxes) > 0:
                        box = results.boxes[0]
                        if box.conf[0] > 0.75:
                            label = vision.model.names[int(box.cls[0])]
                            x_center = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
                            direction = "left" if x_center < 213 else "right" if x_center > 426 else "ahead"
                            advice = f"{label} {direction}"
                            last_voice_time = now

            # --- 3. VOICE EXECUTION ---
            if advice:
                voice.say(advice)

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nShutdown...")
    finally:
        fan.stop()
        GPIO.cleanup()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
