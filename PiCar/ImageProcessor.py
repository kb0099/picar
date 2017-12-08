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
        # string for debugging image output
        self.init_time = datetime.datetime.now().isoformat()
        self.image_number = 0
        self.save_images = 0
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
            temp = self.camera.read()

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
            ret,thresh = cv2.threshold(bw, 220, 255, cv2.THRESH_BINARY)
        else:
            ret,thresh = cv2.threshold(bw, 140, 255, cv2.THRESH_BINARY_INV)
        # Rows to check in an image for lane markings
        low = 280 #200
        high = 220 #140

        # Tuples to store the midpoints of detected lane markings (left to right)
        low_row = ()
        high_row = ()
        # Tuples to store the size (in pixels) of detected lane markings
        low_row_sizes = ()
        high_row_sizes = ()
        # 0 = black/0; 1 = white/255
        color_low = 0
        color_high = 0
        # Minimum size in pixels for a detected white region to be considered a lane
        minimum_lane_size = 10

        for i in range(0, columns):
            # Check for lanes on lower image row
            if(thresh.item(low, i) is 255 and color_low is 0):
                # If a white pixel is detected, set color to 1 and store the start point for the potential lane
                color_low = 1
                detection_start_low = i
            elif(thresh.item(low, i) is 0 and color_low is 1):
                # Once end of white region is reached, store data into relevant tuples
                color_low = 0
                detection_end_low = i
                # Check that size of lane meets the minimum threshold
                if (detection_end_low - detection_start_low) >= minimum_lane_size:
                    # Calculate midpoint of detected lane
                    detection_midpoint_low = (detection_start_low + detection_end_low) / 2
                    # Add midpoint of detected lane to tuple
                    low_row += (detection_midpoint_low,)
                    # Add size of detected lane to tuple
                    low_row_sizes += ((detection_end_low - detection_start_low),)

            # Check for lanes on upper image row
            if(thresh.item(high, i) is 255 and color_high is 0):
                # If a white pixel is detected, set color to 1 and store the start point for the potential lane
                color_high = 1
                detection_start_high = i
            elif(thresh.item(high, i) is 0 and color_high is 1):
                # Once end of white region is reached, store data into relevant tuples
                color_high = 0
                detection_end_high = i
                # Check that size of lane meets the minimum threshold
                if (detection_end_high - detection_start_high) >= minimum_lane_size:
                    # Calculate midpoint of detected lane
                    detection_midpoint_high = (detection_start_high + detection_end_high) / 2
                    # Add midpoint of detected lane to tuple
                    high_row += (detection_midpoint_high,)
                    # Add size of detected lane to tuple
                    high_row_sizes += ((detection_end_high - detection_start_high),)
            # Draw lines representing scanned areas on image output
            thresh.itemset((low, i), 155)
            thresh.itemset((high, i), 155)

        # Variables to store the number of lanes detected on each row
        low_row_len = len(low_row)
        high_row_len = len(high_row)

        if self.save_images == 1:
            # # Debug image output
            save_string = '../../../images/' + datetime.datetime.now().isoformat() + '.jpg'
            raw_save_string = '../../../images/' + datetime.datetime.now().isoformat() + '-RAW' + '.jpg'

            cv2.imwrite(save_string, thresh)
            cv2.imwrite(raw_save_string, img)

            # print("Image saved to {0}".format(save_string))
            self.image_number += 1



        # Use the midpoints of detected lanes to tell the car if and how it needs to adjust

        # The distance from the expected midpoint to begin making slight adjustments
        midpoint_threshold = 5

        # Unexpected Case: >2 lanes in either row [occurs due to error in parsing image (noise etc)]
        # Action taken: Fix image processing issue/hope next image is better
        if low_row_len > 2 or high_row_len > 2:
            return 0
            #print("More than 2 lane points in one row, check output image {0} to view issue.".format(self.image_number))

        # Unexpected Case: 0 lanes detected [car is off course by a significant margin]
        # Action taken: Call a "recovery" function that attempts to relocate lanes
        if low_row_len == 0 and high_row_len == 0:
            #print("Off course! No lanes detected!")
            # TODO: Recovery function
            return 3

        # Expected Case: 2 lanes detected in each row
        # Action taken: Slight adjustments based on location of detected lines
        if low_row_len == 2 and high_row_len == 2:
            # Use midpoint of image to reference where lanes should be to make small adjustments
            image_midpoint = columns / 2
            # Midpoint of the two lower region lanes
            lower_midpoint = (low_row[0] + low_row[1]) / 2
            # Midpoint of upper region lanes
            upper_midpoint = (high_row[0] + high_row[1]) / 2
            # If midpoints are far enough away from the true middle, make a slight adjustment
            if abs(lower_midpoint - image_midpoint) > midpoint_threshold and abs(upper_midpoint - image_midpoint) > midpoint_threshold:
                # Determine direction based on sign of image_midpoint - lower_midpoint
                if (image_midpoint - lower_midpoint) > 0:
                    # Turn right
                    #print("Mild adjustment right...")
                    return -1
                else:
                    # Turn Left
                    #print("Mild adjustment left...")
                    return 1
            else:
                #print("Lane positioning is good!")
                return 0


        # Expected Case: 1 lane detected in each row (car is veering to one side)
        # Action taken: Reverse direction car is currently traveling
        if low_row_len == 1 and high_row_len == 1:
            # Use midpoint of image to determine which direction to turn.
            image_midpoint = columns / 2
            # Left hand lane detected [from inside lane area]
            if low_row[0] >= image_midpoint:
                #print("Single Lane turning right...")
                return 1
            # Right hand lane detected [from inside lane area]
            else:
                #print("Single Lane turning left...")
                return -1

	# Unexpected Case: Only 1 lane detected in upper or lower regions combined [most likely found in lower region].
        # This should occur when the vehicle is veering out of the lanes and requires a large change in duty cycle.
        if low_row_len + high_row_len == 1:
            # Use midpoint of image to determine which direction to turn.
            image_midpoint = columns / 2
            if low_row_len == 1:
                if low_row[0] >= image_midpoint:
                    # Turn Right
                    return 1
                else:
                    # Turn Left
                    return -1
            else:
                # I don't expect this to ever occur, will implement if observed.
                #print("SINGLE LANE IN UPPER REGION CHECK IMAGE AND IMPLEMENT BEHAVIOR!!!!!!!!!!!!!!!!!!!!\n$$$$$$$$$$$$\n$$$$$$$$$$$\n$$$$$$$$$$$")
                return 0

        # Unexpected Case: 1 lane detected in lower row and 2 detected in the upper row [off course and/or image parsing error]
        # Action taken: Determine which direction to turn using lane orientation and make more significant adjustments.
        if low_row_len == 1 and high_row_len == 2:
            # Determine which "side" the single lane is on/closer to
            # Single lane on left side
            if min(abs(high_row[0] - low_row[0]), abs(high_row[1] - low_row[0])) == abs(high_row[0] - low_row[0]):
                # Turn right
                #print("Lanes 2/1 turning right...")
                return 1
            # Single lane on right side
            else:
                # Turn left
                #print("Lanes 2/1 turning left...")
                return -1

        # Unexpected Case: 1 lane detected in upper row and 2 detected in the lower row [off course and/or image parsing error]
        # Action taken: Determine which direction to turn using lane orientation and make more significant adjustments.
        if low_row_len == 2 and high_row_len == 1:
            # Single lane on left side
            if min(abs(low_row[0] - high_row[0]), abs(low_row[1] - high_row[0])) == abs(low_row[0] - high_row[0]):
                # Turn right
                #print("Lanes 1/2 turning right...")
                return 1
            # Single lane on right side
            else:
                # Turn left
                #print("Lanes 2/1 turning left...")
                return -1

        return 0

    def recovery(self, sensor, pt):
        '''
        Called when no lanes are detected by the camera.
        Attempts to get the vehicle back on track using the direction traveled when lanes were lost.
        Accomplishes this by reversing the last direction the car traveled until 2 lanes are visible.
        '''
        # Return once two lanes are detected
        while(True):
            distance = sensor.distance()
            if distance < 20:
                pt.stop()
                continue
            status = self.check_status()
            if status == 1 or status == -1:
                return status

        
        pass;
    def cleanup(self):
        del(self.camera)

    
