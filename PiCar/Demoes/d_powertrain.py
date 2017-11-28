"""Script to demonstrate the Powertrain class operating"""

import sys
import time

sys.path.append('..')

from powertrain import Powertrain
from car_config import *
import RPi.GPIO as GPIO

pwr = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
t = 2 # time to delay actions; in seconds
try:
    # roll forward and backward
    print("calling forward(80)")
    pwr.forward(100)
    time.sleep(t);
    print("calling reverse(80)")
    pwr.reverse(100)
    time.sleep(t)
    pwr.stop()

    # pivot clockwise and counterclockwise
    print("calling pivot(50)")
    pwr.pivot(80)
    time.sleep(t)
    print("calling pivot(50, clockwise=True)")
    pwr.pivot(80, True)
    time.sleep(t)
    pwr.stop()

    # turn wide
    print("calling turn_left(50, 20)")
    pwr.turn_left(100, 80)
    time.sleep(t)
    pwr.stop()

    # turn tight
    print("calling turn_right(80, 80)")
    pwr.turn_right(100, 80)
    time.sleep(t)
    pwr.stop()

    print("done")
except KeyboardInterrupt:
    pwr.stop()
    GPIO.cleanup()
