import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

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

    #_,thresh = cv.threshold(mask,127,255,0)
    #contours, hierarchy = cv.findContours(thresh,1,2)
    #cnt = contours[0]


    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)


    #cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    #cv.imshow('res',res)


    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()