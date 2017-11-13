#!python2
from ImageProcessor import ImageProcessor;
from powertrain import Powertrain;
from car_config import *
import time

def start():
    imgpr = ImageProcessor(0, 1)
    imgpr.init_camera()
    pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
    # self.image_processor.start();
    try:
        pt.forward(100)
        while(True):
            status = imgpr.check_status()
            print("Status: {0}".format(status))
            if status != 5:
                pt.turn_intensity(100, status)
            time.sleep(.2)


    except KeyboardInterrupt:
        stop()

def stop():
    # probably can call cleanup here
    # release all resources
    pt.stop()
    image_processor.cleanup()
    GPIO.cleanup()

start()
