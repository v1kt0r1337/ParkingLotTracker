import time
import cv2
import numpy as np


#car_hc = cv2.CascadeClassifier('cars.xml')
vid = cv2.VideoCapture('video1.avi')
bgs = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
opMorph = np.ones((4,4),np.uint8)
clMorph = np.ones((4,4),np.uint8)


#cnt_up = 0
#cnt_down = 0

areaTH = 500
font = cv2.FONT_HERSHEY_SIMPLEX
cars = []
max_c_age = 5
cid = 1

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

            new = True
            for i in cars:
                if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                    new = False
                    i.updateCoords(cx,cy)
                    break
            if new == True:
                c = Car.MyCar(cid,cx,cy, max_c_age)
                cars.append(c)
                cid += 1

            cv2.circle(frame, (cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.drawContours(frame, cont, -1, (0,255,0), 3)

            for i in cars:
                if len(i.getTracks()) >= 2:
                    cts = np.array(i.getTracks(), np.int32)
                    cts = cts.reshape((-1,1,2))
                    frame = cv2.polylines(frame,[cts],False,i.getRGB())
                if i.getId() == 9:
                    print str(i.getX()), ',', str(i.getY())
                cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
            
    #cars = car_hc.detectMultiScale(frame, 1.1, 2)

    #ncars = 0
    #for (x,y,w,h) in cars:
    #    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    #    ncars = ncars + 1
    #    print ncars

    cv2.imshow("Backround Subtraction", fgmask)
    cv2.imshow("Result",frame)
    cv2.waitKey(1);
vid.release()

