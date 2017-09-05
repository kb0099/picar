
class PiCar:
    " Represents a "
    def __init__(self, left_fp, left_bp, right_fp, right_bp, front_trigger, front_echo, back_trigger, back_echo):
        self.power_train = Powertrain(left_fp, left_bp, right_fp, right_bp);

    def start():
        # poll image analyzer
        # poll obstacle detector
        # poll other sensors
        # and take action
        pass;

    def stop():
        # probably can call cleanup here
        pass;

    def cleanup():
        # 
        # release all resources
        GPIO.cleanup();





# if main function
#    car_object = PiCar();
#    car_object.Start(what_type_of_operation);
