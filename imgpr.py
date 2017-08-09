#!python2
import numpy
import cv2
import time
import datetime

print cv2.__version__
print numpy.__version__
print numpy.__path__

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
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = camera.read()
 return im

try:
	while 1:
		# Read image from camera or file
		#img = cv2.imread('cam2.jpg', 1)
		img = get_image()

		# Get the rows, cloumns, and channel values from the image
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

		print thresh.shape
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
		low = 250
		high = 160

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

		# Wait 2 seconds
		time.sleep(2)

		# Write thresholded image to file
		cv2.imwrite('../../data/imgs/' + datetime.datetime.now().isoformat() + ".jpg", thresh)
		cv2.imwrite('../../data/imgs/' + datetime.datetime.now().isoformat() + "raw.jpg", img)
except KeyboardInterrupt:
	# Delete/Release Camera
	del(camera)
