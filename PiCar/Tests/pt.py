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
## To run test0 with argument 0
##      python pt.py 0 0
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
    
    
def test1(dc):
    pt.forward(dc[0]);
    time.sleep(2);
    
def test2(dc):
    pt.reverse(dc[0]);
    time.sleep(2);

    
    
def test3(x):
    print(x);
    
# global tests
tests = [test0, test1, test2, test3];
if __name__ == "__main__":
    tests[int(sys.argv[1])](map(float, sys.argv[2:]));
    print("all done!");
    pt.cleanup();
    
    
