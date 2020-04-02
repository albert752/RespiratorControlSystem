from .motor import Motor
import threading
from time import sleep
import configparser
from pydub import AudioSegment
from pydub.playback import play

from pprint import pprint as pp


config = configparser.ConfigParser()
config.read("config.conf")

MIN_RPM_MOTOR = int(config.get('Breather', 'MIN_RPM_MOTOR'))
MAX_RPM_MOTOR = int(config.get('Breather', 'MAX_RPM_MOTOR'))
MIN_PREASURE = int(config.get('Breather', 'MIN_RPM_MOTOR'))
MAX_PREASURE = int(config.get('Breather', 'MAX_RPM_MOTOR'))
POLL_FREQ = int(config.get('Breather', 'POLL_FREQ'))


class Breather(threading.Thread):

    def __init__(self, ID, loc):
        threading.Thread.__init__(self, daemon=True)
        self.motor = Motor()
        self.ID = ID
        self.loc = loc
        self.info = {"rpm": self.motor.get_rpm(),
                        "preasure": 55,
                        "id": self.ID,
                        "loc": self.loc,
                        "status": "off"
                        }
        self.buzz = AudioSegment.from_mp3("utils/buzz.mp3")
        self.alarm = False

    def run(self):
        while True:
            self.info["rpm"] = self.motor.get_rpm()
            self.info["preasure"] = 55

            if self.info["rpm"] == -2:
                self.info["status"] = "fail"

            elif self.info["rpm"] == -1 and self.info["status"] == "off":
                self.info["status"] = "off"

            if self.info["rpm"] > 0:  

                if self.info["rpm"] < MIN_RPM_MOTOR or self.info["rpm"] > MAX_RPM_MOTOR:
                    self.info["status"] = "fail"
                    self._raise_the_alarm()

                elif self.info["preasure"] < MIN_PREASURE or self.info["rpm"] > MAX_PREASURE:
                    self.info["status"] = "fail"
                    self._raise_the_alarm()

                elif self.info["status"] == "off":
                    self.info["status"] = "on"

            elif self.info["status"] == "on":
                self.info["status"] = "fail"    
                self._raise_the_alarm()

            sleep(POLL_FREQ)

    def _raise_the_alarm(self):
        def run():
            while True:
                play(self.buzz)
                sleep(0.5)

        if not self.alarm:
            self.alarm = True
            threading.Thread(target=run, daemon=True).start()
            

    def get_info(self):
        return self.info

if __name__ == "__main__":
    breather = Breather(1234, 123)
    breather.start()
    while True:
        pp(breather.info)
        sleep(2)
