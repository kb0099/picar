import server_test;
from shared_data import SharedData;
import threading, random;


from ServerConstants import *;
'''TODO:
    0. test controller by hooking to motors
    1. implement adjustment functions if necessary
    2. integrate everything together
'''

def handle_cmd(cmd):
    if(cmd == CMD_FORWARD):
        output = '{"result": "CMD_FORWARD"}';    # choose between threading, ipc, or multiprocessing

    elif (cmd == CMD_BACKWARD):
        output = '{"result": "CMD_BACKWARD"}';
        pass;    

    elif(cmd == CMD_ACCELERATE):
        output = '{"result": "CMD_ACCL"}';
        pass;  

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

