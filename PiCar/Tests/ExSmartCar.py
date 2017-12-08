
import sys;
import time;
sys.path.append('..');
from car_config import *;
from DirMotor import DirMotor;
from SpeedMotor import SpeedMotor;
from ServerConstants import *;
from ex_shared_data import SD;

'''TODO:
    0. test controller by connecting to motors                  x
    1. implement adjustment functions if necessary
    2. integrate everything together
'''

class ExSmartCar:
    def __init__(self):
        self.dm = DirMotor(EX_DIRECTION_LEFT, EX_DIRECTION_RIGHT, EX_DIRECTION_PWM);
        self.sm = SpeedMotor(EX_SPEED_FORWARD, EX_SPEED_BACKWARD, EX_SPEED_PWM);
        #self.obstacle_detector  = ObstacleDetector(FTP, FEP, 10);
        #self.image_processor    = ImageProcesor(camera_port_num);

    # mult_factor = 1 for accelerate, and -1 for decelerate
    def accelerate(self, mult_factor = 1):
        new_dc = 0;
        if (SD.ps['sm_stopped'] == True and mult_factor == 1):
            #self.power_train.accelerate(SD.ps['default_duty_cycle']);
            new_dc = SD.ps['default_dc'];
            SD.ps['sm_stopped'] = False;
        else:
            new_dc  = SD.ps['sm_dc'] + mult_factor * SD.ps['dc_delta'];
            print "factor is ", mult_factor * SD.ps['dc_delta'];
            if(new_dc < SD.ps['min_sm_dc']):
                print "stopping .....";
                self.stop();
                SD.ps['sm_stopped'] = True;
                new_dc = 0;

        print "changing dc to: ", (new_dc);
        self.sm.change_dc(new_dc);      

    # change backward or forward : changes direction and stops
    def change_orientation(self, forward=True): 
        # clear turn
        SD.ps['turn_direction']               = 0;
        #self.dm.pwm.ChangeDutyCycle(0);
        if(SD.ps['headed_forward']       != forward):
            self.sm.change_dir(forward);
            self.stop();

    def update_turn_diection(self, delta): 
        turn_dir = SD.ps['turn_direction'] + delta;
        if (turn_dir < -0.9999):
            turn_dir = -0.99;
        elif(turn_dir > 0.9999):
            turn_dir = 0.99;
        
        self.dm.set_direction(turn_dir, abs(turn_dir)*100);
        print ("turn dir: ", turn_dir, "turn dc: ", abs(turn_dir)*100);
        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

    # let it stop on its own
    def stop(self):
        print ("stopping? ..");
        self.sm.stop();
        self.dm.reset(); # 

    def cleanup(self):
        print ("C => Cleaning up!")
        self.sm.cleanup();
        self.dm.cleanup();

    def handle_cmd(self, cmd):
        if(cmd == CMD_FORWARD):
            self.change_orientation(True);

        elif (cmd == CMD_BACKWARD):
            self.change_orientation(False);

        elif(cmd == CMD_ACCELERATE):
            print "Accelerating...";
            self.accelerate();

        elif(cmd == CMD_DECELERATE):
            print "decelerating...";
            self.accelerate(-1);

        elif(cmd == CMD_LEFT):
            self.update_turn_diection(-SD.ps['direction_delta']);

        elif(cmd == CMD_RIGHT):
            self.update_turn_diection(+SD.ps['direction_delta']);

        elif (cmd == CMD_STOP): # motors
            self.stop(); 

        elif (cmd == CMD_CLEANUP):
            self.cleanup();

        elif (cmd == CMD_CAL_LEFT):
            # if car goes more towards right
            #  we need to pull it left means decrease speed of right motor.
            if (SD.ps['right_motor_dc_adjustment'] > 0.1):
                SD.ps['right_motor_dc_adjustment'] -= 0.1;

        elif (cmd == CMD_CAL_RIGHT):
            if (SD.ps['left_motor_dc_adjustment'] > 0.1):
                SD.ps['left_motor_dc_adjustment'] -= 0.1;

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
