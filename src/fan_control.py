import RPi.GPIO as GPIO
import os
import time

class FanManager:
    def __init__(self, pin=12):
        self.fan_pin = pin
        GPIO.setup(self.fan_pin, GPIO.OUT)
        # 100Hz frequency par PWM start karna
        self.pwm = GPIO.PWM(self.fan_pin, 100)
        self.pwm.start(0)

    def get_temp(self):
        # Pi ka internal CPU temperature read karna
        res = os.popen('vcgencmd measure_temp').readline()
        temp = float(res.replace("temp=","").replace("'C\n",""))
        return temp

    def update_speed(self):
        temp = self.get_temp()
        
        # Speed logic:
        # 45'C se kam -> 20% speed
        # 45-55'C -> 50% speed
        # 55'C se upar -> 100% speed
        if temp < 45:
            speed = 20
        elif 45 <= temp < 55:
            speed = 60
        else:
            speed = 100
            
        self.pwm.ChangeDutyCycle(speed)
        return temp, speed

    def stop(self):
        self.pwm.stop()
