import numpy as np
#import os
import cv2
#from cv2 import *
#import sys
#import time
#import json
import serial
import kociemba


########################################
## MISC VARIABLES
########################################

cubes = list()
cubes = [None]*54
position = {}

## Minimum area that a contour must have in order to be recognised as valid
minimumContourArea = 20

## Size of target zone: half of length of size of the square
## This is used +- from the centre points of the porthole mask
altOffset = 20
offset = 11

## Colours are White, Blue, Red, Yellow, Green, Orange,
colours = {0:'U',1:'R',2:'F',3:'D',4:'L',5:'B'}

########################################
## HSV COLOURS
########################################
##lower_yellow = np.array([23,60,100], dtype=np.uint8)
##lower_yellow = np.array([23,80,100], dtype=np.uint8)
lower_yellow = np.array([26,70,100], dtype=np.uint8)
upper_yellow = np.array([36,255,255], dtype=np.uint8)

#DBALL Slightly adjusted Blue values
#lower_blue = np.array([101,120,100], dtype=np.uint8)
lower_blue = np.array([101,110,100], dtype=np.uint8)
upper_blue = np.array([150,255,255], dtype=np.uint8)

##lower_orange = np.array([8,120,100], dtype=np.uint8)
lower_orange = np.array([10,140,100], dtype=np.uint8)
##upper_orange = np.array([22,255,255], dtype=np.uint8)
upper_orange = np.array([24,255,255], dtype=np.uint8)

#lower_green = np.array([37,120,100], dtype=np.uint8)
lower_green = np.array([37,80,100], dtype=np.uint8)
upper_green = np.array([100,255,255], dtype=np.uint8)

lower_red1 = np.array([0,80,100], dtype=np.uint8)
upper_red1 = np.array([7,255,255], dtype=np.uint8)
lower_red2 = np.array([160,80,100], dtype=np.uint8)
upper_red2 = np.array([179,255,255], dtype=np.uint8)


########################################
## FUNCTION DEFINITIONS
########################################

def cropRawImage(rawImage, cameraNumber):
    ## The various cameras have slightly different angles/perspectives on their side of the cube
    ## Hence, this function takes the camera number to decide which set of co-ordinates to use
    ## Still really hacky

    # Crop image to small area around cube
    # 1. Co-ordinates for the 24 cubes should be more consistent
    # 2. Make a smaller array as soon as possible: Will make later
    #   processing a teeny bit faster
    if cameraNumber == 0:
        croppedImage = rawImage[55:455, 120:505]
    elif cameraNumber == 1:
        croppedImage = rawImage[50:450, 135:520]
    else:
        croppedImage = rawImage[45:445, 135:520]

    return croppedImage
    

def getImage(cameraNumber):
    camera = cv2.VideoCapture(cameraNumber)

    for i in xrange(30):
        temp = camera.read()
    null, cameraCapture = camera.read()

    del(camera)
    
    return cameraCapture


def getColourMask(colouredImage, lowerThreshold, upperThreshold):
    hsvImage = cv2.cvtColor(colouredImage, cv2.COLOR_BGR2HSV) 
    thresholdContour = cv2.inRange(hsvImage, lowerThreshold, upperThreshold)
    null, thresholdImage = cv2.threshold(thresholdContour, 127,255,3)

    return thresholdImage

########################################
## CONTOUR -> LIST FUNCTIONS
########################################
## colour given as number 0-5 for white, blue, red, yellow, green, orange in that order

## TODO this should be tidied up into a dictionary or something
## dirty hacks incoming

## 1) Figure out which position the contour centre is in, with respect to that camera 
## 2) Figure out which position in the list this is based on which camera it is... (ie which face)
## 3) Insert the required colour marker into that position in the list

