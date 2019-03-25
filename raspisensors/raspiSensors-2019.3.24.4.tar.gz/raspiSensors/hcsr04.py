#!/bin/python3
"""

# author:    Johann Hofstaetter
# website:   http://www.sabhan.at

"""

import RPi.GPIO as GPIO
import time


class HCSR04():

    def __init__(self, trigger_pin = 21, echo_pin = 20):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # save vars
        self.echoPin = echo_pin
        self.triggerPin = trigger_pin
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.setup(self.triggerPin, GPIO.OUT)


    def distance(self):
        GPIO.output(self.triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(self.triggerPin, False)
        start = time.time()
        stop = time.time()
        while GPIO.input(self.echoPin) == 0:
            start = time.time()
        while GPIO.input(self.echoPin) == 1:
            stop = time.time()
        # GPIO.wait_for_edge(self.echoPin, GPIO.BOTH, timeout=100)
        stop = time.time()
        return ((stop - start) * 34300.0) / 2.0