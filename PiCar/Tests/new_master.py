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
    0. test controller by connecting to motors                  x
    1. implement adjustment functions if necessary
    2. integrate everything together
'''

# some methods need to be added on motors or powertrain
# on powertrain
def acclerate(self, increment):
    # left motor
    new_dc = SharedData.pi_status['left_motor_dc'] + increment;
    self.left.pwm.ChangeDutyCycle(new_dc); 

    # right motor
    new_dc = SharedData.pi_status['right_motor_dc'] + increment;
    self.right.pwm.ChangeDutyCycle(new_dc);

class SmartCar:
    def __init__(self,
        camera_port_num = 1,
        left_fp = LFP, left_bp = LBP, left_en = LEP,
        right_fp = RFP, right_bp = RBP, right_en = REP,
        front_trigger= FTP, front_echo = FEP, front_distance_threshold=10):

        self.power_train         = Powertrain(left_fp, left_bp, left_en, right_fp, right_bp, right_en);
        #self.obstacle_detector  = ObstacleDetector(front_trigger, frot_echo, front_threshold);
        #self.image_processor    = ImageProcesor(camera_port_num);

    # incr_factor = 1 for accelerate, and -1 for decelerate
    def accelerate(self, incr_factor = 1):
        new_dc = 0;
        new_dc_left = 0;        # without the adjustment
        new_dc_right = 0;       # without the adjustment
        if (SharedData.pi_status['motors_stopped'] == True and incr_factor == 1):
            #self.power_train.accelerate(SharedData.pi_status['default_duty_cycle']);
            new_dc = SharedData.pi_status['default_duty_cycle'];
            print "changing dc to: ", new_dc;
            new_dc_left     = new_dc; # *SharedData.pi_status['left_motor_dc_adjustment'];
            new_dc_right    = new_dc; #*SharedData.pi_status['right_motor_dc_adjustment'];
            SharedData.pi_status['motors_stopped'] = False;
        else:
            #self.power_train.accelerate(SharedData.pi_status['default_duty_cycle']);
            print "factor is ", incr_factor * SharedData.pi_status['dc_delta'];
            new_dc_left = SharedData.pi_status['left_motor_dc'] + incr_factor * SharedData.pi_status['dc_delta'];
            new_dc_right = SharedData.pi_status['left_motor_dc'] + incr_factor * SharedData.pi_status['dc_delta'];
            if(new_dc_left < 10 and new_dc_right < 10):
                print "stopping left .....";
                self.stop();
                SharedData.pi_status['motors_stopped'] = True;
                new_dc_left = 0;        # without the adjustment
                new_dc_right = 0;       # without the adjustment
            else:
                new_dc_left = 0 if new_dc_left < 10 else new_dc_left;
                new_dc_right = 0 if new_dc_right < 10 else new_dc_right;

        # update at last
        # update global
        # use un-adjusted original values!
        SharedData.pi_status['left_motor_dc']       = new_dc_left;               
        SharedData.pi_status['right_motor_dc']      = new_dc_right;   

        # adjust now!     
        new_dc_left = new_dc_left   * SharedData.pi_status['left_motor_dc_adjustment'];
        new_dc_right = new_dc_right * SharedData.pi_status['right_motor_dc_adjustment'];

        print "changing dc to: ", (new_dc_left, new_dc_right);

        self.power_train.left.pwm.ChangeDutyCycle(new_dc_left);         
        self.power_train.right.pwm.ChangeDutyCycle(new_dc_right);        

    # change backward or forward : changes direction and stops
    def set_forward_direction(self, forward=True):
        self.power_train.left.change_dir(forward);
        self.power_train.right.change_dir(forward);

        SharedData.pi_status['direction']               = 0;
        if(SharedData.pi_status['headed_forward']       != forward):
            SharedData.pi_status['headed_forward']      = forward;
            self.stop();

    def change_left_right(self, dir):
        SharedData.pi_status['direction']               -= direction_delta;

    # let it stop on its own
    def stop(self):
        print ("stopping? ..");
        SharedData.pi_status['left_motor_dc']   = 0;
        SharedData.pi_status['right_motor_dc']  = 0;
        self.power_train.stop();

    def cleanup(self):
        print ("C => Cleaning up!")
        self.power_train.cleanup();

    def handle_cmd(self, cmd):
        if(cmd == CMD_FORWARD):
            self.set_forward_direction(True);

        elif (cmd == CMD_BACKWARD):
            self.set_forward_direction(False);
            pass;    

        elif(cmd == CMD_ACCELERATE):
            print "Accelerating...";
            self.accelerate();

        elif(cmd == CMD_DECELERATE):
            print "decelerating...";
            self.accelerate(-1);

        elif(cmd == CMD_LEFT):
            SharedData.pi_status['direction']           -= SharedData.pi_status['direction_delta'] ;
            pass;

        elif(cmd == CMD_RIGHT):
            SharedData.pi_status['direction']           += SharedData.pi_status['direction_delta'] ;
            pass;

        elif (cmd == CMD_STOP): # motors
            self.stop();

        elif (cmd == CMD_CLEANUP):
            self.cleanup();

        elif (cmd == CMD_CAL_LEFT):
            # if car goes more towards right
            #  we need to pull it left means decrease speed of right motor.
            if (SharedData.pi_status['right_motor_dc_adjustment'] > 0.1):
                SharedData.pi_status['right_motor_dc_adjustment'] -= 0.1;

        elif (cmd == CMD_CAL_RIGHT):
            if (SharedData.pi_status['left_motor_dc_adjustment'] > 0.1):
                SharedData.pi_status['left_motor_dc_adjustment'] -= 0.1;

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
    
    try:
        while True:
            # 0. Check for server commands
            # if cmd, execute them
            #   0.1. Check for obstacles
            #       if obstacles, pause
            # 1. If no server commands, do image processing()
            #   1.1 check, obstacles, stops and run
            #   
            if not SharedData.command_list.empty():
                cmd = SharedData.command_list.get();
                print "the master: ", cmd;
                smart_car.handle_cmd(cmd);
                print "handled?";
            
            # for test:
            SharedData.pi_status['od_back_distance'] = random.randint(2, 50);
    except KeyboardInterrupt:
        smart_car.cleanup();


