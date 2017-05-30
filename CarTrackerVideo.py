#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import cv2
import Car
import numpy as np
import requests
from requests.auth import HTTPDigestAuth
import json

__author__ = "Adam Ajmi, Kjetil Hoel, Federico E. MejÃ­a Barajas"

data = {'deviceId': 'api', 'password': 'passord'}

url = "http://158.37.63.8:3000/api/v0/auth"
r = requests.post(url, data=data)

jData = r.json()

# For successful API call, response code will be 200 (OK)
if(r.ok):
    token = jData.get('token')
    message = jData.get('message')
    print(message)

else:
  # If response code is not ok (200), print the resulting http error code with description
  message = jData.get('message')
print(message)

headers = {'x-access-token': token}
url = "http://158.37.63.8:3000/api/v0/parkinglogs/increment"

#car_hc = cv2.CascadeClassifier('cars.xml')
#Initiates capture of video file
vid = cv2.VideoCapture('video4.mp4')
#Creates background subtractor using MOG2 to remove most background noise before morphological transformations
bgs = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

#Values used for morphological transformations (open and close)
opMorph = np.ones((2,2),np.uint8)
opMorph2 = np.ones((3,3),np.uint8)
clMorph = np.ones((6,6),np.uint8)

#Counters for objects travelling up and down
cnt_up = 0
cnt_down = 0

#Prints out video properties
for i in range(19):
    print i, vid.get(i)

#Gets height and width of video
w = vid.get(3)
h = vid.get(4)
#Multiplies height and width to get area in pixels
frameArea = h*w
#Divide area with a pre-defined threshold value to get object recognition size
areaTH = frameArea/250
print 'Area threshold: ', areaTH

#Value used to draw lines based on video height
line_up = int(2*(h/5))
line_down = int(3*(h/5))
#Value used to define upper and lower limits of object detection
up_limit = int(1*(h/5))
down_limit = int(4*(h/5))

print "Red line y:",str(line_down)
#Colors the line red
line_down_color = (255,0,0)
#Creates two points, one on each side of the video with the same height
pt1 = [0, line_down];
pt2 = [w, line_down];
#Put point variables inside an array
pts_L1 = np.array([pt1,pt2], np.int32)
#Reshape array for compatability with function later on
pts_L1 = pts_L1.reshape((-1,1,2))

#The outlined process is repeated three more times, in total two for lines and two for limits
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

#font: font used for text display
#cars: Array used to store objects
#max_c_age: The amount of frames a car can remain alive while not being recognized/out of frame
#cid: Initial Car ID
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

    #Ensures that every active car object is aged every frame
    for i in cars:
        i.age_one()
        
    #Applies background subtraction to both foreground masks
    fgmask = bgs.apply(frame)
    fgmask2 = bgs.apply(frame)

    #Sets color threshold to binary to remove any gray colors
    rval, imBin=cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    rval, imBin2=cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)
        
    #Morphological transformations are applied
    #First we "open" the image, meaning we first erode and then dilate
    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, opMorph)
    fgmask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, opMorph)
    
    #Second, we "close" the image, meaning we first dilate then erode
    fgmask = cv2.morphologyEx(imBin, cv2.MORPH_CLOSE, clMorph)
    fgmask2 = cv2.morphologyEx(imBin2, cv2.MORPH_CLOSE, clMorph)
    
    #This removes all child contours from any earlier frames
    _, contours0, hierarchy = cv2.findContours(fgmask2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cont in contours0:
        #Draw a contour around any moving objects
        cv2.drawContours(frame, cont, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cont)
        #print area

        #If contour area is bigger than our pre-defined object size...
        if area > areaTH:
            #Loop is initiated, start tracking an object

            #Moments are, very simply put, used to approximate object position
            #We also use this to approximate the center of the object
            M = cv2.moments(cont)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cont)

            new = True
            #If object y-coordinates is within upper/lower tracking limit...
            if cy in range(up_limit,down_limit):
                for i in cars:
                    #if object is very close to one already detected last frame...
                    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                        #...then it is likely not a new object and new is set to False
                        new = False
                        i.updateCoords(cx,cy)
                        #If object is moving up...
                        if i.going_UP(line_down,line_up) == True:
                            #Increment counter and POST to database
                            cnt_up += 1;
                            print 'Object ID: ',i.getId(),' travelled up at',time.strftime('%c')
			    data = {"increment":1,"parkingLot_id":1}
			    r2 = requests.post(url, data, headers = headers)
                        #else if object is moving down...
                        elif i.going_DOWN(line_down,line_up) == True:
                            #Increment counter and POST to database
                            cnt_down += 1;
                            print 'Object ID: ',i.getId(),' travelled down at',time.strftime('%c')
			    data = {"increment":-1,"parkingLot_id":1}
			    r2 = requests.post(url, data, headers = headers)
                        break
                    #If state is '1', where '1' is already counted and '0' is default (not yet counted)
                    if i.getState () == '1':
                        #If direction is up/down and Y coordinate is past tracking limits, set done
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    #If car has not been detected in max_c_age amount of frames...
                    if i.timedOut():
                        #Pop car from index, then delete the entry
                        index = cars.index(i)
                        cars.pop(index)
                        del i
                if new == True:
                    #Create new object from class Car for tracking purposes
                    c = Car.MyCar(cid,cx,cy, max_c_age)
                    #Append new object to array
                    cars.append(c)
                    #Increment car ID counter
                    cid += 1
                
            #Draw green contours around the object with a red dot identifying the middle
            cv2.circle(frame, (cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.drawContours(frame, cont, -1, (0,255,0), 3)


            #This loop draws lines showing vectors of objects between frames
            for i in cars:
                if len(i.getTracks()) >= 2:
                    cts = np.array(i.getTracks(), np.int32)
                    cts = cts.reshape((-1,1,2))
                    frame = cv2.polylines(frame,[cts],False,i.getRGB())
                if i.getId() == 9:
                    print str(i.getX()), ',', str(i.getY())

                #Draw lines, object counters and text on the video frame
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

    #This loop uses haar cascading to put rectangles around recognized objects
    #cars = car_hc.detectMultiScale(frame, 1.1, 2)
    #ncars = 0
    #for (x,y,w,h) in cars:
    #    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    #    ncars = ncars + 1
    #    print ncars

    #Show frames with video playback
    cv2.imshow("Backround Subtraction", fgmask2)
    cv2.imshow("Result",frame)
    #Wait for key input
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
#Releases video and destroys all active windows
vid.release()
cv2.destroyAllWindows()

