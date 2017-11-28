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
    base_duty_cycle = 45
    try:
	
        #pt.turn_intensity(base_duty_cycle, base_intensity)
	#time.sleep(2)
	#pt.turn_intensity(base_duty_cycle, -80)
	#time.sleep(3)
	#pt.turn_intensity(base_duty_cycle, 80)
	#time.sleep(3)
        while(True):
	    pt.stop()
	    time.sleep(.1)
	    print("\n\n")
            adjustment = imgpr.check_status() * 1000 + 100
            print("Adjustment: {0}".format(adjustment))
            if adjustment == 17 * 1000 + 100:
                print("Unexpected resolution of image processing method.\n")
            else:
                pt.turn_intensity(base_duty_cycle, (base_intensity + adjustment))
	    time.sleep(.1)


    except KeyboardInterrupt:
        stop()

def stop():
    # probably can call cleanup here
    # release all resources
    pt.stop()
    imgpr.cleanup()
    GPIO.cleanup()

start()
