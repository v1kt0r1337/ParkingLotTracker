#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import time

__author__ = "Adam Ajmi, Federico E. MejÃ­a Barajas"

class MyCar:
    #initiate array used for tracking positions inbetween frames
    tracks = []
    #Constructor
    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None

    #Returns color defined by randint in constructor
    def getRGB(self):
        return (self.R,self.G,self.B)
    #Returns last positions in frame
    def getTracks(self):
        return self.tracks
    #Returns ID
    def getId(self):
        return self.i
    #Returns state, where '0' is not being counted yet and '1' is already counted
    def getState(self):
        return self.state
    #Returns direction object has been tracked in, which can be either 'up' or 'down'
    def getDir(self):
        return self.dir
    #Returns current x coordinate
    def getX(self):
        return self.x
    #Returns current y coordinate
    def getY(self):
        return self.y
    #Updates the coordinates of object
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
    #Sets done to true, meaning object is no longer checked for direction travelled
    def setDone(self):
        self.done = True
    #Checks to see if object has been timed out (eg. set to done)
    def timedOut(self):
        return self.done
    
    #Counts object as going up if egligible
    def going_UP(self,mid_start,mid_end):
        #If there are more than two entries in tracks array (meaning we will have a potential vector)
        if len(self.tracks) >= 2:
            #If object is not 'done'
            if self.state == '0':
                #If two latest vectors created from tracks have crossed the line, meaning
                #if second last track originated before line, and last track originated equal to or afterwards
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end:
                    #Set new state and direction and return true
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False

    #Identical to going_UP with exception of self.dir being set to 'down'
    #and tracks being compared to mid_start instead of mid_end
    def going_DOWN(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start:
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False

    #Ages object by one frame and sets done if age has surpassed max_age
    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True

#class MultiCar:
#    def __init__(self, cars, xi, yi):
#        self.cars = cars
#        self.x = xi
#        self.y = yi
#        self.tracks = []
#        self.R = randint(0,255)
#        self.G = randint(0,255)
#        self.Y = randint(0,255)
#        self.done = False
