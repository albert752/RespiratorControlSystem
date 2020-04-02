from motor import Motor
import threading
from time import sleep

from pprint import pprint as pp

MIN_RPM_MOTOR = 35
MAX_RPM_MOTOR = 45
MIN_PREASURE = 45
MAX_PREASURE = 55

class Breather(threading.Thread):
    def __init__(self, ID, loc):
        threading.Thread.__init__(self, daemon=True)
        self.motor = Motor(1)
        self.ID = ID
        self.loc = loc
        self.info = {"rpm": self.motor.get_rpm(),
                        "preasure": 55,
                        "id": self.ID,
                        "loc": self.loc,
                        "status": "off"
                        }
    def run(self):
        self.motor.start()
        while True:
            self.info["rpm"] = self.motor.get_rpm()
            self.info["preasure"] = 55
            if self.info["rpm"] > 0:  
                if self.info["rpm"] < MIN_RPM_MOTOR or self.info["rpm"] > MAX_RPM_MOTOR:
                    self.info["status"] = "fail"
                elif self.info["preasure"] < MIN_PREASURE or self.info["rpm"] > MAX_PREASURE:
                    self.info["status"] = "fail"
                elif self.info["status"] == "off":
                    self.info["status"] = "on"
            elif self.info["status"] == "on":
                self.info["status"] = "fail"    
            sleep(1)

    def get_info(self):
        return self.info
