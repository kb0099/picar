from ..motor import Motor;
from ..car_config import *;


left = Motor(LFP, LBP, LEP);
right = Motor(RFP, RBP, REP);

def test_left():
	left.forward(30);
	sleep(1);
	left.off();
	sleep(1);
	left.backward(1);
	sleep(1);
	left.off();

def test_right():
	right.forward(30);
	sleep(1);
	right.off();
	sleep(1);
	right.backward(1);
	sleep(1);
	right.off();

test_left();
test_right();
