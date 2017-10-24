#
# Sample demo for obstacle detector (od)
#

import sys;
import time;

sys.path.append('..');

from ObstacleDetector import ObstacleDetector;
from car_config import *;
from __future__ import print_function;

# sample function
def obstacle_detector_sample_usage():
  dt = ObstacleDetector(TRIGGER_PIN, ECHO_PIN, 10);
  print("before starting thread");
  dt.start();
  print( "after starting the thread");
  #dt.on_obstacle_detected_handler(lambda self, d : print("distance is %f " % d));
  dt.on_obstacle_detected_handler(lambda d : print("distance is %f " % d));
  dt.join();
  
  
# run the function
obstacle_detector_sample_usage();
