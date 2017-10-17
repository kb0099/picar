import sys;
import time;

sys.path.append('..');

from motor import Motor;
from car_config import *;


left = Motor(LFP, LBP, LEP);
right = Motor(RFP, RBP, REP);

def test_left():
	left.forward(50);
	time.sleep(2);
	left.off();
	time.sleep(1);
	left.backward(50);
	time.sleep(2);
	left.off();

def test_right():
	right.forward(80);
	time.sleep(1);
	right.off();
	time.sleep(1);
	right.backward(80);
	time.sleep(1);
	right.off();

test_left();
test_right();
left.cleanup();
right.cleanup();

