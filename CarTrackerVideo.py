import cv2
import numpy as np

car_hc = cv2.CascadeClassifier('cars.xml')
vid = cv2.VideoCapture('video1.avi')
bgs = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
opMorph = np.ones((4,4),np.uint8)
clMorph = np.ones((4,4),np.uint8)

if vid.isOpened():
    rval , frame = vid.read()
else:
    rval = False
while rval:
    rval, frame = vid.read()
	
	fgmask = bgs.apply(frame)
	
	rval, imBin=cv2.threshold(fgmask, 200, 255, cv2.TRESH_BINARY)
	
	fgmask = cv.morphologyEx(imBin, cv2.MORPH_OPEN, opMorph)
	
	fgmask = cv2.morphologyEx(imBin, cv2.MORPH_CLOSE, clMorph)
	
    cars = car_hc.detectMultiScale(frame, 1.1, 2)

    ncars = 0
    for (x,y,w,h) in cars:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        ncars = ncars + 1
		print ncars

    cv2.imshow("Background Subtraction", fgmask)
	cv2.imshow("Result",frame)
    cv2.waitKey(1);
vid.release()
