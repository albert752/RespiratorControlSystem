#!/usr/bin/python3

from time import sleep, time
from collections import deque
from pprint import pprint as pp
import configparser
import RPi.GPIO as GPIO
import os

DIR = os.getcwd() + "/WebServer/"
## SIMULATION ONLY ##
import threading
import random
## END SYMULATION  ##

# CONFIGURATION CONSTANTS
config = configparser.ConfigParser()
config.read(DIR + "config.conf")
STARTUP_TIME = int(config.get('Motor', 'STARTUP_TIME'))

class Motor():
    def __init__(self, debug=False):
        # GPIO configuration
        GPIO.setmode(GPIO.BOARD)
        sensor_pin = 11 # G17
        GPIO.setup([sensor_pin], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(sensor_pin, GPIO.RISING, self.on_sensor)

        # Inner variable configuration
        self.raw = []
        self.startup = time()

        # Debugging
        # Runs at 30RPM duging 80s, then stops
        if debug:
            def run():
                for i in range(40):
                    self.on_sensor(17)
                    sleep(0.5)
                    self.on_sensor(17)
                    sleep(1.5)

                while True: pass
            threading.Thread(target=run).start()
   
    def on_sensor(self, pin):
        self.raw.append(time())

    def get_last_sample(self):
        try:
            return self.raw[-1]
        except:
            return None

    def get_rpm(self):
        """
        Returns the current RPM value of the motor. 
        :return: -1 if the motor is starting up
                 -2 if there is an internal error
                 positive float representing the RPM value
        """
        try:
            now = time()

            # If the startup time has not been consumed, return -1
            if now - self.startup < STARTUP_TIME:
                return -1

            # Remove old samples out of the one minute window
            while now - self.raw[0] > 60.0:
                self.raw.pop(0)     

            # Count the number of interrupts and divided it by the time diff
            # between the first sample of the window and the current time
            interrupts = len(self.raw)/2
            time_diff = (now - self.raw[0])/60
            return interrupts/time_diff

        except:
            # Any error will trigger the fail state, return -2
            return -2


# Little script to test
if __name__ == "__main__":
    motor = Motor(debug=False)
    print("*** DEBUGGING MODE FOR MOTOR ***")
    while True:
        rpm = motor.get_rpm()
        print(f"\nThe rpms are {rpm}")
        print(f"DEBUG:\n\telems: {len(motor.raw)}\n")
        try:
            print(f"\traw:\n\t\t0: {motor.raw[0]}\n\t\t-1:{motor.raw[-1]}")
            print(f"\t\tdiff:{time() - motor.raw[0]} ")
        except:
            print("No samples yet")
        sleep(2)

