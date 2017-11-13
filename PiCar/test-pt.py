#!python2
from powertrain import Powertrain
from car_config import *
import time
import RPi.GPIO as GPIO

try:
    pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
    time.sleep(3)
    print("Turning Right Intensity .05")
    pt.turn_intensity(100, .05)
    time.sleep(3)
    print("Turning Left Intensity .05")
    pt.turn_intensity(100, -.05)
    time.sleep(3)
    print("Turning Right Intensity .30")
    pt.turn_intensity(100, .30)
    time.sleep(3)
    print("Turning Right Intensity .30")
    pt.turn_intensity(100, -.30)
except KeyboardInterrupt:
    pt.stop()
    GPIO.cleanup()