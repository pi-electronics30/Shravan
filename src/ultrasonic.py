# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

class UltrasonicManager:
    def __init__(self, config):
        """
        config: { "left": {"trig": 5, "echo": 6}, ... }
        """
        self.config = config
        self.setup_pins()

    def setup_pins(self):
        # GPIO Setup for all 3 sensors
        for side in self.config:
            trig = self.config[side]["trig"]
            echo = self.config[side]["echo"]
            GPIO.setup(trig, GPIO.OUT)
            GPIO.setup(echo, GPIO.IN)
            GPIO.output(trig, False) # Initial Low
        time.sleep(0.5) # Sensors ko settle hone ka time do

    def _read_distance(self, trig, echo):
        """Hardware level distance calculation"""
        try:
            # Trigger Pulse
            GPIO.output(trig, True)
            time.sleep(0.00001)
            GPIO.output(trig, False)

            start_time = time.time()
            stop_time = time.time()

            # Timeout logic to prevent freezing if sensor fails
            timeout = time.time() + 0.1 

            while GPIO.input(echo) == 0:
                start_time = time.time()
                if time.time() > timeout: return 400.0 # Max distance on timeout

            while GPIO.input(echo) == 1:
                stop_time = time.time()
                if time.time() > timeout: return 400.0

            elapsed = stop_time - start_time
            # Sound speed 34300 cm/s
            distance = (elapsed * 34300) / 2
            
            # Limit distance to avoid garbage values
            return round(min(distance, 400.0), 2)
        except Exception as e:
            print(f"Sensor Error: {e}")
            return 400.0

    def get_distance(self, side):
        """Public method to get distance of a specific side"""
        if side in self.config:
            trig = self.config[side]["trig"]
            echo = self.config[side]["echo"]
            return self._read_distance(trig, echo)
        return 400.0

    def get_all_distances(self):
        """Returns a dictionary of all distances"""
        return {side: self.get_distance(side) for side in self.config}

    def get_closest(self):
        """Legacy support for your old main.py logic"""
        distances = self.get_all_distances()
        closest_side = min(distances, key=distances.get)
        return closest_side, distances[closest_side]

