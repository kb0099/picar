
# Imports
import RPi.GPIO as GPIO 

# Set GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class DirMotor:
    """DirMotor class represents direction [-1, 1]
    """
    def __init__(self, left, right, enable_pin):
        """Constructor.

        Args:
            forward_pin (int): GPIO pin connected to motor's forward pin.
            backward_pin (int): GPIO pin connected to motor's backward pin.
            enable_pin (int): GPIO pin connected to motor's enable pin
        """
        # store pins
        self.left_pin       = left
        self.right_pin      = right
        self.pwm_pin        = enable_pin
        self.turn_direction = 0.0; # [-1, 1] 

        GPIO.setup( [self.left_pin, self.right_pin, self.pwm_pin], GPIO.OUT, initial=False)

        # frequency (Hz) second parameter
        self.pwm = GPIO.PWM(self.pwm_pin, 100)

        self.pwm.start(0.0)

        # initial direction: 0.0
        # self.change_dir(True);

    def set_direction(self, direction = 0.0, duty_cycle=40.0):
        """ Set turn direction [-1, 1].
            duty_cycle is max limit
        """
        self.turn_direction = direction;
        if (direction < 0):
            self.left(duty_cycle);
        elif (direction > 0):
            self.right(duty_cycle);
        else:
            self.reset();


    def left(self, duty_cycle=40.0):
        """Drive the motor forward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 40.0.
        """
        GPIO.output(self.left_pin, True)
        GPIO.output(self.right_pin, False)
        if duty_cycle > 60:
            duty_cycle = 60;
        self.pwm.ChangeDutyCycle(duty_cycle);

    def right(self, duty_cycle=40.0):
        """Drive the motor backward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 40.0.
        """
        GPIO.output(self.left_pin, False)
        GPIO.output(self.right_pin, True)
        if duty_cycle > 60:
            duty_cycle = 60;
        self.pwm.ChangeDutyCycle(duty_cycle)

    def reset(self):
        """ Set direction to straight.
        """
        #GPIO.output(self.left_pin, False)
        #GPIO.output(self.right_pin, False)
        self.pwm.ChangeDutyCycle(0.0)

    def cleanup(self):
        """Cleanup the GPIO pins used by the motor.

        Calling this releases the motor, so further use of the motor will not
        be possible.
        """
        self.pwm.stop();
        GPIO.cleanup( [self.left_pin, self.right_pin, self.pwm_pin])



class SpeedMotor:
    """Represents a Speed.
    """

    def __init__(self, forward_pin, backward_pin, enable_pin):
        """Constructor.

        Args:
            forward_pin (int): GPIO pin connected to motor's forward pin.
            backward_pin (int): GPIO pin connected to motor's backward pin.
            enable_pin (int): GPIO pin connected to motor's enable pin
        """
        # store pins
        self.left_pin = forward_pin
        self.right_pin = backward_pin
        self.pwm_pin = enable_pin

        GPIO.setup( [self.left_pin, self.right_pin, self.pwm_pin], GPIO.OUT, initial=False)

        # frequency (Hz) second parameter
        self.pwm = GPIO.PWM(self.pwm_pin, 100)

        self.pwm.start(0.0)

        # initial direction forward
        self.change_dir(True);

    def forward(self, duty_cycle=40.0):
        """Drive the motor forward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 40.0.
        """
        GPIO.output(self.left_pin, True)
        GPIO.output(self.right_pin, False)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def backward(self, duty_cycle=40.0):
        """Drive the motor backward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 40.0.
        """
        GPIO.output(self.left_pin, False)
        GPIO.output(self.right_pin, True)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        """Stop motors gracefully
        """
        #GPIO.output(self.left_pin, True)
        #GPIO.output(self.right_pin, True)
        self.pwm.ChangeDutyCycle(0.0)

    def off(self):
        """Disable power to motor to coast.
        """
        #GPIO.output(self.left_pin, False)
        #GPIO.output(self.right_pin, False)
        self.pwm.ChangeDutyCycle(0.0)

    def cleanup(self):
        """Cleanup the GPIO pins used by the motor.

        Calling this releases the motor, so further use of the motor will not
        be possible.
        """
        self.pwm.stop();
        GPIO.cleanup( [self.left_pin, self.right_pin, self.pwm_pin])

    def change_dir(self, forward=True):
        GPIO.output(self.left_pin, forward)
        GPIO.output(self.right_pin, not forward) 

# ==================================================== temp

