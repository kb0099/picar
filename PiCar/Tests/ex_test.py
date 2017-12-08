# manual_test.py

import sys;
import time;

sys.path.append('..');
from car_config import *;
from ex import *;


# ==================================================== temp


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
# EX_DIRECTION_PWM        = 18;
# EX_DIRECTION_LEFT       = 14;
# EX_DIRECTION_RIGHT      = 15;


# EX_SPEED_PWM            = 13;
# EX_SPEED_FORWARD        = 26;
# EX_SPEED_BACKWARD       = 19;


# direction motor
dm = DirMotor(EX_DIRECTION_LEFT, EX_DIRECTION_RIGHT, EX_DIRECTION_PWM);
sm = SpeedMotor(EX_SPEED_FORWARD, EX_SPEED_BACKWARD, EX_SPEED_PWM);


# test0 is for reset
def test0(dc):
    dm.reset();
    time.sleep(2);
    
# left
def test1(dc):
    dm.left(dc[0]);
    time.sleep(2);

# right
def test2(dc):
    dm.right(dc[0]);
    time.sleep(2);

# speed: forward
def test3(dc):
    sm.forward(dc[0]);
    time.sleep(2);


# speed: backward
def test4(arg):
    sm.backward(arg[0]);
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
    dm.cleanup();
    
    
