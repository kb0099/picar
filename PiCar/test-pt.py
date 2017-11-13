#!python2
from powertrain import Powertrain
from car_config import *
import time
import RPi.GPIO as GPIO

try:
    pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
    time.sleep(3)
    pt.turn_intensity(100, 50)
    time.sleep(1.5)
    pt.turn_intensity(100, -50)
    time.sleep(1.5)
    pt.turn_intensity(90, 45)
    time.sleep(1.5)
    pt.turn_intensity(90, 45)
    time.sleep(1.5)
    pt.stop()
    GPIO.cleanup()
except KeyboardInterrupt:
    pt.stop()
    GPIO.cleanup()