def insertContourBRDCamera(colour, cX, cY):

    if cX > (35 -offset) and cX < (35 +offset) and cY > (125-offset) and cY < (125+offset):
        cubes.pop(45)
        cubes.insert(45,colours[colour])
    elif cX > (40 -offset) and cX < (40 +offset) and cY > (195-offset) and cY < (195+offset):
        cubes.pop(48)
        cubes.insert(48,colours[colour])
    ##  Bottom left: Viewed through rod
    ##elif cX > (45 -offset) and cX < (45 +offset) and cY > (265-offset) and cY < (265+offset):
    ##    cubes.pop(51)
    ##    cubes.insert(51,colours[colour])
    elif cX > (95 -offset) and cX < (95 +offset) and cY > (160-offset) and cY < (160+offset):
        cubes.pop(46)
        cubes.insert(46,colours[colour])
    elif cX > (100-offset) and cX < (100+offset) and cY > (300-offset) and cY < (300+offset):
        cubes.pop(52)
        cubes.insert(52,colours[colour])
    elif cX > (155-offset) and cX < (155+offset) and cY > (200-offset) and cY < (200+offset):
        cubes.pop(47)
        cubes.insert(47,colours[colour])
    elif cX > (160-offset) and cX < (160+offset) and cY > (290-offset) and cY < (290+offset):
        cubes.pop(50)
        cubes.insert(50,colours[colour])
    elif cX > (165-offset) and cX < (165+offset) and cY > (350-offset) and cY < (350+offset):
        cubes.pop(53)
        cubes.insert(53,colours[colour])

    elif cX > (225-offset) and cX < (225+offset) and cY > (200-offset) and cY < (200+offset):
        cubes.pop(36)
        cubes.insert(36,colours[colour])
    elif cX > (225-offset) and cX < (225+offset) and cY > (290-offset) and cY < (290+offset):
        cubes.pop(39)
        cubes.insert(39,colours[colour])
    elif cX > (225-offset) and cX < (225+offset) and cY > (350-offset) and cY < (350+offset):
        cubes.pop(42)
        cubes.insert(42,colours[colour])
    elif cX > (295-offset) and cX < (295+offset) and cY > (170-offset) and cY < (170+offset):
        cubes.pop(37)
        cubes.insert(37,colours[colour])
    elif cX > (280-offset) and cX < (280+offset) and cY > (310-offset) and cY < (310+offset):
        cubes.pop(43)
        cubes.insert(43,colours[colour])
    elif cX > (355-offset) and cX < (355+offset) and cY > (125-offset) and cY < (125+offset):
        cubes.pop(38)
        cubes.insert(38,colours[colour])
    elif cX > (345-offset) and cX < (345+offset) and cY > (195-offset) and cY < (195+offset):
        cubes.pop(41)
        cubes.insert(41,colours[colour])
    ##  Bottom left: Viewed through rod
    ##elif cX > (345-offset) and cX < (345+offset) and cY > (265-offset) and cY < (265+offset):
    ##    cubes.pop(44)
    ##    cubes.insert(44,colours[colour])

    elif cX > (55 -offset) and cX < (55 +offset) and cY > (75 -offset) and cY < (75 +offset):
        cubes.pop(2)
        cubes.insert(2,colours[colour])
    elif cX > (120-offset) and cX < (120+offset) and cY > (100-offset) and cY < (100+offset):
        cubes.pop(1)
        cubes.insert(1,colours[colour])
    elif cX > (190-offset) and cX < (190+offset) and cY > (135-offset) and cY < (135+offset):
        cubes.pop(0)
        cubes.insert(0,colours[colour])
    elif cX > (125-offset) and cX < (125+offset) and cY > (40 -offset) and cY < (40 +offset):
        cubes.pop(5)
        cubes.insert(5,colours[colour])
    elif cX > (260-offset) and cX < (260+offset) and cY > (100-offset) and cY < (100+offset):
        cubes.pop(3)
        cubes.insert(3,colours[colour])
    elif cX > (195-altOffset) and cX < (195+altOffset) and cY > (15 -altOffset) and cY < (15 +altOffset):
        cubes.pop(8)
        cubes.insert(8,colours[colour])
    elif cX > (260-offset) and cX < (260+offset) and cY > (40 -offset) and cY < (40 +offset):
        cubes.pop(7)
        cubes.insert(7,colours[colour])
    elif cX > (330-offset) and cX < (330+offset) and cY > (70 -offset) and cY < (70 +offset):
        cubes.pop(6)
        cubes.insert(6,colours[colour])


def insertContourRUFCamera(colour, cX, cY):
## colour given as number 0-5 for white, blue, red, yellow, green, orange in that order


