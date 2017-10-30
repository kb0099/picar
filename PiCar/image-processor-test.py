#!python2
from ImageProcessor import ImageProcesor;
from Powertrain import Powertrain;
import car_config.py

def start(self):
    imgpr = ImageProcesor(0, 1)
    pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
    # self.image_processor.start();
    try:
        pt.forward(100)
        while(True):
            status = imgpr.check_status()
            print("Status: {0}".format(status))
            pt.turn_intensity(100, status)

    except KeyboardInterrupt:
        self.stop();

def stop():
    # probably can call cleanup here
    # release all resources
    self.image_processor.cleanup();
    GPIO.cleanup();

def pause():
    PowerTrain.stop();


# if main function
#    car_object = PiCar();
#    car_object.Start(what_type_of_operation);
