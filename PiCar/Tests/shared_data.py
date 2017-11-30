from Queue import Queue;

class SharedData:
    #   ''' static class with shared data '''
    command_list                    = Queue();  # server to master
    #pi_status                      = Queue();  # master to server

    # complete info/status
    pi_status =  {
        # whether stopped
        'motors_stopped'             : True,
        'forward'                    : True,    # set to go forward

        # left_motor
        'left_motor_dc'              : 0,
        'left_motor_dc_adjustment'   : 0,

        # right_motor
        'right_motor_dc'             : 0,
        'right_motor_dc_adjustment'  : 0,

        # "od" stands for object detector
        'od_front_distance'          : 0,
        'od_back_distance'           : 0,

        # image processor
        'imgp_turn_direction'        : 0,        # 0 for straight, -1 for complete left, +1 for complete right?

        # stop sign detector
        'ss_is_stop_sign_present'    : False
        }