## TODO I think this is incorrect: Remove when other code is confirmed to work instead
    ##if cX > (35 -offset) and cX < (35 +offset) and cY > (125-offset) and cY < (125+offset):
    ##    cubes.pop(44)
    ##    cubes.insert(44,colours[colour])
    ##elif cX > (40 -offset) and cX < (40 +offset) and cY > (195-offset) and cY < (195+offset):
    ##    cubes.pop(41)
    ##    cubes.insert(41,colours[colour])
    ####elif cX > (45 -offset) and cX < (45 +offset) and cY > (265-offset) and cY < (265+offset):
    ####    cubes.pop(38)
    ####    cubes.insert(38,colours[colour])
    ##elif cX > (95 -offset) and cX < (95 +offset) and cY > (160-offset) and cY < (160+offset):
    ##    cubes.pop(43)
    ##    cubes.insert(43,colours[colour])
    ##elif cX > (100-offset) and cX < (100+offset) and cY > (300-offset) and cY < (300+offset):
    ##    cubes.pop(37)
    ##    cubes.insert(37,colours[colour])
    ##elif cX > (155-offset) and cX < (155+offset) and cY > (200-offset) and cY < (200+offset):
    ##    cubes.pop(42)
    ##    cubes.insert(42,colours[colour])
    ##elif cX > (160-offset) and cX < (160+offset) and cY > (290-offset) and cY < (290+offset):
    ##    cubes.pop(39)
    ##    cubes.insert(39,colours[colour])
    ##    cubes.insert(36,colours[colour])


    if cX > (35 -offset) and cX < (35 +offset) and cY > (125-offset) and cY < (125+offset):
        cubes.pop(38)
        cubes.insert(38,colours[colour])
    elif cX > (40 -offset) and cX < (40 +offset) and cY > (195-offset) and cY < (195+offset):
        cubes.pop(37)
        cubes.insert(37,colours[colour])
    ##  Bottom left: Viewed through rod
    ##elif cX > (45 -offset) and cX < (45 +offset) and cY > (265-offset) and cY < (265+offset):
    ##    cubes.pop(36)
    ##    cubes.insert(36,colours[colour])
    elif cX > (95 -offset) and cX < (95 +offset) and cY > (160-offset) and cY < (160+offset):
        cubes.pop(41)
        cubes.insert(41,colours[colour])
    elif cX > (100-offset) and cX < (100+offset) and cY > (300-offset) and cY < (300+offset):
        cubes.pop(39)
        cubes.insert(39,colours[colour])
    elif cX > (155-offset) and cX < (155+offset) and cY > (200-offset) and cY < (200+offset):
        cubes.pop(44)
        cubes.insert(44,colours[colour])
    elif cX > (160-offset) and cX < (160+offset) and cY > (290-offset) and cY < (290+offset):
        cubes.pop(43)
        cubes.insert(43,colours[colour])
    elif cX > (165-offset) and cX < (165+offset) and cY > (350-offset) and cY < (350+offset):
        cubes.pop(42)
        cubes.insert(42,colours[colour])

    elif cX > (225-offset) and cX < (225+offset) and cY > (200-offset) and cY < (200+offset):
        cubes.pop(27)
        cubes.insert(27,colours[colour])
    elif cX > (225-offset) and cX < (225+offset) and cY > (290-offset) and cY < (290+offset):
        cubes.pop(30)
        cubes.insert(30,colours[colour])
    elif cX > (225-offset) and cX < (225+offset) and cY > (350-offset) and cY < (350+offset):
        cubes.pop(33)
        cubes.insert(33,colours[colour])
    elif cX > (295-offset) and cX < (295+offset) and cY > (170-offset) and cY < (170+offset):
        cubes.pop(28)
        cubes.insert(28,colours[colour])
    elif cX > (280-offset) and cX < (280+offset) and cY > (310-offset) and cY < (310+offset):
        cubes.pop(34)
        cubes.insert(34,colours[colour])
    elif cX > (355-offset) and cX < (355+offset) and cY > (125-offset) and cY < (125+offset):
        cubes.pop(29)
        cubes.insert(29,colours[colour])
    elif cX > (345-offset) and cX < (345+offset) and cY > (195-offset) and cY < (195+offset):
        cubes.pop(32)
        cubes.insert(32,colours[colour])
    ##  Bottom left: Viewed through rod
    ##elif cX > (345-offset) and cX < (345+offset) and cY > (265-offset) and cY < (265+offset):
    ##    cubes.pop(35)
    ##    cubes.insert(35,colours[colour])

    elif cX > (55 -offset) and cX < (55 +offset) and cY > (75 -offset) and cY < (75 +offset):
        cubes.pop(18)
        cubes.insert(18,colours[colour])
    elif cX > (120-offset) and cX < (120+offset) and cY > (100-offset) and cY < (100+offset):
        cubes.pop(21)
        cubes.insert(21,colours[colour])
    elif cX > (190-offset) and cX < (190+offset) and cY > (135-offset) and cY < (135+offset):
        cubes.pop(24)
        cubes.insert(24,colours[colour])
    elif cX > (125-offset) and cX < (125+offset) and cY > (40 -offset) and cY < (40 +offset):
        cubes.pop(19)
        cubes.insert(19,colours[colour])
    elif cX > (260-offset) and cX < (260+offset) and cY > (100-offset) and cY < (100+offset):
        cubes.pop(25)
        cubes.insert(25,colours[colour])
    elif cX > (195-altOffset) and cX < (195+altOffset) and cY > (15 -altOffset) and cY < (15 +altOffset):
        cubes.pop(20)
        cubes.insert(20,colours[colour])
    elif cX > (260-offset) and cX < (260+offset) and cY > (40 -offset) and cY < (40 +offset):
        cubes.pop(23)
        cubes.insert(23,colours[colour])
    elif cX > (330-offset) and cX < (330+offset) and cY > (70 -offset) and cY < (70 +offset):
        cubes.pop(26)
        cubes.insert(26,colours[colour])

