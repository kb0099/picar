# manual_test.py

import sys;
import time;

sys.path.append('..');

from motor import Motor;
from car_config import *;
from powertrain import Powertrain;
## Note  :
## Usage : python pt.py <test#> <args>

## Example
## To run test0 with argument 50
##      python pt.py 0 50
##
## To run test1 with duty cycle of 40:
##      python pt.py 1 40
##
## And similar for other tests!


# global
pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP);

# test0 is for motors
def test0(dc):
    m1 = Motor(LFP, LBP, LEP);
    m2 = Motor(RFP, RBP, REP);
    m1.forward(dc[0]);
    time.sleep(2);
    m1.off();
    m2.forward(dc[0]);
    time.sleep(2);
    
# forward
def test1(dc):
    pt.forward(dc[0]);
    time.sleep(2);

# reverse
def test2(dc):
    pt.reverse(dc[0]);
    time.sleep(2);

# turn:     def turn(self, left_duty_cycle, right_duty_cycle, left_forward=True, right_forward=True):
def test3(dc):
    pt.turn(dc[0], dc[1]);
    time.sleep(2);


# turn-left: turn_left(self, max_duty_cycle, intensity=50.0, forward = True):
def test4(arg):
    pt.turn_left(arg[0], arg[1]);
    time.sleep(2);
    

# turn-right: turn_right(self, max_duty_cycle, intensity=50.0, forward=True):
def test5(arg):
    pt.turn_right(arg[0], arg[1]);
    time.sleep(2);

# tur-intensity: turn_intensity(self, max_duty_cycle, intensity, forward=True):
def test6(arg):
    pt.turn_intensity(arg[0], arg[1]);
    time.sleep(2);

# pivot pivot(self, duty_cycle, clockwise=False):
def test7(arg):
    pt.pivot(arg[0], arg[1]);
    time.sleep(2);

# stop
def test8(dc):
    pt.forward(dc[0]);
    time.sleep(2)
    pt.stop();
    time.sleep(2);
    pt.forward(dc[0])
    time.sleep(2);

    
# global tests
tests = [test0, test1, test2, test3, test4, test5, test6, test7, test8];
if __name__ == "__main__":
    tests[int(sys.argv[1])](map(float, sys.argv[2:]));
    print("all done!");
    pt.cleanup();
    
    
