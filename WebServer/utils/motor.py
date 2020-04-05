#!/usr/bin/python3

from time import sleep, time
from pprint import pprint as pp
import RPi.GPIO as GPIO
import os

## SIMULATION ONLY ##
import threading
import random
## END SYMULATION  ##

class Motor():
    def __init__(self, debug=False, config):

        # Gather the configuration
        self.config = config

        # GPIO configuration
        GPIO.setmode(GPIO.BOARD)
        sensor_pin = 11 # G17
        GPIO.setup([sensor_pin], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(sensor_pin, GPIO.RISING, self.on_sensor)

        # Inner variable configuration
        self.raw = []
        self.startup = None

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
        """
        Handler for the reed switch. It adds the timestamp of the interruption
        to the raw list. If its the first sample, it  changes the startup time.
        """
        if len(self.raw) == 0 and self.startup == None: 
            self.startup = time()
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
                  0 if the motor is off
                 positive float representing the RPM value
        """
        try:
            if len(self.raw) == 0:
                return 0
                
            now = time()

            # If the startup time has not been consumed, return -1
            if now - self.startup < STARTUP_TIME:
                return -1

            # Remove old samples out of the one minute window
            while now - self.raw[0] > 60.0:
                self.raw.pop(0)     

            # Count the number of interrupts and divided it by the time diff
            # between the first sample of the window and the current time
            # Each pair of interrupts represents one respiration
            interrupts = len(self.raw)/2
            time_diff = (now - self.raw[0])/60
            return interrupts/time_diff

        except:
            # Any error will trigger the fail state, return -2
            return -2


# Little script to test
if __name__ == "__main__":
    config = {  
            "Respirator": {
                "ID": "123",
                "LOC": "SF45",
                "POLL_FREQ": "1"
            },
            "Motor":{
                "STARTUP_TIME": "60",
                "MIN_RPM_MOTOR": "10",
                "MAX_RPM_MOTOR": "40",
                "MAX_DIFF_SAMPLES": "6"
            }
        }    
    motor = Motor(debug=True, config)
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