def insertContourUBLCamera(colour, cX, cY):
    if cX > (35 -offset) and cX < (35 +offset) and cY > (125-offset) and cY < (125+offset):
        cubes.pop(29)
        cubes.insert(29,colours[colour])
    elif cX > (40 -offset) and cX < (40 +offset) and cY > (195-offset) and cY < (195+offset):
        cubes.pop(28)
        cubes.insert(28,colours[colour])
    ##  Bottom left: Viewed through rod
    ##elif cX > (45 -offset) and cX < (45 +offset) and cY > (265-offset) and cY < (265+offset):
    ##    cubes.pop(27)
    ##    cubes.insert(27,colours[colour])
    elif cX > (95 -offset) and cX < (95 +offset) and cY > (160-offset) and cY < (160+offset):
        cubes.pop(32)
        cubes.insert(32,colours[colour])
    elif cX > (100-offset) and cX < (100+offset) and cY > (300-offset) and cY < (300+offset):
        cubes.pop(30)
        cubes.insert(30,colours[colour])
    elif cX > (155-offset) and cX < (155+offset) and cY > (200-offset) and cY < (200+offset):
        cubes.pop(35)
        cubes.insert(35,colours[colour])
    elif cX > (160-offset) and cX < (160+offset) and cY > (290-offset) and cY < (290+offset):
        cubes.pop(34)
        cubes.insert(34,colours[colour])
    elif cX > (165-offset) and cX < (165+offset) and cY > (350-offset) and cY < (350+offset):
        cubes.pop(33)
        cubes.insert(33,colours[colour])

    elif cX > (225-offset) and cX < (225+offset) and cY > (200-offset) and cY < (200+offset):
        cubes.pop(51)
        cubes.insert(51,colours[colour])
    elif cX > (225-offset) and cX < (225+offset) and cY > (290-offset) and cY < (290+offset):
        cubes.pop(52)
        cubes.insert(52,colours[colour])
    elif cX > (225-offset) and cX < (225+offset) and cY > (350-offset) and cY < (350+offset):
        cubes.pop(53)
        cubes.insert(53,colours[colour])
    elif cX > (295-offset) and cX < (295+offset) and cY > (170-offset) and cY < (170+offset):
        cubes.pop(48)
        cubes.insert(48,colours[colour])
    elif cX > (280-offset) and cX < (280+offset) and cY > (310-offset) and cY < (310+offset):
        cubes.pop(50)
        cubes.insert(50,colours[colour])
    elif cX > (355-offset) and cX < (355+offset) and cY > (125-offset) and cY < (125+offset):
        cubes.pop(45)
        cubes.insert(45,colours[colour])
    elif cX > (345-offset) and cX < (345+offset) and cY > (195-offset) and cY < (195+offset):
        cubes.pop(46)
        cubes.insert(46,colours[colour])
    ##  Bottom left: Viewed through rod
    ##elif cX > (345-offset) and cX < (345+offset) and cY > (265-offset) and cY < (265+offset):
    ##    cubes.pop(47)
    ##    cubes.insert(47,colours[colour])

    elif cX > (55 -offset) and cX < (55 +offset) and cY > (75 -offset) and cY < (75 +offset):
        cubes.pop(15)
        cubes.insert(15,colours[colour])
    elif cX > (120-offset) and cX < (120+offset) and cY > (100-offset) and cY < (100+offset):
        cubes.pop(16)
        cubes.insert(16,colours[colour])
    elif cX > (190-offset) and cX < (190+offset) and cY > (135-offset) and cY < (135+offset):
        cubes.pop(17)
        cubes.insert(17,colours[colour])
    elif cX > (125-offset) and cX < (125+offset) and cY > (40 -offset) and cY < (40 +offset):
        cubes.pop(12)
        cubes.insert(12,colours[colour])
    elif cX > (260-offset) and cX < (260+offset) and cY > (100-offset) and cY < (100+offset):
        cubes.pop(14)
        cubes.insert(14,colours[colour])
    elif cX > (195-altOffset) and cX < (195+altOffset) and cY > (15 -altOffset) and cY < (15 +altOffset):
        cubes.pop(9)
        cubes.insert(9,colours[colour])
    elif cX > (260-offset) and cX < (260+offset) and cY > (40 -offset) and cY < (40 +offset):
        cubes.pop(10)
        cubes.insert(10,colours[colour])
    elif cX > (330-offset) and cX < (330+offset) and cY > (70 -offset) and cY < (70 +offset):
        cubes.pop(11)
        cubes.insert(11,colours[colour])


