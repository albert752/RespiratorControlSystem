from motor import Motor
import threading
from time import sleep, time
import configparser
from pydub import AudioSegment
from pydub.playback import play

from pprint import pprint as pp

# CONFIGURATION CONSTANTS
config = configparser.ConfigParser()
config.read("config.conf")

MIN_RPM_MOTOR = int(config.get('Motor', 'MIN_RPM_MOTOR'))
MAX_RPM_MOTOR = int(config.get('Motor', 'MAX_RPM_MOTOR'))
MAX_DIFF_SAMPLES = int(config.get('Motor', 'MAX_DIFF_SAMPLES'))
POLL_FREQ = int(config.get('Respirator', 'POLL_FREQ'))


class Respirator(threading.Thread):

    def __init__(self, ID, loc):
        """
        Tries to initialize all the respirator parameters, if not able, raises the
        alarm.
        """
        self.alarm = False
        threading.Thread.__init__(self, daemon=True)
        self.motor = Motor(debug=True)
        self.ID = ID
        self.loc = loc
        self.info = {"rpm": self.motor.get_rpm(),
                    "id": self.ID,
                    "loc": self.loc,
                    "status": "off"
                    }
        self.buzz = AudioSegment.from_mp3("utils/buzz.mp3")


    def run(self):
        """
        Main controll loop and target of the thread, every POLL_FREQ reuests the
        last sample of the motor and the current RPMS. 
        If during the last MAX_DIFF_SAMPLES seconds there is no new samples, 
        raises the alarm.
        If the rpm value is out of operating parameters or contains an error
        code, raises the alarm.
        """
        while True:
            # Check if if there has been an interrupt during the last 6s
            now = time()
            last = self.motor.get_last_sample()
            if now - last > MAX_DIFF_SAMPLES:
                self._raise_the_alarm("No new samples, motor stopped")
            
            # Check the current RPMs
            self.info["rpm"] = self.motor.get_rpm()

            # The -2 value of rpm means internal error of the motor module
            if self.info["rpm"] == -2:
                self._raise_the_alarm("Internal motor monitor system error")

            # The -1 value of rpm means that the motor does not have enough
            # samples yet
            elif self.info["rpm"] == -1 and self.info["status"] == "off":
                self.info["status"] = "off"

            # If the value is positive 
            if self.info["rpm"] > 0:  
                
                # Check if rpm is in range of the operational parameters 
                if self.info["rpm"] < MIN_RPM_MOTOR or self.info["rpm"] > MAX_RPM_MOTOR:
                    self._raise_the_alarm("RPMs out of bounds")

                # If a value is received and status was off, turn on
                elif self.info["status"] == "off":
                    self.info["status"] = "on"

            # If the status was on, a negative value indicates an error
            elif self.info["status"] == "on":
                self._raise_the_alarm("RPMs are negative")
            
            # Wait to continue polling
            sleep(POLL_FREQ)

    def _raise_the_alarm(self, cause):
        """
        Creates a new thread that reproduces a buzzer sound every 0.5 seconds
        """
        self.info["status"] = "fail"
        def run():
            while True:
                # play(self.buzz)
                print(f"!!! The alarm has been triggered: {cause}")
                sleep(0.5)

        if self.alarm == False:
            self.alarm = threading.Thread(target=run, daemon=True)
            self.alarm.start()
            

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
        sleep(1)
