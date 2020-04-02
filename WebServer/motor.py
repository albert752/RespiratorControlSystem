from time import sleep, time
from collections import deque
from pprint import pprint as pp
## SIMULATION ONLY ##
import random
import threading
## END SYMULATION  ##

STARTUP_TIME = 10

class Motor():
    def __init__(self):
        self.raw = []
        self.startup = time()
        self.status = 'off'
        ## SIMULATION ONLY ##
        def run():
            while True:
                self.handle()
                sleep(random.uniform(1.4, 1.6))
        threading.Thread(target=run, daemon=True).start()
        ## END SYMULATION  ##
    
    def _get_data(self):
        ## SIMULATION ONLY ##
        return random.choices(population=[1, 0], weights=[4/6, 2/6], k=1)[0]
        ## END SYMULATION  ##

    def handle(self):
        ## SIMULATION ONLY ##
        value = self._get_data()
        ## END SYMULATION  ##
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

