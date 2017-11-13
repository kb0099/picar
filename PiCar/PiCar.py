from ImageProcessor import ImageProcesor;
from ObstacleDetector import ObstacleDetector;
from Powertrain import Powertrain;
import car_config.py

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
                # 1. Is it a temporary obstacle?
                # 2. Can obstacle be avoided by turning around the obstacle?
                #
                
                ###
                ### Alternative logic for the whole process
                ### 
                
                # Place all sensors processing logic in threads
                # Register event handlers for each possible event in every sensor
                # Then in main():
                #   just setup the handlers.
                # events/handlers:
                #   - on_obstacle_within_threshold:     stop/pause the vehicle
                #   - on_obstacle_removed:              continue
                #   - on_lane_status_update:            steer vehicle accordingly
                #   - any other sensor logic:           handle appropriately

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
