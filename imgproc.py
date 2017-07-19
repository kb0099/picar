#!python2
import numpy
import cv2
import time
print cv2.__version__
print numpy.__version__
print numpy.__path__

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

while 1:
	#img = cv2.imread('capture.png', 1)
	img = get_image()

	rows,columns,channels = img.shape
	print('Rows: {0} Columns: {1} Channels: {2}'.format(rows, columns, channels))

	bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret,thresh = cv2.threshold(bw, 95, 255, cv2.THRESH_BINARY)
	ret,thresh2 = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY_INV)

	adapt = cv2.adaptiveThreshold(bw,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,81,12)

	print thresh.shape
	prog = 0
	start1 = 0
	start2 = 0
	end1 = 0
	end2 = 0
	for i in range(0, columns):
		if(thresh.item(250, i) is 0 and prog is 0):
			start1 = i
			prog = 1
		elif(thresh.item(250, i) is 255 and prog is 1):
			end1 = i
			prog = 2
		elif(thresh.item(250, i) is 0 and prog is 2):
			start2 = i
			prog = 3
		elif(thresh.item(250, i) is 255 and prog is 3):
			end2 = i
			prog = 4
	print('Start 1: {0}  End 1: {1}  Start 2: {2} End 2: {3}'.format(start1, end1, start2, end2))
	time.sleep(2)
	#cv2.imwrite('C:/Users/Tim/Desktop/img proc prac/nice.jpg', adapt)
	#cv2.imwrite('C:/Users/Tim/Desktop/img proc prac/nice2.jpg', thresh2)

	#edges = cv2.Canny(adapt,50,150,apertureSize = 3)
	#lines = cv2.HoughLinesP(edges,1,numpy.pi/180,100,minLineLength=100,maxLineGap=10)
	#for line in lines:
	#    x1,y1,x2,y2 = line[0]
	#    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
	#cv2.imwrite('nicelines.jpg',img)
