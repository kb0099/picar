import numpy as np;
import cv2

# sample test
stop_cascade = cv2.CascadeClassifier('haarcascade_ss.xml')

for im in ['s1.jpg', 's2.jpg']:
	img = cv2.imread(im)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ss = stop_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in ss:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),4)
		print "stop detected!" 
		cv2.imshow('img',img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	
print "if no image, means, didn't detect!"