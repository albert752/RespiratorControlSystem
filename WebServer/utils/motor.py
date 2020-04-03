from time import sleep, time
from collections import deque
from pprint import pprint as pp
import configparser

## SIMULATION ONLY ##
import random
import threading
## END SYMULATION  ##

# CONFIGURATION VARIABLES
config = configparser.ConfigParser()
config.read("config.conf")
STARTUP_TIME = int(config.get('Motor', 'STARTUP_TIME'))

class Motor():
    def __init__(self, debug):
        # GPIO configuration
        GPIO.setmode(GPIO.BOARD)
        motor_pin = 11 # G17
        GPIO.setup([sensor_pin], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(sensor_pin, GPIO.RISING, self.on_sensor)

        # Inner variable configuration
        self.raw = []
        self.startup = time()

        # Debugging
        if debug:
            def run():
                for i in range(60):
                    self.on_sensor()
                    sleep(1.5)
                while True: pass
            threading.Thread(target=run).start()
   
    def on_sensor(self, pin):
        self.raw.append(time())

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
    motor = Motor()
    print("*** DEBUGGING MODE FOR MOTOR ***")
    while True:
        rpm = motor.get_rpm()
        print(f"\nThe rpms are {rpm}")
        print(f"DEBUG:\n\telems: {len(motor.raw)}\n")
        print(f"\traw:\n\t\t0: {motor.raw[0]}\n\t\t-1:{motor.raw[-1]}")
        print(f"\t\tdiff:{time() - motor.raw[0]} ")
        sleep(2)

