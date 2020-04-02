from time import sleep, time
from collections import deque
from pprint import pprint as pp
import configparser

## SIMULATION ONLY ##
import random
import threading
## END SYMULATION  ##

config = configparser.ConfigParser()
config.read("config.conf")

STARTUP_TIME = int(config.get('Motor', 'STARTUP_TIME'))

class Motor():
    def __init__(self):
        self.raw = []
        self.startup = time()
        self.status = 'off'
        ## SIMULATION ONLY ##
        def run():
            for i in range(60):
                self.handle()
                sleep(random.uniform(1.4, 1.6))
            sleep(15)
            while True:
                self.handle()
                sleep(random.uniform(1.4, 1.6))

        threading.Thread(target=run, daemon=True).start()
        ## END SYMULATION  ##
    
    def handle(self):
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
            if now - self.startup < STARTUP_TIME:
                return -1
            while now - self.raw[0] > 60.0:
                self.raw.pop(0)     
            interrupts = len(self.raw)
            time_diff = (now - self.raw[0])/60
            return interrupts/time_diff
        except:
            self.status = 'fail'
            return -2


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

