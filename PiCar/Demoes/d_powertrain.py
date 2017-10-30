"""Script to demonstrate the Powertrain class operating"""

import sys
import time

sys.path.append('..')

from powertrain import Powertrain
from car_config import *

pwr = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
t = 3 # time to delay actions; in seconds

# roll forward and backward
print("calling forward(80)")
pwr.forward(80)
time.sleep(t);
print("calling reverse(80)")
pwr.reverse(80)
time.sleep(t)
pwr.stop()

# pivot clockwise and counterclockwise
print("calling pivot(50)")
pwr.pivot(50)
time.sleep(t)
print("calling pivot(50, clockwise=True)")
pwr.pivot(50, True)
time.sleep(t)
pwr.stop()

# turn wide
print("calling turn_left(50, 20)")
pwr.turn_left(50, 20)
time.sleep(t)
pwr.stop()

# turn tight
print("calling turn_left(80, 80)")
pwr.turn_left(80, 80)
time.sleep(t)
pwr.stop()

print("done")
