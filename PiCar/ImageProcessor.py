#!python2
import sys
import numpy
import cv2
import time
import datetime
#Libraries
import RPi.GPIO as GPIO

class ImageProcessor:
    '''
    A module to be used for fetching images and performing various image processing functions
    to provide instructions to the vehicle.
    Attributes:
        camera_port: An int representing the port of the desire camera.
        lane_type: An int that tells the class to look for light lines on dark background (1) or dark lines on light background (0)
    '''
    def __init__(self, camera_port, lane_type):
        '''
        Return a ImageProcessor capturing from the provided camera port.
        camera_port: port of desired camera (int)
        lane_type: value 1 for light on dark, value 0 for dark on light lanes
        '''
        self.lane_type = lane_type
        self.camera = cv2.VideoCapture(camera_port)
        pass;

    def get_image(self):
        '''
        Fetches an image from the camera.
        '''
        retval, im = self.camera.read()
        return im

    def init_camera(self):
        '''
        Skips a number of frames to allow the webcam to adjust light levels etc.
        '''
        for i in xrange(30):
            temp = self.get_image()

    def set_lane_type(self, lane_t):
        '''
        Sets the line type to light on dark [1] or dark on light [0]
        '''
        if lane_t > 1 or lane_t < 0:
            raise ValueError("Lane type must be of value 0 or 1.")
            return
        else:
            self.lane_type = lane_t
    def check_status(self):
        '''
        Analyzes an image and provides instructions/parameters to support the vehicle's path.
        Returns a value between -1 and 1 that represents the turning action to be taken.
        A positive value represents a right turn while a negative value represents a left turn.
        The magnitude of the value determines the amount of turning desired (1/-1 being max).
        '''
        img = self.get_image()
        # Get the rows, columns, and channel values from the image
        rows,columns,channels = img.shape
        # Convert image to greyscale
        bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Process image using Binary Thresholding
        if self.lane_type:
            ret,thresh = cv2.threshold(bw, 245, 255, cv2.THRESH_BINARY)
        else:
            ret,thresh = cv2.threshold(bw, 100, 255, cv2.THRESH_BINARY_INV)
        # Initial values
        prog = 0
        start1_low = 0
        start2_low = 0
        end1_low = 0
        end2_low = 0
        start1_high = 0
        start2_high = 0
        end1_high = 0
        end2_high = 0
        low = 200
        high = 140

        # Detect potential lane markings at the 'low' pixel row value
        for i in range(0, columns):
            if(thresh.item(low, i) is 255 and prog is 0):
                start1_low = i
                prog = 1
            elif(thresh.item(low, i) is 0 and prog is 1):
                end1_low = i
                prog = 2
            elif(thresh.item(low, i) is 255 and prog is 2):
                start2_low = i
                prog = 3
            elif(thresh.item(low, i) is 0 and prog is 3):
                end2_low = i
                prog = 4
            # Uncomment the below line to draw a line on the row that is being detected:
            thresh.itemset((low, i), 155)
        prog = 0

        # Detect potential lane markings at the 'high' pixel row value
        for j in range(0, columns):
            if(thresh.item(high, j) is 255 and prog is 0):
                start1_high = j
                prog = 1
            elif(thresh.item(high, j) is 0 and prog is 1):
                end1_high = j
                prog = 2
            elif(thresh.item(high, j) is 255 and prog is 2):
                start2_high = j
                prog = 3
            elif(thresh.item(high, j) is 0 and prog is 3):
                end2_high = j
                prog = 4
            # Uncomment the below line to draw a line on the row that is being detected:
            thresh.itemset((high, j), 155)

        # Condense the two-point lane detection to a single point at the midpoint of the lane
        if start1_low != 0 and end1_low != 0:
            low_1 = (start1_low + end1_low) / 2
        else:
            low_1 = 0
        if start2_low != 0 and end2_low != 0:
            low_2 = (start2_low + end2_low) / 2
        else:
            low_2 = 0
        if start1_high != 0 and end1_high != 0:
            high_1 = (start1_high + end1_high) / 2
        else:
            high_1 = 0
        if start2_high != 0 and end2_high != 0:
            high_2 = (start2_high + end2_high) / 2
        else:
            high_2 = 0

        print("Low l/2: {0} / {1}\nHigh 1/2: {2} / {3}\n".format(low_1, low_2, high_1, high_2))
        cv2.imwrite('../../../images/' + datetime.datetime.now().isoformat() + ".jpg", thresh)
        cv2.imwrite('../../../images/' + datetime.datetime.now().isoformat() + "_RAW.jpg", img)

        # If only one lane is detected, determine which direction it is 'slanting' to tell the car which way to go
        if high_2 == 0 or low_2 == 0:
            if high_1 != 0 and low_1 != 0:
                if high_1 > low_1:
                    # TODO: Turn Right
                    return .25
                elif low_1 > high_1:
                    # TODO: Turn Left
                    return -.25
        # Case where lanes are detected on both lines. [Using midpoint for preemptive adjustments]
        elif high_1 != 0 and high_2 != 0 and low_1 != 0 and low_2 != 0:
            # Default forward state
            midpoint = (high_1 + high_2) / 2
            if midpoint >= (columns / 2) + 50:
                # TODO: Turn Right
                return .10
            elif midpoint < (columns / 2) - 50:
                # TODO: Turn Left
                return -.10
            else:
                # TODO: Continue Straight
                return 0
        # No lines detected/issues
        else:
            # TODO: Error/Misalignment recovery
            print("RECOVERY METHOD CALLED")
        return

    def process_images(img):
        # threshold
        # detect lines
        # detect obstacles
        # detect stop signs
        
        pass;
    def cleanup(self):
        del(self.camera)

    
