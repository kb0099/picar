# manual_test.py

import sys;
import time;

sys.path.append('..');

from motor import Motor;
from car_config import *;
from powertrain import Powertrain;

## Usage : python powtertrain.py <test#> <args>
def test0(x):
    print ("ready...", x);
    
def test1(dc):
    pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP);
    pt.forward(dc);
    
def test2(dc):
    pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP);
    pt.backward(dc);
    
def test3(x):
    print(x);
    
# 
tests = [test0, test1, test2, test3];
if __name__ == "__main__":
    tests[int(sys.argv[1])](sys.argv[2])
    
