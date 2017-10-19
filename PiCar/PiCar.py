from ImageProcessor import ImageProcesor;
from ObstacleDetector import ObstacleDetector;
from Powertrain import Powertrain;

class PiCar:
    '''
    Represents the topmost class. *_fp and *_bp stand for forward direction 
    pin (A) and backdirection pin (B). *_en stands for enable *_trigger and *_echo 
    are for ultrasonic sensor. 
    '''
    def __init__(self,
        camera_port_num,
        left_fp, left_bp, left_en,
        right_fp, right_bp, right_en,
        front_trigger, front_echo, front_distance_threshold
        back_trigger, back_echo, back_distance_threshold):

        self.power_train = Powertrain(left_fp, left_bp, left_en, right_fp, right_bp, right_en);
        self.obstacle_detector = ObstacleDetector(front_trigger, frot_echo, front_threshold);
        self.image_processor = ImageProcesor(camera_port_num);

    def start(self):
        self.obstacle_detector.start();
        # self.image_processor.start();
        try:
            while(True):
                if(self.obstacle_detector.is_within_threshold()):
                    self.pause();
                    time.sleep(1);
                    continue;       # escape rest.
                # get status from image processor // get turning direction and turn to that 
                # status from image processor === [range of -1 to 1, and curviness or speed factor 0 to 1]
                self.power_train.steer(self.image_processor.check_status());
                
                # poll other sensors
                # and take action
                
                #
                # Other logic that needs to be implemented.
                # 

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
