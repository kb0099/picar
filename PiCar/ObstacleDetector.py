from __future__ import print_function;
import time;
import random;
import threading;
import types;
import RPi.GPIO as GPIO

class ObstacleDetector(threading.Thread):
  '''Uses sensors to detect obstacles'''
    
  def __init__(self, trigger_pin, echo_pin, distance_threshold):
    threading.Thread.__init__(self)
    self.trigger_pin  = trigger_pin;
    self.echo_pin     = echo_pin; 
    self.not_stopped  = True;
    
    #set GPIO direction (IN / OUT)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    
    '''Callbacks to be handled when obstacle is detected'''
    self.on_obstacle_detected_handlers = []
    self.current_distance = 0;
    '''distance threshold is used to trigger the handlers'''
    self.threshold = distance_threshold;
  
  def _measure_distance(self):
    '''should not be called manually (else, threading issues might occur)'''
    # set Trigger to HIGH
    GPIO.output(self.trigger_pin, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(self.trigger_pin, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(self.echo_pin) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(self.echo_pin) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    self.current_distance = (TimeElapsed * 34300) / 2
 
    return self.current_distance

  def get_distance_to_obstacle():
    '''just returns currrent_distance as run() updates current_distance automatically'''
    return self.current_distance;

  def set_distance_threshold(self, dt):
    '''used to trigger the callback'''
    self.threshold = dt;

  def is_within_threshold():
    return self.get_distance_to_obstacle() <= self.distance_threshold;
    
  '''Each call adds that handler to be called when obstacle is detected'''
  def on_obstacle_detected_handler(self, handler):
    #self.on_obstacle_detected_handlers.append(types.MethodType(handler, self));
    self.on_obstacle_detected_handlers.append(handler);

  def stop_thread(self):
    self.not_stopped = False;
    
  def run(self):
    print("Obstacle detector is running ..... ");
    try:
      t = threading.currentThread()
      while getattr(t, "do_run", True):
        self._measure_distance();
        if(self.current_distance <= self.threshold):
          for h in self.on_obstacle_detected_handlers:
            h(self.current_distance);
        else:
          print("all good!");      
        time.sleep(2);  # wait before making next measurement.
    except KeyboardInterrupt:
      return
          
# Sample usage
 
def handler_creator(dt):
  def handler1(d):
    print("distance is %f" % d);
    try:
      pass;
    except KeyboardInterrupt:
      dt.stop_thread();
  return handler1;

def obstacle_detector_sample_usage():
  dt = ObstacleDetector(2,3, 10);
  print("before calling process_loop");
  dt.start();
  print( "after calling process_loop");
  #dt.on_obstacle_detected_handler(lambda self, d : print("distance is %f " % d));
  
  # dt.on_obstacle_detected_handler(lambda d : print("distance is %f " % d));  
  dt.on_obstacle_detected_handler(handler_creator(dt));
  dt.join();
 
