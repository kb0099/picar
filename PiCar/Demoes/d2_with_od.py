
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

# sample function
def obstacle_detector_sample_usage():
  dt = ObstacleDetector(TRIGGER_PIN, ECHO_PIN, 10);
  print("before starting thread");
  dt.start();
  print( "after starting the thread");
  #dt.on_obstacle_detected_handler(lambda self, d : print("distance is %f " % d));
  dt.on_obstacle_detected_handler(lambda d : print("distance is %f " % d));
  try:
  	while 1:
  		time.sleep(.1)
  except KeyboardInterrupt:
  	print("TRYING TO STOP")
  	dt.do_run = False
  	dt.join();
  	print("STOPPED")
  
  
# run the function
obstacle_detector_sample_usage();
