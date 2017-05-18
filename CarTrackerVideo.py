import time
import cv2
import numpy as np


car_hc = cv2.CascadeClassifier('cars.xml')
vid = cv2.VideoCapture('video1.avi')
bgs = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
opMorph = np.ones((4,4),np.uint8)
clMorph = np.ones((4,4),np.uint8)
areaTH = 500

if vid.isOpened():
    rval , frame = vid.read()
else:
    rval = False
while rval:
    rval, frame = vid.read()

    fgmask = bgs.apply(frame)

    rval, imBin=cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, opMorph)
    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_CLOSE, clMorph)

    _, contours0, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cont in contours0:
        cv2.drawContours(frame, cont, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cont)
        print area
        if area > areaTH:
            M = cv2.moments(cont)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cont)
            cv2.circle(frame, (cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.drawContours(frame, cont, -1, (0,255,0), 3)

    cars = car_hc.detectMultiScale(frame, 1.1, 2)

    #ncars = 0
    #for (x,y,w,h) in cars:
    #    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    #    ncars = ncars + 1
    #    print ncars

    cv2.imshow("Backround Subtraction", fgmask)
    cv2.imshow("Result",frame)
    cv2.waitKey(1);
vid.release()

