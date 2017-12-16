#!python2
from ImageProcessor import ImageProcessor
from powertrain import Powertrain
from Ultrasonic import Ultrasonic
from car_config import *
import time
import RPi.GPIO as GPIO

imgpr = ImageProcessor(0, 0)
imgpr.init_camera()
pt = Powertrain(LFP, LBP, LEP, RFP, RBP, REP)
sensor = Ultrasonic()

def start():
    # Speed at which to turn each motor
    base_intensity = 0
    left_duty_cycle = 45
    right_duty_cycle = 45
    try:
        # Store the traveled direction between image processor calls
    	lastDir = 1
        while(True):
            # Get distance to nearest obstacle
            distance = sensor.distance()
            # If obstacle is too close, stop motors.
            if distance < 20:
                pt.stop()
                continue
            # Direction: -1 = left, 1 = right, 0 = no change
            # Call image processor to determine which wheel to turn
            direction = imgpr.check_status()

            if direction == -1:
                # Turn left
                pt.turn_intensity(right_duty_cycle, -100)
                lastDir = -1

            elif direction == 1:
                # Turn right
                pt.turn_intensity(left_duty_cycle, 100)
                lastDir = 1
            # Continue using previous direction
            elif direction == 0:
                if lastDir == -1:
                    # Turn Left
                    pt.turn_intensity(right_duty_cycle, -100)
                elif lastDir == 1:
                    # Turn Right
                    pt.turn_intensity(left_duty_cycle, 100)
            # Switch Directions
            elif direction == 2:
                if lastDir == -1:
                    # Turn Right
                    pt.turn_intensity(left_duty_cycle, 100)
                    lastDir = 1
                elif lastDir == 1:
                    # Turn Left
                    pt.turn_intensity(right_duty_cycle, -100)
                    lastDir = -1
                imgpr.recovery(sensor, pt)

            # Recovery - called when no lanes are detected.
            elif direction == 3:
                # Reverse Direction
                if lastDir == 1:
                    # Turn Right
                    pt.turn_intensity(left_duty_cycle, 100)
                elif lastDir == -1:
                    # Turn Left
                    pt.turn_intensity(right_duty_cycle, -100)
                # Call recovery function
                # Runs until 2 lanes are visible again.
                lastDir = imgpr.recovery(sensor, pt)

    except KeyboardInterrupt:
        stop()

def stop():
    # release all resources
    pt.stop()
    imgpr.cleanup()
    GPIO.cleanup()

start()
