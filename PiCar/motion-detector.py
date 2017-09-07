
from __future__ import print_function;
import time;
import random;
import threading;
import types;

class MotionDetector(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    '''Event to be handled when motion is detected'''
    self.on_motion_detected_handlers = []
  
  def run(self):
    print("run called.");
    while(True):
      time.sleep(1);
      detected = random.random()
      if(detected > 0.4):
        if(self.on_motion_detected):
          self.on_motion_detected(detected)
        else:
          print("event not initialized")
      else:
        print("all good!");
          
dt = Detector();
print("before calling process_loop");
dt.start();
print( "after calling process_loop");
dt.on_motion_detected = types.MethodType(lambda self, d : print("distance is %f " % d), dt);
dt.join();


