import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BOARD)

BTN_G = 11 # G17

GPIO.setup([BTN_G], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# can't add separate callbacks for both rising and falling
#GPIO.add_event_detect(BTN_B, GPIO.RISING, lambda pin: GPIO.output(LED_B, False))
#GPIO.add_event_detect(BTN_B, GPIO.FALLING, lambda pin: GPIO.output(LED_B, True))

i = 0

def handle(pin):
    global i
    print(i)
    i += 1

GPIO.add_event_detect(BTN_G, GPIO.RISING, handle)

while True:
    pass
