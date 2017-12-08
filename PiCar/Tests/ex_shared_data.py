from Queue import Queue;

# Shared Data == SD
class SD:
    #   ''' static class with shared data '''
    command_list                    = Queue();  # server to master
    #ps                      = Queue();  # master to server

    # complete info/status :: ps == pi_status
    ps =  {
        'pwm_freq': 200,

        # speed motor
        'default_dc'                    : 15,
        'sm_dc'                         : 0,        # powertrain duty cycle or max duty-cycle
        'dc_delta'                      : 5,        # duty cycle increment/decrement
        'sm_stopped'                    : True,     # ===> current_dc === 0                                       ***unneessary?
        'min_sm_dc'                     : 10,       # minimum dc, below this will stop motors.
        'max_sm_dc'                     : 70,

        # direction motor
        'turn_direction'                : 0.0,     # 0.0 straight, -1 left, +1 right.
        'headed_forward'                : True,    # orientation/set to go forward
        'direction_delta'               : 0.2,     # left/right change value                                         ***unneessary?
        'min_dm_dc'                     : 0.15,
        'max_dm_dc'                     : 40,
        'dm_dc'                         : 0,

        # "od" stands for object detector
        'od_front_distance'             : 0, 
        'od_back_distance'              : 0,

        # image processor
        'imgp_turn_direction'           : 0,        # 0 for straight, -1 for complete left, +1 for complete right?

        # stop sign detector
        'ss_is_stop_sign_present'       : False,

        'gpio_cleaned': False,
        }
