"""
The bulk of this code was taken from the Color Spaces tutorial where the object tracking
was described. From this I also saw some examples of using contours after initially 
applying a black/white threshold as seen on lines 28-29. This essentially further contrasts
the mask and applies contours around anything that matches the specified color range. 
Lastly, I look for the largest contour by area and apply a bounding box around it to track
the largest object that is within our specified color range.
"""

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
width = cap.get(3)
height = cap.get(4)

while(1):
    # Take each frame
    _, frame = cap.read()


    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV

    lower_hsv = np.array([36, 50, 70])
    upper_hsv= np.array([89, 255, 255])
    # Threshold the HSV image 
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)

    _,thresh = cv.threshold(mask,127,255,0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    if len(contours):
        cont = max(contours, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(cont)
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    cv.imshow('frame',frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()