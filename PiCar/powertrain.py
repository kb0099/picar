
class Powertrain:
    "Uses motors to drive the PiCar"
    def __init__(left_wheel_forward_pin, left_wheel_backward_pin, right_wheel_forward_pin, right_wheel_backward_pin):
        self.left_motor = Motor(2, 14, 15);
        self.right_motor = Motor(3, 4, 19);

    def forward(speed_or_duty_cycle, direction):
        pass;

    def reverse(speed_or_duty_cycle);
        pass;

    def turn(left_motor_speed, right_motor_speed):
        pass;

    # -1 will be max negative +1 will be max positive . 
    def turn_right():
        pass;

    def turn_left():
        pass;

    def stop():
        pass;
