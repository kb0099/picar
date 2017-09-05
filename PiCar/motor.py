
import RPi.GPIO as GPIO


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class Motor:
    "Represents a single PWM motor"

    def __init__(self, forward_pin, backward_pin, enable_pin):
        self.fp     = forward_pin;
        self.bp     = backward_pin;
        self.pwm    = GPIO.PWM(enable_pin, 100);

        GPIO.setup(forward_pin, GPIO.OUT);
        GPIO.setup(backward_pin, GPIO.OUT);

    def forward(duty_cycle=100):
        GPIO.output(self.fp, True)
        GPIO.output(self.bp, False)
        self.pwm.setDutycycle(dyty_cycle);
        
    def backward(duty_cyele=100):
        self.pwm.setDutycycle(dyty_cycle);
        pass;
    
    def halt():
        self.pwm.setDutycycle(0);
        pass;


