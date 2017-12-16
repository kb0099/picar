#!python2
from car_config import *
import time
import RPi.GPIO as GPIO

class Ultrasonic:

    def __init__(self):
        self.trigger_pin  = TRIGGER_PIN
        self.echo_pin     = ECHO_PIN
        
        #set GPIO direction (IN / OUT)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def distance(self):
        '''
        Uses ultrasonic sensor to get distance to the nearest obstacle.
        '''
        # set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)
     
        # set Trigger after 0.01ms to LOW 
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
     
        StartTime = 0
        StopTime = 0
     
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
        distance = (TimeElapsed * 34300) / 2
     
        return distance