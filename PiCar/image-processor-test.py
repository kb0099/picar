#!python2
from ImageProcessor import ImageProcessor
from powertrain import Powertrain
from Ultrasonic import Ultrasonic
from car_config import *
import time
import RPi.GPIO as GPIO

imgpr = ImageProcessor(0, 0)
imgpr.init_camera()
pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
sensor = Ultrasonic()

def start():
    # self.image_processor.start();
    base_intensity = 0
    left_duty_cycle = 45
    right_duty_cycle = 45
    try:
    	lastDir = 1
        while(True):
            distance = sensor.distance()
            if distance < 20:
                pt.stop()
                #print(distance)
                continue
            #pt.stop()
            #time.sleep(.1)
            # Direction: -1 = left, 1 = right, 0 = no change
            direction = imgpr.check_status()
            #print(direction)
            if direction == -1:
                # Turn left
                pt.turn_intensity(right_duty_cycle, -100)
                lastDir = -1
            elif direction == 1:
                # Turn right
                pt.turn_intensity(left_duty_cycle, 100)
                lastDir = 1
            elif direction == 0:
                if lastDir == -1:
                    # Turn Left
                    pt.turn_intensity(right_duty_cycle, -100)
                elif lastDir == 1:
                    # Turn Right
                    pt.turn_intensity(left_duty_cycle, 100)
            # Switch Directions
            elif direction == 2:
                if lastDir == -1:
                    # Turn Right
                    pt.turn_intensity(left_duty_cycle, 100)
                    lastDir = 1
                elif lastDir == 1:
                    # Turn Left
                    pt.turn_intensity(right_duty_cycle, -100)
                    lastDir = -1
                imgpr.recovery(sensor, pt)
            # Recovery
            elif direction == 3:
                # Reverse Direction
                if lastDir == 1:
                    # Turn Right
                    pt.turn_intensity(left_duty_cycle, 100)
                elif lastDir == -1:
                    # Turn Left
                    pt.turn_intensity(right_duty_cycle, -100)
                # Call recovery function
                # Runs until 2 lanes are visible again.
                lastDir = imgpr.recovery(sensor, pt)
            #time.sleep(.13)







            #print("Adjustment: {0}".format(adjustment))
         #    if adjustment == 17 * 1000 or adjustment == 0:
         #        #print("Unexpected resolution of image processing method.\n")
         #        #pt.turn_intensity(base_duty_cycle, (base_intensity + lastAdj))
         #        adjustment = lastAdj
         #    else:
         #        #pt.turn_intensity(base_duty_cycle, (base_intensity + adjustment))
         #        lastAdj = adjustment
         #    if adjustment > 0:
         #        #pt.left_wheel(left_duty_cycle)
         #        pt.turn_intensity(left_duty_cycle, (base_intensity + adjustment))
         #    else:
         #        #pt.right_wheel(right_duty_cycle)
         #        pt.turn_intensity(right_duty_cycle, (base_intensity + adjustment))
    	    # #time.sleep(.1)


    except KeyboardInterrupt:
        stop()

def stop():
    # probably can call cleanup here
    # release all resources
    pt.stop()
    imgpr.cleanup()
    GPIO.cleanup()

start()
