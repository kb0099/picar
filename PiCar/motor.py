
import RPi.GPIO as GPIO


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class Motor:
    "Represents a single PWM motor"

    def __init__(self, forward_pin, backward_pin):
        self.fp     = forward_pin;
        self.bp     = backward_pin;
        self.pwm    = GPIO.PWM(self.fp, 100);

        GPIO.setup(forward_pin, GPIO.OUT);
        GPIO.setup(backward_pin, GPIO.OUT);

    def forward(duty_cycle=100):
        self.pwm.setDutycycle(dyty_cycle);
        pass;

    def backward(duty_cyele=100):
        self.pwm.setDutycycle(dyty_cycle);
        pass;
    
    def halt():
        self.pwm.setDutycycle(0);
        pass;


class Powertrain:
    "Uses motors to drive the PiCar"
    def __init__(left_wheel_forward_pin, left_wheel_backward_pin, right_wheel_forward_pin, right_wheel_backward_pin):
        pass;

class ObstacleDetector:
    "Uses sensors to detect obstacles"
    def __init__(trigger_pin, echo_pin):
        pass;

class ImageAnalyzer:
    "Uses camera to process images"
    def __init(camera_number):
        pass;

class PiCar:
    " Represents a "
    def __init__(self, left_fp, left_bp, right_fp, right_bp, front_trigger, front_echo, back_trigger, back_echo):
        self.power_train = Powertrain(left_fp, left_bp, right_fp, right_bp);

    def start():
        pass;

    