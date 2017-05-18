from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


car_hc = cv2.CascadeClassifier('cars.xml')
camera = PiCamera()
camera.resolution = (300, 240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=camera.resolution)
bgs = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
opMorph = np.ones((4,4),np.uint8)
clMorph = np.ones((4,4),np.uint8)
areaTH = 500

time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    fgmask = bgs.apply(image)

    _,imBin=cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, opMorph)
    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_CLOSE, clMorph)
    
    _, contours0, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cont in contours0:
        cv2.drawContours(image, cont, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cont)
        print area
        if area > areaTH:
            M = cv2.moments(cont)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cont)
            cv2.circle(image, (cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.drawContours(image, cont, -1, (0,255,0), 3)
    
    #cars = car_hc.detectMultiScale(image, 1.1, 2)

    #ncars = 0
    #for (x,y,w,h) in cars:
    #    cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
    #    ncars = ncars + 1
    #    print ncars    
    
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break