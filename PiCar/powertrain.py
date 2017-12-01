"""Powertrain class to manage two motors along a similar axle.
"""

# Imports
from motor import Motor

# Helper functions
def number_clamp(value, minimum, maximum):
    """ Function to clamp a given value between a minimum and maximum.

    Args:
        value: The value to clamp.
        minimum: The minimum of the return value.
        maximum: The maximum of the return value.

    Returns:
        Value clamped between the minimum and maximum.
    """
    return max(minimum, min(maximum, value))

def get_new_duty_cycle(duty_cycle, intensity):
    """Calculate duty cycle from the given intensity.

    The formula for this function has a greater intensity cause a greater
    difference between the given and returned duty cycle. Intensity 0 can
    return an equivalent duty cycle, and intensity 100 can return a 0 duty
    cycle.

    Args:
        duty_cycle (float): The duty cycle to get a portion of.
        intensity (float): The numerical portion to find. Clamps range between
            100 and 0.

    Returns:
        float: A new, potentially slower duty cycle.
    """
    # clamp the intensity
    cl_intensity = number_clamp(intensity, 0.0, 100.0)
    # calculate new duty cycle
    return duty_cycle * (100.0 - cl_intensity) / 100.0

class Powertrain:
    """Represents a pair of motors. Uses the Motor class to control them.
    """

    def __init__(self, left_wheel_forward, left_wheel_backward,
                 left_wheel_enable, right_wheel_forward, right_wheel_backward,
                 right_wheel_enable):
        """Constructor.

        Args:
            left_wheel_forward (int): GPIO pin connected to left motor's
                forward pin.
            left_wheel_backward (int): GPIO pin connected to left motor's
                backward pin.
            left_wheel_enable (int): GPIO pin connected to left motor's enable
                pin.
            right_wheel_forward (int): GPIO pin connected to right motor's
                forward pin.
            right_wheel_backward (int): GPIO pin connected to right motor's
                backward pin.
            right_wheel_enable (int): GPIO pin connected to right motor's
                enable pin.
        """
        # set motors
        self.left = Motor(left_wheel_forward, left_wheel_backward,
                          left_wheel_enable)
        self.right = Motor(right_wheel_forward, right_wheel_backward,
                           right_wheel_enable)

    def forward(self, duty_cycle):
        """Drive the powertrain forward.

        Args:
            duty_cycle (float): The duty cycle to run the motors at.
        """
        # apply to both motors
        self.left.forward(duty_cycle)
        self.right.forward(duty_cycle)

    def reverse(self, duty_cycle):
        """Drive the powertrain backward.

        Args:
            duty_cycle (float): The duty cycle to run the motors at.
        """
        # apply to both motors
        self.left.backward(duty_cycle)
        self.right.backward(duty_cycle)

    def turn(self, left_duty_cycle, right_duty_cycle, left_forward=True,
             right_forward=True):
        """Drive motor speeds separately to turn.

        Args:
            left_duty_cyle (float): The duty cyle to run the left motor at.
            right_duty_cycle (float): The duty cycle to run the right motor at.
            left_forward (boolean, optional): Flag for the left motor to go
                forward. Defaults to True.
            right_forward (boolean, optional): Flag for the right motor to go
                forward. Defaults to True.
        """
        #print("LDC: {0}, RDC: {1}".format(left_duty_cycle, right_duty_cycle))
        # if-else to use forward/backward
        if (left_forward):
            self.left.forward(left_duty_cycle)
        else:
            self.left.backward(left_duty_cycle)

        if (right_forward):
            self.right.forward(right_duty_cycle)
        else:
            self.right.backward(right_duty_cycle)

    def turn_left(self, max_duty_cycle, intensity=50.0, forward = True):
        """Drive the motors to turn left.

        Args:
            max_duty_cycle (float): The duty cycle to run the right motor at.
                The left motor runs at a portion of this.
            intensity (float, optional): The intensity to turn left. The value
                is clamped between 100 and 0. A greater intensity turns harder.
                Defaults to 50.0.
            forward (boolean, optional): Flag for spinning motors forward.
                Defaults to True.
        """
        # get min_duty_cycle
        min_duty_cycle = get_new_duty_cycle(max_duty_cycle, intensity)
        # pass to turn
        self.turn(min_duty_cycle, max_duty_cycle, forward, forward)

    def turn_right(self, max_duty_cycle, intensity=50.0, forward=True):
        """Drive the motors to turn right.

        Args:
            max_duty_cycle (float): The duty cycle to run the left motor at.
                The right motor runs at a portion of this.
            intensity (float, optional): The intensity to turn right. The value
                is clamped between 100 and 0. A greater intensity turns harder.
                Defaults to 50.0.
            forward (boolean, optional): Flag for spinning motors forward.
                Defaults to True.
        """
        # get min_duty_cycle
        min_duty_cycle = get_new_duty_cycle(max_duty_cycle, intensity)
        # pass to turn
        self.turn(max_duty_cycle, min_duty_cycle, forward, forward)

    def turn_intensity(self, max_duty_cycle, intensity, forward=True):
        """Drive the motors to turn based on intensity and its sign.

        Args:
            max_duty_cycle (float): The duty cycle to run the faster motor at.
                The other motor runs at a portion of this.
            intensity (float): The intensity to turn. The sign of the intensity
                affects the turn direction (e.g. negative for left, positive
                for right). The absolute value is clamped between 100 and 0. A
                greater intensity turns harder. If intensity is 0, this
                function drives motors equally.
            forward (boolean, optional): Flag for spinning motors forward.
                Defaults to True.
        """
        # need to multiply intensity by -1 if intensity is negative
        if (intensity < 0):
            self.turn_left(max_duty_cycle, intensity=(-1*intensity), forward=forward)
        else:
            self.turn_right(max_duty_cycle, intensity=intensity, forward=forward)

    def pivot(self, duty_cycle, clockwise=False):
        """Drive the motors to run opposite of each other to pivot.

        Args:
            duty_cycle (float): The duty cycle to run the motors at.
            clockwise (boolean, optional): Flag for pivoting clockwise.
                Defaults to False.
        """
        if (clockwise):
            self.turn(duty_cycle, duty_cycle, right_forward=False)
        else:
            self.turn(duty_cycle, duty_cycle, left_forward=False)

    def stop(self):
        """Stop the motors.
        """
        # TODO should this call brake() for a short time then call off()?
        self.left.off()
        self.right.off()

    def cleanup(self):
        """Cleanup GPIO pins for the motors.

        Calling this releases the motors, so further use of the powertrain will
        not be possible.
        """
        # apply to both motors
        self.left.cleanup()
        self.right.cleanup()
