import numpy as np
import cv2


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
   