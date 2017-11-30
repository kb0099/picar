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
def acclerate(self):
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

        self.power_train        = Powertrain(left_fp, left_bp, left_en, right_fp, right_bp, right_en);
        self.obstacle_detector  = ObstacleDetector(front_trigger, frot_echo, front_threshold);
        self.image_processor    = ImageProcesor(camera_port_num);

    # decelerate could work by giving negative increment.
    def accelerate(self, increment):
        self.power_train.accelerate(increment);


    # change backward or forward : changes direction and stops
    def change_bf_direction(self, forward=True):
        if(SharedData.pi_status.is_set_forward != forward):
            SharedData.pi_status.is_set_forward = forward;
            self.stop();

    # let it stop on its own
    def stop(self):
        self.power_train.stop();


# global smart_car object
smart_car = SmartCar();

# extend
smart_car.power_train.accelerate = accelerate;

def handle_cmd(cmd):
    if(cmd == CMD_FORWARD):
        change_bf_direction()


    elif (cmd == CMD_BACKWARD):
        output = '{"result": "CMD_BACKWARD"}';
        pass;    

    elif(cmd == CMD_ACCELERATE):

    elif(cmd == CMD_DECELERATE):
        output = '{"result": "CMD_DECL"}';
        pass;

    elif(cmd == CMD_LEFT):
        output = '{"result": "CMD_LEFT"}';
        pass;

    elif(cmd == CMD_RIGHT):
        output = '{"result": "CMD_RIGHT"}';
        pass;

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

