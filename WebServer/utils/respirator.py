from .motor import Motor
import threading
from time import sleep
import configparser
from pydub import AudioSegment
from pydub.playback import play

from pprint import pprint as pp


config = configparser.ConfigParser()
config.read("config.conf")

MIN_RPM_MOTOR = int(config.get('Motor', 'MIN_RPM_MOTOR'))
MAX_RPM_MOTOR = int(config.get('Motor', 'MAX_RPM_MOTOR'))
MIN_PREASURE = int(config.get('Pressure', 'MIN_PRESSURE'))
MAX_PREASURE = int(config.get('Pressure', 'MAX_PRESSURE'))
POLL_FREQ = int(config.get('Respirator', 'POLL_FREQ'))


class Respirator(threading.Thread):

    def __init__(self, ID, loc):
        """
        Tries to initialize all the respirator parameters, if not able, raises the
        alarm.
        """
        self.alarm = False
        threading.Thread.__init__(self, daemon=True)
        self.motor = Motor()
        self.ID = ID
        self.loc = loc
        self.info = {"rpm": self.motor.get_rpm(),
                    "pressure": 55,
                    "id": self.ID,
                    "loc": self.loc,
                    "status": "off"
                    }
        self.buzz = AudioSegment.from_mp3("utils/buzz.mp3")

    def run(self):
        """
        Main controll loop and target of the thread, every POLL_FREQ reuests the
        rpms of the motor and the pressure of the sensor. It decides weather the
        values are correct or within the operation range and changes the status
        according to them.
        """

        while True:
            self.info["rpm"] = self.motor.get_rpm()
            self.info["pressure"] = 55
            
            # The -2 value of rpm means internal error of the motor module
            if self.info["rpm"] == -2:
                self._raise_the_alarm()

            # The -1 value of rpm means that the motor does not have enough
            # samples yet
            elif self.info["rpm"] == -1 and self.info["status"] == "off":
                self.info["status"] = "off"

            # If the value is positive 
            if self.info["rpm"] > 0:  
                
                # Check if rpm is in range of the operational parameters 
                if self.info["rpm"] < MIN_RPM_MOTOR or self.info["rpm"] > MAX_RPM_MOTOR:
                    self._raise_the_alarm()

                # Check if pressure is in range of the operation parameters
                elif self.info["pressure"] < MIN_PREASURE or self.info["pressure"] > MAX_PREASURE:
                    self._raise_the_alarm()

                # If a value is received and status was off, turn on
                elif self.info["status"] == "off":
                    self.info["status"] = "on"

            # If the status was on, a negative value indicates an error
            elif self.info["status"] == "on":
                self._raise_the_alarm()
            
            # Wait to continue polling
            sleep(POLL_FREQ)

    def _raise_the_alarm(self):
        """
        Creates a new thread that reproduces a buzzer sound every 0.5 seconds
        """
        self.info["status"] = "fail"
        def run():
            while True:
                #play(self.buzz)
                print("ALARMA")
                sleep(0.5)

        if not self.alarm:
            self.alarm = True
            threading.Thread(target=run, daemon=True).start()
            

    def get_info(self):
        """
        Returns the current info of the respirator
        :retuns: self.info
        """
        return self.info


# Little script to test
if __name__ == "__main__":
    respirator = Respirator(1234, 123)
    respirator.start()
    while True:
        pp(respirator.info)
        sleep(2)
