
import RPi.GPIO as GPIO


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class Motor:
    "Represents a single motor"

    def __init__(self, forward_pin, backward_pin):
        self.fp = forward_pin;
        self.bp = backward_pin;

        GPIO.setup(forward_pin, GPIO.OUT);
        GPIO.setup(backward_pin, GPIO.OUT);

    def forward():
        pass;
    def backward():
        pass;
    