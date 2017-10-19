#
# Sample demo for obstacle detector (od)
#

# sample function
def obstacle_detector_sample_usage():
  dt = ObstacleDetector(2,3, 10);
  print("before calling process_loop");
  dt.start();
  print( "after calling process_loop");
  #dt.on_obstacle_detected_handler(lambda self, d : print("distance is %f " % d));
  dt.on_obstacle_detected_handler(lambda d : print("distance is %f " % d));
  dt.join();
  
  
# run the function
obstacle_detector_sample_usage();
