
# Imports
import RPi.GPIO as GPIO 

from ex_shared_data import SD;

# Set GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class DirMotor:
    """DirMotor class represents direction [-1, 1]
    """
    def __init__(self, left, right, enable_pin):
        # store pins
        self.left_pin       = left
        self.right_pin      = right
        self.pwm_pin        = enable_pin

        GPIO.setup( [self.left_pin, self.right_pin, self.pwm_pin], GPIO.OUT, initial=False)
        self.pwm = GPIO.PWM(self.pwm_pin, SD.ps['pwm_freq'])
        self.pwm.start(0.0)

    def set_direction(self, direction = 0.0, duty_cycle=40.0):
        SD.ps['turn_direction'] = direction;
        if (direction < 0):
            self.left(duty_cycle);
        elif (direction > 0):
            self.right(duty_cycle);
        else:
            self.reset();


    def left(self, duty_cycle=40.0):
        GPIO.output(self.left_pin, True)
        GPIO.output(self.right_pin, False)
        self.change_dc(duty_cycle);

    def right(self, duty_cycle=40.0):
        GPIO.output(self.left_pin, False)
        GPIO.output(self.right_pin, True)
        self.change_dc(duty_cycle)

    def reset(self):
        self.change_dc(0.0)

    def cleanup(self):
        self.pwm.stop();
        GPIO.cleanup( [self.left_pin, self.right_pin, self.pwm_pin])

    def change_dc(self, dc):
        if(dc > SD.ps['max_dm_dc']):
            dc = SD.ps['max_dm_dc'];
        SD.ps['dm_dc'] = dc;
        self.pwm.ChangeDutyCycle(dc);
