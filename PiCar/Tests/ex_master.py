import ex_server;
from ex_shared_data import SD;
import threading, random;
from ServerConstants import *;
from ExSmartCar import ExSmartCar;

# SmartCar
import sys;
import time;
sys.path.append('..');

# global smart_car object
smart_car = ExSmartCar(); 

# Main execution
if __name__ == "__main__":
    t1 = threading.Thread(target=ex_server.run_server);
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
            if not SD.command_list.empty():
                cmd = SD.command_list.get();
                print "In master, key_code: ", cmd;
                smart_car.handle_cmd(cmd);
                print "success: handle_cmd";
            
            # for test:
            SD.ps['od_back_distance'] = random.randint(2, 50);

    except KeyboardInterrupt:
        smart_car.cleanup();


