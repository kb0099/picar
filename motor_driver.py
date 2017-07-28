"""Driver module to configure, setup, use, and cleanup GPIO for motor control.
"""

# Imports
import RPi.GPIO as GPIO

# Variables
# Pinout
#   Names like motor controller pins, values like BCM numbers.
A_InA = 2
"""int: Motor controller pin for motor A, intput A.

The value represents the BCM number on the RPi GPIO. Default is 2. 
"""
A_InB = 3
"""int: Motor controller pin for motor A, input B.

The value represents the BCM number on the RPi GPIO. Default is 3.
"""
B_InA = 14
"""int: Motor controller pin for motor B, input A.

The value represents the BCM number on the RPi GPIO. Default is 14.
"""
B_InB = 15
"""int: Motor controller pin for motor B, input B.

The value represents the BCM number on the RPi GPIO. Default is 15.
"""
# List to track pins after setup
#   useful for preserving values at setup, used in cleanup
__pin_list = []
# PWM
__A_AP = None
__A_BP = None
__B_AP = None
__B_BP = None
__frequency = 1000

def setup():
    """Initialize driver.

    Change motor controller pin variables if needed before setup.
    """

    # set mode to BCM numbers
    GPIO.setmode(GPIO.BCM)

    # set pin list
    global __pin_list = [A_InA, A_InB, B_InA, B_InB]

    # set pins to out
    GPIO.setup(__pin_list, GPIO.OUT)

    # assign PWM to pins w/ frequency
    global __A_AP = GPIO.PWM(A_InA, __frequency)
    global __A_BP = GPIO.PWM(A_InB, __frequency)
    global __B_AP = GPIO.PWM(B_InA, __frequency)
    global __B_BP = GPIO.PWM(B_InB, __frequency)

    # start PWM at 0.0 duty cycle
    __A_AP.start(0.0)
    __A_BP.start(0.0)
    __B_AP.start(0.0)
    __B_BP.start(0.0)

def forward_A(speed):
    """Drive motor A forward by setting A high and B low.

    Args:
        speed (float): Duty cycle for motor PWM.
    """

    __A_AP.ChangeDutyCycle(speed)
    __A_BP.ChangeDutyCycle(0.0)

def forward_B(speed):
    """Drive motor B forward by setting A high and B low.

    Args:
        speed (float): Duty cycle for motor PWM.
    """

    __B_AP.ChangeDutyCycle(speed)
    __B_BP.ChangeDutyCycle(0.0)

def backward_A(speed):
    """Drive motor A backward by setting A low and B high.

    Args:
        speed (float): Duty cycle for motor PWM.
    """

    __A_AP.ChangeDutyCycle(0.0)
    __A_BP.ChangeDutyCycle(speed)

def backward_B(speed):
    """Drive motor B backward by setting A low and B high.

    Args:
        speed (float): Duty cycle for motor PWM.
    """

    __B_AP.ChangeDutyCycle(0.0)
    __B_BP.ChangeDutyCycle(speed)

def off_A():
    """Turn off power to motor A."""

    __A_AP.ChangeDutyCycle(0.0)
    __A_BP.ChangeDutyCycle(0.0)

def off_B():
    """Turn off power to motor B."""

    __B_AP.ChangeDutyCycle(0.0)
    __B_BP.ChangeDutyCycle(0.0)

def cleanup():
    """Cleanup driver settings."""

    # stop PWM
    __A_AP.stop()
    __A_BP.stop()
    __B_AP.stop()
    __B_BP.stop()

    # call GPIO cleanup
    GPIO.cleanup(__pin_list)
