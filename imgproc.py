#!python2
import sys;
# fix for numpy/cv2
sys.path.append('/usr/lib/python2.7/lib-old');
sys.path.append('/usr/lib/python2.7/lib-dynload');
sys.path.append('/usr/local/lib/python2.7/dist-packages');
sys.path.append('/usr/lib/python2.7/dist-packages');
sys.path.append('/usr/lib/pymodules/python2.7');

import numpy
import cv2
import time
import datetime
#Libraries
import RPi.GPIO as GPIO

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_A1 = 2
GPIO_A2 = 3
GPIO_B1 = 14
GPIO_B2 = 15
GPIO_A3 = 4
GPIO_B3 = 18

GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_A1, GPIO.OUT)
GPIO.setup(GPIO_A2, GPIO.OUT)
GPIO.setup(GPIO_B1, GPIO.OUT)
GPIO.setup(GPIO_B2, GPIO.OUT)
GPIO.setup(GPIO_A3, GPIO.OUT)
GPIO.setup(GPIO_B3, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#Initial Pwm
p1 = GPIO.PWM(GPIO_A3, 1000)
p2 = GPIO.PWM(GPIO_B3, 1000)
p1.start(0);
p2.start(0);
# Default PWM Duty Cycle Value and Threshold
default_cycle = 80
cycle_limit_high = 100
cycle_limit_low = 60

# Distance at which to react to obstructions
safe_distance = 15

# Lines 10-24 from source: https://codeplasma.com/2012/12/03/getting-webcam-images-with-python-and-opencv-2-for-real-this-time/
# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)

# Captures a single image from the camera and returns it in PIL format
def get_image():
	'''
	Gets an image from the provided camera port for use in image processing.
	'''
 	# read is the easiest way to get a full image out of a VideoCapture object.
	retval, im = camera.read()
	return im

def forward(left, right):
	'''
	Gives the vehicle the instruction to move forward with the left and right arguments providing the desired duty cycle for each wheel.
	Providing differing values such as 70 and 100 will cause the vehicle to turn in the opposite direction of the higher valued argument.
	(0-100)
	'''
	if left > 100 or right > 100 or left < 0 or right < 0:
		Print('Invalid Forward Argument(s), must be between 0 and 100.')
		return
	# Set both wheels to forward motion.
	GPIO.output(GPIO_A1, True)
	GPIO.output(GPIO_A2, False)
	GPIO.output(GPIO_B1, True)
	GPIO.output(GPIO_B2, False)

	# Change Duty Cycle to desired values.
	p1.ChangeDutyCycle(left)
	p2.ChangeDutyCycle(right)
	return

def reverse(left, right):
	'''
	Gives the vehicle the instruction to move backwards with the left and right arguments providing the desired duty cycle for each wheel.
	Providing differing values such as 70 and 100 will cause the vehicle to turn in the opposite direction of the higher valued argument.
	(0-100)
	'''
	# Set both wheels to reverse motion
	GPIO.output(GPIO_A1, False)
	GPIO.output(GPIO_A2, True)
	GPIO.output(GPIO_B1, False)
	GPIO.output(GPIO_B2, True)

	# Change Duty cycle to desired value
	p1.ChangeDutyCycle(left)
	p2.ChangeDutyCycle(right)
	return

def right():
	'''
	Gives the vehicle the instruction to turn to the right.
	This function allows for a much faster turning speed than the forward function as the wheels are turning in opposite directions.
	Useful for quick turning adjustments.
	'''
	# Set left wheel to forward and right wheel to reverse.
	GPIO.output(GPIO_A1, True)
	GPIO.output(GPIO_A2, False)
	GPIO.output(GPIO_B1, False)
	GPIO.output(GPIO_B2, True)

	# Set the duty cycle for each wheel to the same default value.
	p1.ChangeDutyCycle(default_cycle)
	p2.ChangeDutyCycle(default_cycle)
	return

def left():
	'''
	Gives the vehicle the instruction to turn to the left.
	This function allows for a much faster turning speed than the forward function as the wheels are turning in opposite directions.
	Useful for quick turning adjustments.
	'''
	# Set left wheel to reverse and right wheel to forward.
	GPIO.output(GPIO_A1, False)
	GPIO.output(GPIO_A2, True)
	GPIO.output(GPIO_B1, True)
	GPIO.output(GPIO_B2, False)

	# Set the duty cycle for each wheel to the same default value.
	p1.ChangeDutyCycle(default_cycle)
	p2.ChangeDutyCycle(default_cycle)
	return

def stop():
	'''
	Gives the vehicle the instruction to stop all movement.
	'''
	# Set the duty cycle for each wheel to 0.
	p1.ChangeDutyCycle(0)
	p2.ChangeDutyCycle(0)
	return

def distance():
	'''
	Utilizes an ultrasonic sensor to determine the distance (in cm) to the nearest detected object.
	Returns the distance in centimeters.
	'''
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)
 
	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
 
	StartTime = time.time()
	StopTime = time.time()
 
	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
 
	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()
 
	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2
 
	return distance
