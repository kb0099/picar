import numpy as np;
import cv2;


## Read an Image

def readAnImage(filePath, colored):
    img = cv2.imread(filePath,0);
    cv2.imshow(filePath,img);
    k = cv2.waitKey(0) & 0xFF;
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows();
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite(filePath + "modified.png", img);
        cv2.destroyAllWindows();
   

## test lane steering algorithm on static images
def getSteeringDirection(imagePath):
    ''' 
        It returns the steering direction for the robot given the image. 
        Return value: (left, straight, right) = (-1, 0, 1)
    '''
    # read the image in grayscale
    #readAnImage(image, 0);
    image = cv2.imread(imagePath, 0);

    # reduce image size if necessary
    # perform basic thresholding
    ret, thImage = cv2.threshold(image,127,255,cv2.THRESH_BINARY);
    #cv2.imwrite("threshold_modified.jpg", thImage);
    print "roi: ";
    #print (thImage[300, :]);

    #erImage = cv2.erode(thImage, np.ones((20,20), np.uint8), iterations=1);
    #cv2.imwrite("threshold_eroded.jpg", erImage);


    # find the two lane lines
    whitePixels = cv2.findNonZero(thImage[300, :]);
    # find the middle of the lane
    #print whitePixels.shape

    """
        for row in whitePixels:
            for pair in row:
                print pair;
    """
    # the center pixel of the image indicates the current steering direction
    # return steering direction = lane middle [which expected position] - center pixel [current position] 
    # print image.shape (472 x 640)
    imageCenter         = 320;
    steeringThreshold   = 30;
    laneCenter          = (whitePixels[10][0][1] + whitePixels[whitePixels.shape[0]-10][0][1])/2;
    print "lane center: ", laneCenter;
    diff = laneCenter - imageCenter;
    if(diff < -steeringThreshold):
        print "Go Right"
    elif(diff > steeringThreshold):
        print "Go Left"
    else:
        print "Go straight"
 
if __name__ == '__main__':
    getSteeringDirection("threshold.jpg");
