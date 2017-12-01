from Queue import Queue;

class SharedData:
    #   ''' static class with shared data '''
    command_list                    = Queue();  # server to master
    #pi_status                      = Queue();  # master to server

    # complete info/status
    pi_status =  {
        # whether stopped
        'default_duty_cycle'            : 15,
        'current_duty_cycle'            : 0,       # powertrain duty cycle or max duty-cycle
        'motors_stopped'                : True,
        'dc_delta'                      : 5,       # duty cycle increment

        'headed_forward'                : True,    # set to go forward
        'direction'                     : 0.0,     # 0.0 straight, -1 left, +1 right.
        'direction_delta'               : 0.1,     # left/right change value

        # left_motor
        'left_motor_dc'                 : 0,       # without adjustent
        'left_motor_dc_adjustment'      : 1,       # factor

        # right_motor
        'right_motor_dc'                : 0,       # without adjustment
        'right_motor_dc_adjustment'     : 0.8,

        # "od" stands for object detector
        'od_front_distance'             : 0,
        'od_back_distance'              : 0,

        # image processor
        'imgp_turn_direction'           : 0,        # 0 for straight, -1 for complete left, +1 for complete right?

        # stop sign detector
        'ss_is_stop_sign_present'       : False
        }