def checkCycle(cycle):
	'''
	Ensures the provided duty cycle value falls within the acceptable range.
	'''
	if cycle > cycle_limit_high:
		adj_cycle = cycle_limit_high
	elif cycle < cycle_limit_low:
		adj_cycle = cycle_limit_low
	else:
		adj_cycle = cycle
	return adj_cycle

try:
	# Variables tracking wheel speed
	speed_left = default_cycle
	speed_right = default_cycle
	while 1:
		# Read image from camera or file
		#img = cv2.imread('cam2.jpg', 1)
		img = get_image()

		# Get the rows, columns, and channel values from the image
		rows,columns,channels = img.shape
		print('Rows: {0} Columns: {1} Channels: {2}'.format(rows, columns, channels))

		# Convert image to greyscale
		bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Value to determine whether to detect 'white on dark' or 'black on light' lanes (1 = white on dark)
		# TODO  ALLOW EASY SWITCHING WITHOUT CODE EDITING
		white_on_dark = 1

		# Process image using Binary Thresholding
		if white_on_dark:
			ret,thresh = cv2.threshold(bw, 235, 255, cv2.THRESH_BINARY)
		else:
			ret,thresh = cv2.threshold(bw, 100, 255, cv2.THRESH_BINARY_INV)

		# Line for adaptive thresholding if needed...
		#adapt = cv2.adaptiveThreshold(bw,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,221,1)

		#print thresh.shape
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
			# Uncomment the below line to draw a line on the row that is being detected:
			#thresh.itemset((low, i), 155)
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
			thresh.itemset((low, i), 155)
		prog = 0

		# Detect potential lane markings at the 'high' pixel row value
		for j in range(0, columns):
			# Uncomment the below line to draw a line on the row that is being detected:
			#thresh.itemset((high, j), 155)
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
		#print('Low: {0} to {1} and {2} to {3}'.format(start1_low, end1_low, start2_low, end2_low))
		#print('High: {0} to {1} and {2} to {3}'.format(start1_high, end1_high, start2_high, end2_high))

		# Print location of detected lanes
		print('Lanes detected in upper region at {0} and {1}'.format(high_1, high_2))
		print('Lanes detected in lower region at {0} and {1}'.format(low_1, low_2))

		sensor_distance = distance()
		print("DISTANCE: {0}".format(sensor_distance))

		# Determine how to control the car based on the image.
		# if obstruction is detected, stop
		if distance < safe_distance:
			print("stop!!")
			stop()

		# If only one lane is detected, determine which direction it is 'slanting' to tell the car which way to go
		if high_2 == 0 or low_2 == 0:
			if high_1 != 0 and low_1 != 0:
				print("Need Turning!")
				if high_1 > low_1:
					# Turn Right
					speed_right = 75
					speed_left = 90
				elif low_1 > high_1:
					# Turn Left
					print("LEFT")
					speed_right = 90
					speed_left = 75
			# Check that cycles are valid
			speed_left = checkCycle(speed_left)
			speed_right = checkCycle(speed_right)
			forward(speed_left, speed_right)
		# Case where lanes are detected on both lines.
		elif high_1 != 0 and high_2 != 0 and low_1 != 0 and low_2 != 0:
			# Default forward state
			print("looking good!")
			midpoint = (high_1 + high_2) / 2
			if midpoint >= (columns / 2) + 50:
				# Turn Right
				speed_right = 75
				speed_left = 85
			elif midpoint < (columns / 2) - 50:
				speed_right = 85
				speed_left = 75
			else:# high_1 > low_1 and high_2 < low_2:
				speed_left = default_cycle
				speed_right = default_cycle
			speed_left = checkCycle(speed_left)
			speed_right = checkCycle(speed_right)
			forward(speed_left, speed_right)




		# Wait 2 seconds
		time.sleep(.2)

		# Write thresholded image to file
		cv2.imwrite('../../data/imgs/' + datetime.datetime.now().isoformat() + "TEST.jpg", thresh)
except KeyboardInterrupt:
	stop()
	p1.stop()
	p2.stop()
	GPIO.cleanup()
	# Delete/Release Camera
	del(camera)
