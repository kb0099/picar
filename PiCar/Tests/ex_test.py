# manual_test.py

import sys;
import time;

sys.path.append('..');
from car_config import *;



# ==================================================== temp

"""DirMotor class represents direction [-1, 1]
"""

# Imports
import RPi.GPIO as GPIO 

# Set GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM);

class DirMotor:
    """Represents a single motor. Speed is set through PWM.
    """

    def __init__(self, left, right, enable_pin):
        """Constructor.

        Args:
            forward_pin (int): GPIO pin connected to motor's forward pin.
            backward_pin (int): GPIO pin connected to motor's backward pin.
            enable_pin (int): GPIO pin connected to motor's enable pin
        """
        # store pins
        self.frwd_p = left
        self.bkwd_p = right
        self.enbl_p = enable_pin
        self.turn_direction = 0.0; # [-1, 1]

        GPIO.setup( [self.frwd_p, self.bkwd_p, self.enbl_p], GPIO.OUT, initial=False)

        # frequency (Hz) second parameter
        self.pwm = GPIO.PWM(self.enbl_p, 100)

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
        GPIO.output(self.frwd_p, True)
        GPIO.output(self.bkwd_p, False)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def right(self, duty_cycle=40.0):
        """Drive the motor backward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 40.0.
        """
        GPIO.output(self.frwd_p, False)
        GPIO.output(self.bkwd_p, True)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def reset(self):
        """ Set direction to straight.
        """
        #GPIO.output(self.frwd_p, False)
        #GPIO.output(self.bkwd_p, False)
        self.pwm.ChangeDutyCycle(0.0)

    def cleanup(self):
        """Cleanup the GPIO pins used by the motor.

        Calling this releases the motor, so further use of the motor will not
        be possible.
        """
        self.pwm.stop();
        GPIO.cleanup( [self.frwd_p, self.bkwd_p, self.enbl_p])

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
        self.frwd_p = forward_pin
        self.bkwd_p = backward_pin
        self.enbl_p = enable_pin

        GPIO.setup( [self.frwd_p, self.bkwd_p, self.enbl_p], GPIO.OUT, initial=False)

        # frequency (Hz) second parameter
        self.pwm = GPIO.PWM(self.enbl_p, 100)

        self.pwm.start(0.0)

        # initial direction forward
        self.change_dir(True);

    def forward(self, duty_cycle=40.0):
        """Drive the motor forward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 40.0.
        """
        GPIO.output(self.frwd_p, True)
        GPIO.output(self.bkwd_p, False)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def backward(self, duty_cycle=40.0):
        """Drive the motor backward.

        Args:
            duty_cycle (float, optional): The duty cycle to run the motor at.
                Defaults to 40.0.
        """
        GPIO.output(self.frwd_p, False)
        GPIO.output(self.bkwd_p, True)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        """Lock the motor to act as brake.
        """
        #GPIO.output(self.frwd_p, True)
        #GPIO.output(self.bkwd_p, True)
        self.pwm.ChangeDutyCycle(0.0)

    def off(self):
        """Disable power to motor to coast.
        """
        #GPIO.output(self.frwd_p, False)
        #GPIO.output(self.bkwd_p, False)
        self.pwm.ChangeDutyCycle(0.0)

    def cleanup(self):
        """Cleanup the GPIO pins used by the motor.

        Calling this releases the motor, so further use of the motor will not
        be possible.
        """
        self.pwm.stop();
        GPIO.cleanup( [self.frwd_p, self.bkwd_p, self.enbl_p] )

    def change_dir(self, forward=True):
        GPIO.output(self.frwd_p, forward)
        GPIO.output(self.bkwd_p, not forward)


# ==================================================== temp



## Note  :
## Usage : python pt.py <test#> <args>

## Example
## To run test0 with argument 50
##      python pt.py 0 50
##
## To run test1 with duty cycle of 40:
##      python pt.py 1 40
##
## And similar for other tests!


# global
EX_DIRECTION_PWM        = 18;
EX_DIRECTION_LEFT       = 14;
EX_DIRECTION_RIGHT      = 15;


EX_SPEED_PWM            = 13;
EX_SPEED_FORWARD        = 26;
EX_SPEED_BACKWARD       = 19;


# direction motor
dm = DirMotor(EX_DIRECTION_LEFT, EX_DIRECTION_RIGHT, EX_DIRECTION_PWM);
sm = SpeedMotor(EX_SPEED_FORWARD, EX_SPEED_BACKWARD, EX_SPEED_PWM);


# test0 is for reset
def test0(dc):
    dm.reset();
    time.sleep(2);
    
# left
def test1(dc):
    dm.left(dc[0]);
    time.sleep(2);

# right
def test2(dc):
    dm.right(dc[0]);
    time.sleep(2);

# speed: forward
def test3(dc):
    sm.forward(dc[0]);
    time.sleep(2);


# speed: backward
def test4(arg):
    sm.backward(arg[0]);
    time.sleep(2);
    

# turn-right: turn_right(self, max_duty_cycle, intensity=50.0, forward=True):
def test5(arg):
    pt.turn_right(arg[0], arg[1]);
    time.sleep(2);

# tur-intensity: turn_intensity(self, max_duty_cycle, intensity, forward=True):
def test6(arg):
    pt.turn_intensity(arg[0], arg[1]);
    time.sleep(2);

# pivot pivot(self, duty_cycle, clockwise=False):
def test7(arg):
    pt.pivot(arg[0], arg[1]);
    time.sleep(2);

# stop
def test8(dc):
    pt.forward(dc[0]);
    time.sleep(2)
    pt.stop();
    time.sleep(2);
    pt.forward(dc[0])
    time.sleep(2);

    
# global tests
tests = [test0, test1, test2, test3, test4, test5, test6, test7, test8];
if __name__ == "__main__":
    tests[int(sys.argv[1])](map(float, sys.argv[2:]));
    print("all done!");
    dm.cleanup();
    
    
