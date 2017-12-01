import numpy as np
#import os
import cv2
#from cv2 import *
#import sys
#import time
#import json
#import serial
import kociemba

from correlation import *
from motorController import *


########################################
## MISC VARIABLES
########################################

cubes = list()
cubes = [None]*54
position = {}

cameras = {'BRD':1, 'RUF':0, 'UBL':2}

## Minimum area that a contour must have in order to be recognised as valid
minimumContourArea = 20

## Size of target zone: half of length of size of the square
## This is used +- from the centre points of the porthole mask
altOffset = 20
offset = 11

## Colours are White, Blue, Red, Yellow, Green, Orange,
# TODO this cannot be assumed for the new iteration of robot
colours = {0:'U',1:'R',2:'F',3:'D',4:'L',5:'B'}


########################################
## HSV COLOURS
########################################
lower_yellow = np.array([26,70,100], dtype=np.uint8)
upper_yellow = np.array([36,255,255], dtype=np.uint8)

lower_blue = np.array([101,110,100], dtype=np.uint8)
upper_blue = np.array([150,255,255], dtype=np.uint8)

lower_orange = np.array([10,140,100], dtype=np.uint8)
upper_orange = np.array([24,255,255], dtype=np.uint8)

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
    #TODO This needs to be reworked
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
## 1) Figure out which position the contour centre is in, with respect to that camera
## 2) Figure out which position in the list this is based on which camera it is... (ie which face)
## 3) Insert the required colour marker into that position in the list

def correlateCubePosition(cameraNum, contourX, contourY):
    positionCount = 0
    for coordinates in correlation[1,]:
    # TODO This is a square, not a circle!
        if (fabs(coordinates[0] - contourX) < offset and
                fabs(coordinates[1] - contourY) < offset):
            return positionCount

        positionCount += 1


def listifyCubePosition(listPos, colour):
    # Insert cube colour into the cube state list with the appropriate
    # validation.

    # This should validate that:
    #   - listPos is a number, and within limits.
    #   - Contour is not attempted to be inserted twice? At the very least, it
    #       should not disagree with existing.

    # TODO For now this just returns silently but this should probably be fatal
    #   by returning an Input/CV exception
    error = False

    if ( (not listPos) or (listPos < 0) or (listPos > len(cubes)) ):
        print("Index in cubes list is not valid")
        error = True

    #if (cubes[listPos]):
    #    print("Cubelist is already populated in position")

    if (cubes[listPos] != colours[colour] ):
        print("Colour insertion disagrees with existing")
        error = True

    if (error == True):
        return

    cubes[listPos] = colours[colour]


########################################
## COLOUR EXTRACTION
########################################

def extractColours(image, cameraNum):
# TODO this needs reworked a lot
#YELLOW cube detection
    yellowHSVMask = getColourMask(image ,lower_yellow, upper_yellow)

    yellowContours, hierarchy_y = cv2.findContours(yellowHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # TODO Is this correct?
    cnts = sorted(yellowContours, key = cv2.contourArea, reverse = True)[:25]

    # TODO Is this correct?
    for c in cnts:
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        #TODO Why is the decision amde this way?
        if M["m00"] != 0 and area > minimumContourArea:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        listPosition = correlateCubePosition(cameraNum, cX, cY)
        listifyCubePosition(listPosition, 3)

#BLUE cube detection
    blueHSVMask = getColourMask(image ,lower_blue, upper_blue)

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

        listPosition = correlateCubePosition(cameraNum, cX, cY)
        listifyCubePosition(listPosition, 1)

#ORANGE cube detection
    orangeHSVMask = getColourMask(image, lower_orange, upper_orange)
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

        listPosition = correlateCubePosition(cameraNum, cX, cY)
        listifyCubePosition(listPosition, 5)

#GREEN cube detection
    greenHSVMask = getColourMask(image, lower_green, upper_green)
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

        listPosition = correlateCubePosition(cameraNum, cX, cY)
        listifyCubePosition(listPosition, 4)

#RED cube detection
    redHSVMask1 = getColourMask(image, lower_red1, upper_red1)
    redHSVMask2 = getColourMask(image, lower_red2, upper_red2)
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

        listPosition = correlateCubePosition(cameraNum, cX, cY)
        listifyCubePosition(listPosition, 2)

# TODO These 2 functions need to be reworked to use the correlations
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

    rawBRD = getImage(cameras['BRD'])
    rawRUF = getImage(cameras['RUF'])
    rawUBL = getImage(cameras['UBL'])

    imageBRD = cropRawImage(rawBRD, cameras['BRD'])
    imageRUF = cropRawImage(rawRUF, cameras['RUF'])
    imageUBL = cropRawImage(rawUBL, cameras['UBL'])

    heightimage, widthimage, channelsimage = imageBRD.shape
    portholeMask = createPortholeMask(heightimage, widthimage, channelsimage)

    ##maskedImage = np.bitwise_and(firstImage, cubiesMask)
    ## TODO Assumes images are all the same size (Only uses 1 mask)
    imageBRD = cv2.bitwise_and(imageBRD, imageBRD, mask = portholeMask)
    imageRUF = cv2.bitwise_and(imageRUF, imageRUF, mask = portholeMask)
    imageUBL = cv2.bitwise_and(imageUBL, imageUBL, mask = portholeMask)

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

    extractColours(imageBRD, cameras['BRD'])
    extractColours(imageRUF, cameras['RUF'])
    extractColours(imageUBL, cameras['UBL'])

    #cycles through list checking if value is equal to None and replaces with U
    # TODO Check that no more than 8 U (white) values are assumed:
    #   this should fail.
    cubes_k = [ x if x is not None else 'U' for x in cubes]
    cubes_str = ''.join(cubes_k)
    print(cubes_str)

    arduino = motorController()
    # TODO What is the purpose of this?
    # The string is not space delimited so it this just the last char that indicates the end of solution?
    solutionString = kociemba.solve(cubes_str) + ' '

    print(solutionString)
    arduino.sendString(passToArduino)

main()
