#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import cv2
import Car
import numpy as np

__author__ = "Adam Ajmi, Federico E. MejÃ­a Barajas"


#car_hc = cv2.CascadeClassifier('cars.xml')
vid = cv2.VideoCapture('video1.avi')
bgs = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
opMorph = np.ones((2,2),np.uint8)
opMorph2 = np.ones((3,3),np.uint8)
clMorph = np.ones((6,6),np.uint8)


cnt_up = 0
cnt_down = 0

for i in range(19):
    print i, vid.get(i)

w = vid.get(3)
h = vid.get(4)
frameArea = h*w
areaTH = frameArea/250
#areaTH = 500
print 'Area threshold: ', areaTH

line_up = int(2*(h/5))
line_down = int(3*(h/5))

up_limit = int(1*(h/5))
down_limit = int(4*(h/5))

print "Red line y:",str(line_down)
line_down_color = (255,0,0)
pt1 = [0, line_down];
pt2 = [w, line_down];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))

pt3 = [0, up_limit];
pt4 = [w, up_limit];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2

print "Blue line y:",str(line_up)
line_up_color = (0,0,255)
pt5 = [0, line_up];
pt6 = [w, line_down];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L2.reshape((-1,1,2))

pt7 = [0, down_limit];
pt8 = [w, down_limit];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L2.reshape((-1,1,2))




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

    for i in cars:
        i.age_one()
        
    fgmask = bgs.apply(frame)
    fgmask2 = bgs.apply(frame)

    
    rval, imBin=cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    rval, imBin2=cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)
        
    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, opMorph)
    fgmask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, opMorph)
        
    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_CLOSE, clMorph)
    fgmask2 = cv2.morphologyEx(imBin2, cv2.MORPH_CLOSE, clMorph)
    

    _, contours0, hierarchy = cv2.findContours(fgmask2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cont in contours0:
        cv2.drawContours(frame, cont, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cont)
        #print area
        if area > areaTH:
            M = cv2.moments(cont)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cont)

            new = True
            if cy in range(up_limit,down_limit):
                for i in cars:
                    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                        new = False
                        i.updateCoords(cx,cy)
                        if i.going_UP(line_down,line_up) == True:
                            cnt_up += 1;
                            print 'Object ID: ',i.getId(),' travelled up at',time.strftime('%c')
                        elif i.going_DOWN(line_down,line_up) == True:
                            cnt_down += 1;
                            print 'Object ID: ',i.getId(),' travelled down at',time.strftime('%c')
                        break
                    if i.getState () == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        index = cars.index(i)
                        cars.pop(index)
                        del i
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
                str_up = 'UP: '+ str(cnt_up)
                str_down = 'DOWN: '+ str(cnt_down)
                frame = cv2.polylines(frame, [pts_L1],False,line_down_color,thickness=4)
                frame = cv2.polylines(frame, [pts_L2],False,line_up_color,thickness=4)
                frame = cv2.polylines(frame, [pts_L3],False,(255,255,255),thickness=2)
                frame = cv2.polylines(frame, [pts_L4],False,(255,255,255),thickness=2)
                cv2.putText(frame,str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
                cv2.putText(frame,str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
                cv2.putText(frame,str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
                cv2.putText(frame,str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)

    #cars = car_hc.detectMultiScale(frame, 1.1, 2)

    #ncars = 0
    #for (x,y,w,h) in cars:
    #    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    #    ncars = ncars + 1
    #    print ncars

    cv2.imshow("Backround Subtraction", fgmask2)
    cv2.imshow("Result",frame)
    cv2.waitKey(1);
vid.release()
cv2.destroyAllWindows()

