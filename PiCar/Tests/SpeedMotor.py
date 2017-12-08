
# Imports
import RPi.GPIO as GPIO 

from ex_shared_data import SD;

# Set GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class SpeedMotor:
    """Represents speed motor.
    """
    def __init__(self, forward_pin, backward_pin, enable_pin):
        # store pins
        self.left_pin = forward_pin
        self.right_pin = backward_pin
        self.pwm_pin = enable_pin

        GPIO.setup( [self.left_pin, self.right_pin, self.pwm_pin], GPIO.OUT, initial=False)

        # frequency (Hz) second parameter
        self.pwm = GPIO.PWM(self.pwm_pin, SD.ps['pwm_freq'])

        self.pwm.start(0.0)

        # initial direction forward
        self.change_dir(True);

    def forward(self, duty_cycle=40.0):
        GPIO.output(self.left_pin, True)
        GPIO.output(self.right_pin, False)
        self.change_dc(duty_cycle)

    def backward(self, duty_cycle=40.0):
        GPIO.output(self.left_pin, False)
        GPIO.output(self.right_pin, True)
        self.change_dc(duty_cycle)

    def stop(self):
        self.change_dc(0.0)
        SD.ps['sm_stopped'] = True;

    def cleanup(self):
        self.pwm.stop();
        GPIO.cleanup( [self.left_pin, self.right_pin, self.pwm_pin]);
        SD.ps['gpio_cleaned'] = True;

    def change_dir(self, forward=True):
        self.change_dc(0.0);
        GPIO.output(self.left_pin, forward)
        GPIO.output(self.right_pin, not forward)
        SD.ps['headed_forward'] = forward;

    def change_dc(self, dc):
        if(dc > SD.ps['max_sm_dc']):
            dc = SD.ps['max_sm_dc'];
        SD.ps['sm_dc'] = dc;
        self.pwm.ChangeDutyCycle(dc);