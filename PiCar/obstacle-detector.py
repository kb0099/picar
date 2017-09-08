from __future__ import print_function;
import time;
import random;
import threading;
import types;

class ObstacleDetector(threading.Thread):
  "Uses sensors to detect obstacles"        
  def __init__(self, trigger_pin, echo_pin):
    threading.Thread.__init__(self)
    '''Callbacks to be handled when motion is detected'''
    self.on_obstacle_detected_handlers = []
    self.current_distance = 0;
    self.threshold = 0.4;

  def get_distance_to_obstacle():
      return self.current_distance;

  def set_distance_threshold(dt):
    '''used to trigger the callback'''
    self.threshold = dt;

  def is_closer_than(distance):
          pass;
    
  '''Each call adds that handler to be called when motion is detected'''
  def on_obstacle_detected_handler(self, handler):
    #self.on_obstacle_detected_handlers.append(types.MethodType(handler, self));
    self.on_obstacle_detected_handlers.append(handler);

  def run(self):
    print("run called.");
    while(True):
      time.sleep(1);
      self.current_distance = random.random()
      if(self.current_distance > 0.4):
        for h in self.on_obstacle_detected_handlers:
          h(self.current_distance);
      else:
        print("all good!");
          
# Sample usage
dt = ObstacleDetector(2,3);
print("before calling process_loop");
dt.start();
print( "after calling process_loop");
#dt.on_motion_detected_handler(lambda self, d : print("distance is %f " % d));
dt.on_obstacle_detected_handler(lambda d : print("distance is %f " % d));
dt.join();
