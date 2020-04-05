#!/usr/bin/python3

from .motor import Motor
import threading
from time import sleep, time
import RPi.GPIO as GPIO
from pprint import pprint as pp


class Respirator(threading.Thread):

    def __init__(self, config):
        """
        Tries to initialize all the respirator parameters, if not able, raises the
        alarm.
        """
        threading.Thread.__init__(self, daemon=True)
        self.config = config
        self.motor = Motor(debug=False, self.config)
        self.info = {"rpm": self.motor.get_rpm(),
                    "id": self.config['Respirator']['ID'],
                    "loc": self.config['Respirator']['ID'],
                    "status": "off"
                    }
        self.alarm = None

        # GPIO configuration
        GPIO.setmode(GPIO.BOARD)
        button_pin = 13 # G27 7th pin interior row
        GPIO.setup([button_pin], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button_pin, GPIO.RISING, self._on_button)


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
            last = self.motor.get_last_sample()
            if last != None:
                if self.info['status'] == 'off':
                    self.info['status'] = 'cal'
                # Check if if there has been an interrupt during the last 6s
                now = time()
                if now - last > config['Motor']['MAX_DIFF_SAMPLES']:
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
                    if self.info["rpm"] < config['Motor']['MIN_RPM_MOTOR'] 
                    or self.info["rpm"] > config['Motor']['MAX_RPM_MOTOR']:
                        self._raise_the_alarm("RPMs out of bounds")

                    # If a value is received and status was off, turn on
                    elif self.info["status"] == "cal":
                        self.info["status"] = "on"

                # If the status was on, a negative value indicates an error
                elif self.info["status"] == "on":
                    self._raise_the_alarm("RPMs are negative")
            
            # Wait to continue polling
            sleep(config['Respirator']['POLL_FREQ'])

    def _get_alarm(self):
        return self.alarm

    def _on_button(self, pin):
        self.alarm = False

    def _raise_the_alarm(self, cause):
        """
        Creates a new thread that reproduces a buzzer sound every 0.5 seconds
        """
        self.info["status"] = "fail"
        def run(alarm):
            while alarm():
                print(f"!!! The alarm has been triggered: {cause}")
                sleep(0.5)

        if self.alarm == None:
            self.alarm = True
            threading.Thread(target=run, args=(lambda: self.alarm, ),  daemon=True).start()
            
    
    def get_info(self):
        """
        Returns the current info of the respirator
        :retuns: self.info
        """
        return self.info


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

    respirator = Respirator(config)
    respirator.start()
    while True:
        pp(respirator.get_info())
        sleep(1)
