#!python2
from ImageProcessor import ImageProcessor
from powertrain import Powertrain
from car_config import *
import time
import RPi.GPIO as GPIO

imgpr = ImageProcessor(0, 1)
imgpr.init_camera()
pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)

def start():
    # self.image_processor.start();
    base_intensity = 0
    left_duty_cycle = 35
    right_duty_cycle = 35
    try:
    	lastDir = 0
        while(True):
            # Direction: -1 = left, 1 = right, 0 = no change
            direction = imgpr.check_status()
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
            # Recovery
            elif direction == 3:
                # Reverse Direction
                if lastDir == -1:
                    # Turn Right
                    pt.turn_intensity(left_duty_cycle, 100)
                elif lastDir == 1:
                    # Turn Left
                    pt.turn_intensity(right_duty_cycle, -100)
                # Call recovery function
                # Runs until 2 lanes are visible again.
                lastDir = imgpr.recovery()







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
