import server_test;
from shared_data import SharedData;
import threading, random;

from ServerConstants import *;

# SmartCar
import sys;
import time;
sys.path.append('..');
from motor import Motor;
from car_config import *;
from powertrain import Powertrain;



'''TODO:
    0. test controller by connecting to motors
    1. implement adjustment functions if necessary
    2. integrate everything together
'''

# some methods need to be added on motors or powertrain
# on powertrain
def acclerate(self, increment):
    # left motor
    new_dc = SharedData.pi_status['left_motor_dc'] + increment;
    self.left.pwm.changeDutyCycle(new_dc); 

    # right motor
    new_dc = SharedData.pi_status['right_motor_dc'] + increment;
    self.right.pwm.changeDutyCycle(new_dc);


class SmartCar:
    def __init__(self,
        camera_port_num,
        left_fp, left_bp, left_en,
        right_fp, right_bp, right_en,
        front_trigger, front_echo, front_distance_threshold):

        self.power_train         = Powertrain(left_fp, left_bp, left_en, right_fp, right_bp, right_en);
        #self.obstacle_detector  = ObstacleDetector(front_trigger, frot_echo, front_threshold);
        #self.image_processor    = ImageProcesor(camera_port_num);

    # incr_factor = 1 for accelerate, and -1 for decelerate
    def accelerate(self, incr_factor = 1):
        if (SharedData.pi_status['motor_stopped']):
            #self.power_train.accelerate(SharedData.pi_status['default_duty_cycle']);
            self.power_train.left.pwm.changeDutyCycle(SharedData.pi_status['default_duty_cycle']); 
            self.power_train.right.pwm.changeDutyCycle(SharedData.pi_status['default_duty_cycle']); 
        else:
            #self.power_train.accelerate(SharedData.pi_status['default_duty_cycle']);
            new_dc = SharedData.pi_status['left_motor_dc'] + incr_factor * SharedData.pi_status['dc_delta'];
            if(new_dc < 10):
                self.stop();
            else:            
                self.power_train.left.pwm.changeDutyCycle(new_dc);
                self.power_train.right.pwm.changeDutyCycle(new_dc); 

    # change backward or forward : changes direction and stops
    def set_forward_direction(self, forward=True):
        SharedData.pi_status['direction']               = 0;
        if(SharedData.pi_status['headed_forward']       != forward):
            SharedData.pi_status['headed_forward']      = forward;
            self.stop();

    def change_left_right(self, dir):
        SharedData.pi_status['direction']               -= direction_delta;

    # let it stop on its own
    def stop(self):
        self.power_train.stop();

    def cleanup(self):
        self.power_train.cleanup();

    def handle_cmd(self, cmd):
        if(cmd == CMD_FORWARD):
            self.set_forward_direction(True);

        elif (cmd == CMD_BACKWARD):
            self.set_forward_direction(False);
            pass;    

        elif(cmd == CMD_ACCELERATE):
            self.acclerate();

        elif(cmd == CMD_DECELERATE):
            self.accelerate(-1);

        elif(cmd == CMD_LEFT):
            SharedData.pi_status['direction']           -= direction_delta;
            pass;

        elif(cmd == CMD_RIGHT):
            SharedData.pi_status['direction']           += direction_delta;
            pass;

        elif (cmd == CMD_STOP):
            self.stop();

        elif (cmd == CMD_CLEANUP):
            self.cleanup();

        elif (cmd == CMD_TERMINATE):
            '''
            self.wfile.write("closing...");
            self.stopped = True;
            self.server.shutdown();
            self.socket.close()
            print ("server: closing...");
            '''
            pass;
            return;



# global smart_car object
smart_car = SmartCar();

# extend
# smart_car.power_train.accelerate = accelerate;

# Main execution
if __name__ == "__main__":
    t1 = threading.Thread(target=server_test.run_server);
    t1.start();
    
    while True:
        # 0. Check for server commands
        # if cmd, execute them
        #   0.1. Check for obstacles
        #       if obstacles, pause
        # 1. If no server commands, do image processing()
        #   1.1 check, obstacles, stops and run
        #   
        if not SharedData.command_list.empty():
            print "the master: ", SharedData.command_list.get();
        
        # for test:
        SharedData.pi_status['od_back_distance'] = random.randint(2, 50);


