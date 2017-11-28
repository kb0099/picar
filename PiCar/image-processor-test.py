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
    base_intensity = -10
    try:
        pt.turn_intensity(60, base_intensity)
        while(True):
            adjustment = imgpr.check_status()
            print("Status: {0}".format(status))
            if status == 5:
                print("Unexpected resolution of image processing method.\n")
            else:
                pt.turn_intensity(60, (base_intensity + adjustment))
            time.sleep(.2)


    except KeyboardInterrupt:
        stop()

def stop():
    # probably can call cleanup here
    # release all resources
    pt.stop()
    imgpr.cleanup()
    GPIO.cleanup()

start()
