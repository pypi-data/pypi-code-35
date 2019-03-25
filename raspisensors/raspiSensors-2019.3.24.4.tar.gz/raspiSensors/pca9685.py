#!/bin/python3
"""

# author:    Johann Hofstaetter
# website:   http://www.sabhan.at
# PCA9685 Adafruit 16-channel 12 Bit PWM Driver

"""
from adafruit_servokit import ServoKit



class PCA9685():


    def __init__(self, channels=16):


        # init servo
        self.channels = channels
        self.kit = ServoKit(channels=self.channels)
