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
        #pt.turn_intensity(base_duty_cycle, base_intensity)
    	#time.sleep(2)
    	#pt.turn_intensity(base_duty_cycle, -80)
    	#time.sleep(3)
    	#pt.turn_intensity(base_duty_cycle, 80)
    	#time.sleep(3)
        #time.sleep(5)
    	lastAdj = 0
        while(True):
    	    #pt.stop()
    	    #time.sleep(.1)
    	    #print("\n\n")
            adjustment = imgpr.check_status() * 1000
            #print("Adjustment: {0}".format(adjustment))
            if adjustment == 17 * 1000 or adjustment == 0:
                #print("Unexpected resolution of image processing method.\n")
                #pt.turn_intensity(base_duty_cycle, (base_intensity + lastAdj))
                adjustment = lastAdj
            else:
                #pt.turn_intensity(base_duty_cycle, (base_intensity + adjustment))
                lastAdj = adjustment
            if adjustment > 0:
                #pt.left_wheel(left_duty_cycle)
                pt.turn_intensity(left_duty_cycle, (base_intensity + adjustment))
            else:
                #pt.right_wheel(right_duty_cycle)
                pt.turn_intensity(right_duty_cycle, (base_intensity + adjustment))
    	    #time.sleep(.1)


    except KeyboardInterrupt:
        stop()

def stop():
    # probably can call cleanup here
    # release all resources
    pt.stop()
    imgpr.cleanup()
    GPIO.cleanup()

start()