########################################
## COLOUR EXTRACTION
########################################

def extract_color_BRD(BRDImage):
    #BRDImage = firstImage
#YELLOW cube detection
    yellowHSVMask = getColourMask(BRDImage ,lower_yellow, upper_yellow) 
    
    yellowContours, hierarchy_y = cv2.findContours(yellowHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(yellowContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourBRDCamera(3, cX, cY)

#BLUE cube detection
    blueHSVMask = getColourMask(BRDImage ,lower_blue, upper_blue) 

    blueContours, hierarchy_b = cv2.findContours(blueHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(blueContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourBRDCamera(1, cX, cY)

#ORANGE cube detection
    orangeHSVMask = getColourMask(BRDImage, lower_orange, upper_orange)
    orangeContours, hierarchy_o = cv2.findContours(orangeHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(orangeContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourBRDCamera(5, cX, cY)
    
#GREEN cube detection
    greenHSVMask = getColourMask(BRDImage, lower_green, upper_green)
    greenContours, hierarchy_g = cv2.findContours(greenHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(greenContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourBRDCamera(4, cX, cY)
            
#RED cube detection
    redHSVMask1 = getColourMask(BRDImage, lower_red1, upper_red1)
    redHSVMask2 = getColourMask(BRDImage, lower_red2, upper_red2)
    redHSVMask = cv2.bitwise_or(redHSVMask1, redHSVMask2)

    redContours , hierarchy_r = cv2.findContours(redHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(redContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourBRDCamera(2, cX, cY)
    
def extract_color_RUF(RUFImage):
    #RUFImage = secondImage
#YELLOW cube detection
    yellowHSVMask = getColourMask(RUFImage ,lower_yellow, upper_yellow) 
    
    yellowContours, hierarchy_y = cv2.findContours(yellowHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(yellowContours, key = cv2.contourArea, reverse = True)[:25]
    
    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
    
        insertContourRUFCamera(3, cX, cY)
    
#BLUE cube detection
    blueHSVMask = getColourMask(RUFImage ,lower_blue, upper_blue) 

    blueContours, hierarchy_b = cv2.findContours(blueHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(blueContours, key = cv2.contourArea, reverse = True)[:25]
    
    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
    
        insertContourRUFCamera(1, cX, cY)
    
#ORANGE cube detection
    orangeHSVMask = getColourMask(RUFImage, lower_orange, upper_orange)

    orangeContours, hierarchy_o = cv2.findContours(orangeHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(orangeContours, key = cv2.contourArea, reverse = True)[:25]
    
    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
    
        insertContourRUFCamera(5, cX, cY)
    
#GREEN cube detection
    greenHSVMask = getColourMask(RUFImage, lower_green, upper_green)

    greenContours, hierarchy_g = cv2.findContours(greenHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(greenContours, key = cv2.contourArea, reverse = True)[:25]
    
    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
    
        insertContourRUFCamera(4, cX, cY)
            
#RED cube detection
    redHSVMask1 = getColourMask(RUFImage, lower_red1, upper_red1)
    redHSVMask2 = getColourMask(RUFImage, lower_red2, upper_red2)
    redHSVMask = cv2.bitwise_or(redHSVMask1, redHSVMask2)
    
    redContours , hierarchy_r = cv2.findContours(redHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(redContours, key = cv2.contourArea, reverse = True)[:25]
    
    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
    
        insertContourRUFCamera(2, cX, cY)

def extract_color_UBL(UBLImage):
    #UBLImage = thirdImage

#YELLOW cube detection
    yellowHSVMask = getColourMask(UBLImage ,lower_yellow, upper_yellow) 
    
    yellowContours, hierarchy_y = cv2.findContours(yellowHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(yellowContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourUBLCamera(3, cX, cY)

#BLUE cube detection
 
    blueHSVMask = getColourMask(UBLImage ,lower_blue, upper_blue) 

    blueContours, hierarchy_b = cv2.findContours(blueHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(blueContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourUBLCamera(1, cX, cY)

#ORANGE cube detection
    orangeHSVMask = getColourMask(UBLImage, lower_orange, upper_orange)

    orangeContours, hierarchy_o = cv2.findContours(orangeHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(orangeContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourUBLCamera(5, cX, cY)
    
#GREEN cube detection

    greenHSVMask = getColourMask(UBLImage, lower_green, upper_green)

    greenContours, hierarchy_g = cv2.findContours(greenHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(greenContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourUBLCamera(4, cX, cY)

#RED cube detection
    redHSVMask1 = getColourMask(UBLImage, lower_red1, upper_red1)
    redHSVMask2 = getColourMask(UBLImage, lower_red2, upper_red2)
    redHSVMask = cv2.bitwise_or(redHSVMask1, redHSVMask2)
    
    redContours , hierarchy_r = cv2.findContours(redHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(redContours, key = cv2.contourArea, reverse = True)[:25]

    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        insertContourUBLCamera(2, cX, cY)

def drawTargetZonesOnImage(image):
    ## Left face
    cv2.rectangle(image,(35 -offset , 125-offset), (35 +offset, 125+offset), (0,255,0),2)
    cv2.rectangle(image,(40 -offset , 195-offset), (40 +offset, 195+offset), (0,255,0),2)
    cv2.rectangle(image,(45 -offset , 265-offset), (45 +offset, 265+offset), (0,255,0),2)
    cv2.rectangle(image,(95 -offset , 160-offset), (95 +offset, 160+offset), (0,255,0),2)
    cv2.rectangle(image,(100-offset , 300-offset), (100+offset, 300+offset), (0,255,0),2)
    cv2.rectangle(image,(155-offset , 200-offset), (155+offset, 200+offset), (0,255,0),2)
    cv2.rectangle(image,(160-offset , 290-offset), (160+offset, 290+offset), (0,255,0),2)
    cv2.rectangle(image,(165-offset , 350-offset), (165+offset, 350+offset), (0,255,0),2)

    ## Right face
    cv2.rectangle(image,(225-offset , 200-offset), (225+offset, 200+offset), (0,255,0),2)
    cv2.rectangle(image,(225-offset , 290-offset), (225+offset, 290+offset), (0,255,0),2)
    cv2.rectangle(image,(225-offset , 350-offset), (225+offset, 350+offset), (0,255,0),2)
    cv2.rectangle(image,(295-offset , 170-offset), (295+offset, 170+offset), (0,255,0),2)
    cv2.rectangle(image,(280-offset , 310-offset), (280+offset, 310+offset), (0,255,0),2)
    cv2.rectangle(image,(355-offset , 125-offset), (355+offset, 125+offset), (0,255,0),2)
    cv2.rectangle(image,(345-offset , 195-offset), (345+offset, 195+offset), (0,255,0),2)
    cv2.rectangle(image,(345-offset , 265-offset), (345+offset, 265+offset), (0,255,0),2)

    ## Top face
    cv2.rectangle(image,(55 -offset , 75 -offset), (55 +offset, 75 +offset), (0,255,0),2)
    cv2.rectangle(image,(120-offset , 100-offset), (120+offset, 100+offset), (0,255,0),2)
    cv2.rectangle(image,(190-offset , 135-offset), (190+offset, 135+offset), (0,255,0),2)
    cv2.rectangle(image,(125-offset , 40 -offset), (125+offset, 40 +offset), (0,255,0),2)
    cv2.rectangle(image,(260-offset , 100-offset), (260+offset, 100+offset), (0,255,0),2)
    cv2.rectangle(image,(195-altOffset , 15 -altOffset), (195+altOffset, 15 +altOffset), (0,255,0),2)
    cv2.rectangle(image,(260-offset , 40 -offset), (260+offset, 40 +offset), (0,255,0),2)
    cv2.rectangle(image,(330-offset , 70 -offset), (330+offset, 70 +offset), (0,255,0),2)

########################################

def createPortholeMask(height, width, channels):
    ## TODO This should be the same time for all of the images BUT might not be
    ## Cropped images should be 385x400
    cubiesMaskInitial = np.zeros((height, width, channels), np.uint8)

    ## Draw circle "view ports" on mask
    cv2.circle(cubiesMaskInitial, (35 , 125), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (40 , 195), offset, (255,255,255), -1)
    ## BOTTOM LEFT: Through rod
    ##cv2.circle(cubiesMaskInitial, (45 , 265), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (95 , 160), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (100, 300), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (155, 200), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (160, 290), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (165, 350), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (225, 200), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (225, 290), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (225, 350), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (295, 170), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (280, 310), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (355, 125), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (345, 195), offset, (255,255,255), -1)
    ## BOTTOM RIGHT: Through rod
    ##cv2.circle(cubiesMaskInitial, (345, 265), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (55 , 75 ), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (120, 100), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (190, 135), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (125, 40 ), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (260, 100), offset, (255,255,255), -1)
    ## This is the top far cubie, looking through the rod.
    cv2.circle(cubiesMaskInitial, (195, 15 ), altOffset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (260, 40 ), offset, (255,255,255), -1)
    cv2.circle(cubiesMaskInitial, (330, 70 ), offset, (255,255,255), -1)

    ## Create proper mask
    cubiesMaskFinal = cv2.inRange(cubiesMaskInitial, (1,1,1), (255,255,255))
    
    return cubiesMaskFinal

def main():
    print("STARTING")

    firstRaw = getImage(1)
    secondRaw = getImage(0)
    thirdRaw = getImage(2)

    firstImage = cropRawImage(firstRaw,1)
    secondImage = cropRawImage(secondRaw,0)
    thirdImage = cropRawImage(thirdRaw,2)

    heightimage1, widthimage1, channelsimage1 = firstImage.shape
    portholeMask = createPortholeMask(heightimage1, widthimage1, channelsimage1)  

    ##maskedImage = np.bitwise_and(firstImage, cubiesMask)
    ## TODO Assumes images are all the same size (Only uses 1 mask)
    firstImage = cv2.bitwise_and(firstImage, firstImage, mask = portholeMask)
    secondImage = cv2.bitwise_and(secondImage, secondImage, mask = portholeMask)
    thirdImage = cv2.bitwise_and(thirdImage, thirdImage, mask = portholeMask)

    cubes.pop(4)
    cubes.insert(4, "U")
    cubes.pop(13)
    cubes.insert(13, "R")
    cubes.pop(22)
    cubes.insert(22, "F")
    cubes.pop(31)
    cubes.insert(31, "D")
    cubes.pop(40)
    cubes.insert(40, "L")
    cubes.pop(49)
    cubes.insert(49, "B")
                      
    extract_color_BRD.__call__(firstImage)
    extract_color_RUF.__call__(secondImage)
    extract_color_UBL.__call__(thirdImage)

    #print(cubes)
    #cycles through list checking if value is equal to None and replaces with U
    # TODO Check that no more than 8 U (white) values are assumed:
    #   this should fail.
    cubes_k = [ x if x is not None else 'U' for x in cubes]        
    #print(cubes_k)
    cubes_str = ''.join(cubes_k)
    print(cubes_str)

    arduino = serial.Serial('/dev/ttyACM0', 9600)

    passToArduino = kociemba.solve(cubes_str) + ' '

    print(passToArduino)
############################################
## TODO HACK D face turns the wrong direction for some reason.
    passToArduino = passToArduino.replace("D ", "temp ")
    passToArduino = passToArduino.replace("D' ", "D ")
    passToArduino = passToArduino.replace("temp ", "D' ")

############################################
    print(passToArduino)
    arduino.write(passToArduino)

main()
