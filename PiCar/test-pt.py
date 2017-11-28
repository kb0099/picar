#!python2
from powertrain import Powertrain
from car_config import *
import time
import RPi.GPIO as GPIO

try:
    pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
    time.sleep(3)
    pt.turn_intensity(60, -10)
    time.sleep(2)
    pt.stop()
    time.sleep(1)
    pt.turn_intensity(60, 50)
    time.sleep(1.5)
    pt.turn_intensity(60, -50)
    time.sleep(1.5)
    pt.turn_intensity(50, 50)
    time.sleep(1.5)
    pt.turn_intensity(50, -50)
    time.sleep(1.5)
    pt.stop()
    GPIO.cleanup()
except KeyboardInterrupt:
    pt.stop()
    GPIO.cleanup()
