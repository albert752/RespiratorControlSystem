import threading
from time import sleep
from collections import deque

## SIMULATION ONLY ##
import random
## END SYMULATION  ##

class Preasure(threading.Thread):
    def __init__(self, poll_rate):
        threading.Thread.__init__(self, daemon=True)
        self.poll_rate = poll_rate
        self.raw = deque([], maxlen=poll_rate*60)

    def run(self):
        while True:
            self.raw.append(self._get_data())
            sleep(1/self.poll_rate)

    def _get_data(self):
        ## SIMULATION ONLY ##
        return random.random()
        ## END SYMULATION  ##

    def get_rpm(self):
        """
        Return the current rpm value or -1 if there is not enough data
        """
        if len(self.raw) < 60*self.poll_rate:
            return len(self.raw) - 60
        else:
            rpm = sum(self.raw) / self.poll_rate
            return rpm

if __name__ == "__main__":
    motor = Motor(1)
    motor.start()
    print("hello")
    while True:
        rpm = motor.get_rpm()
        if rpm == -1:
            print("Not enough data")
        else:
            print(f"The rpms are {rpm}")
        print(f"DEBUG:\n\telems: {len(motor.raw)}\n\traw: {motor.raw}")
        sleep(2)

