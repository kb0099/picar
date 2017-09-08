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
        left_fp, left_bp, left_en,
        right_fp, right_bp, right_en,
        front_trigger, front_echo, front_distance_threshold
        back_trigger, back_echo, back_distance_threshold):

        self.power_train = Powertrain(left_fp, left_bp, left_en, right_fp, right_bp, right_en);
        self.obstacle_detector = ObstacleDetector(front_trigger, frot_echo, front_threshold);

    def start():
        try:
            while(True):
                if(self.obstacle_detector.get_distance_to_obstacle() < self.obstacle_detector.distance_threshold):
                    time.sleep(1);
                    continue;       # escape rest.
                # poll image analyzer
                # get turning direction and turn to that
                # Powertrain.steer(direction, left, right, etc.);

                # obstacle detector can execute handler(s) when obstacles are detected.
                # poll other sensors
                # and take action

        except KeyboardInterrupt:
            self.stop();

    def stop():
        # probably can call cleanup here
        # release all resources
        GPIO.cleanup();

    def pause():
        # PowerTrain.stop();


# if main function
#    car_object = PiCar();
#    car_object.Start(what_type_of_operation);
