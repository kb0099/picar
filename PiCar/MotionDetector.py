
from __future__ import print_function;
import time;
import random;
import threading;
import types;

class MotionDetector(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    '''Callbacks to be handled when motion is detected'''
    self.on_motion_detected_handlers = []
    self.distance = 0;
    self.threshold = 0.4;
  
  '''Each call adds that handler to be called when motion is detected'''
  def on_motion_detected_handler(self, handler):
    #self.on_motion_detected_handlers.append(types.MethodType(handler, self));
    self.on_motion_detected_handlers.append(handler);

  def run(self):
    print("run called.");
    while(True):
      time.sleep(1);
      self.distance = random.random()
      if(self.distance > 0.4):
        for h in self.on_motion_detected_handlers:
          h(self.distance);
      else:
        print("all good!");
          
# Sample usage
def motion_detector_sample_usage():
  dt = MotionDetector();
  print("before calling process_loop");
  dt.start();
  print( "after calling process_loop");
  #dt.on_motion_detected_handler(lambda self, d : print("distance is %f " % d));
  dt.on_motion_detected_handler(lambda d : print("distance is %f " % d));
  dt.join();

