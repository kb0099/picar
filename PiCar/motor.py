"""Motor class to configure and use motors connected to GPIO pins.
"""

# Imports
import RPi.GPIO as GPIO

# Set GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class Motor:
    """Represents a single motor. Speed is set through PWM.
    """

    def __init__(self, forward_pin, backward_pin, enable_pin):
        """Constructor.

        Args:
            forward_pin (int): GPIO pin connected to motor's forward pin.
            backward_pin (int): GPIO pin connected to motor's backward pin.
            enable_pin (int): GPIO pin connected to motor's enable pin
        """
        # store pins
        self.frwd_p = forward_pin
        self.bkwd_p = backward_pin
        self.enbl_p = enable_pin

        GPIO.setup( [self.frwd_p, self.bkwd_p, self.enbl_p], GPIO.OUT, initial=False)

        # frequency (Hz) second parameter
        self.pwm = GPIO.PWM(self.enbl_p, 150)

        self.pwm.start(0.0)

    def forward(self, duty_cycle=100.0):
        """Drive the motor forward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 100.0.
        """
        GPIO.output(self.frwd_p, True)
        GPIO.output(self.bkwd_p, False)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def backward(self, duty_cycle=100.0):
        """Drive the motor backward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 100.0.
        """
        GPIO.output(self.frwd_p, False)
        GPIO.output(self.bkwd_p, True)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def brake(self):
        """Lock the motor to act as brake.
        """
        GPIO.output(self.frwd_p, True)
        GPIO.output(self.bkwd_p, True)
        self.pwm.ChangeDutyCycle(100.0)

    def off(self):
        """Disable power to motor to coast.
        """
        GPIO.output(self.frwd_p, False)
        GPIO.output(self.bkwd_p, False)
        self.pwm.ChangeDutyCycle(0.0)

    def cleanup(self):
        """Cleanup the GPIO pins used by the motor.

        Calling this releases the motor, so further use of the motor will not
        be possible.
        """
        self.pwm.stop();
        GPIO.cleanup( [self.frwd_p, self.bkwd_p, self.enbl_p] )
