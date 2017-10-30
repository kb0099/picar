from __future__ import print_function;
#
# Sample demo for obstacle detector (od)
#

import sys;
import time;
import RPi.GPIO as GPIO

sys.path.append('..');

from ObstacleDetector import ObstacleDetector;
from car_config import *;
from motor import Motor;
import time
left = Motor(LFP, LBP, LEP);
right = Motor(RFP, RBP, REP);

def stop(distance):
	print("Distance is {0}".format(distance))
	left.off()
	right.off()
	time.sleep(1)
	left.forward(60)
	right.backward(60)
	time.sleep(1)
	left.forward(50)
	right.forward(50)
	return
def od_handler(d):
  print("distance is %f" % d);
  return;
# sample function
def obstacle_detector_sample_usage():
	dt = ObstacleDetector(TRIGGER_PIN, ECHO_PIN, 20);
	dt.set_distance_threshold(20)
	left.forward(50)
	right.forward(50)
	try:
	  print("before starting thread");
	  dt.start();
	  print( "after starting the thread");
	  #dt.on_obstacle_detected_handler(lambda self, d : print("distance is %f " % d));
	  #dt.on_obstacle_detected_handler(lambda d : print("distance is %f " % d));
	  dt.on_obstacle_detected_handler(stop)
	  while 1:
	  	do_nothing = 1
	except KeyboardInterrupt:
	  print("TRYING TO STOP")
	  dt.do_run = False
	  dt.join();
	  print("STOPPED")
  
  
# run the function
obstacle_detector_sample_usage();

