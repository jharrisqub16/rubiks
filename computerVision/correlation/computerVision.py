import cv2
import math
import numpy as np

from correlation import *


class computerVision():
    def __init__(self):
        self.cameras = {'BRD':1, 'RUF':0, 'UBL':2}

        self.colours = {0:'U',1:'R',2:'F',3:'D',4:'L',5:'B'}

        self.correlation = correlation

        # Some CV reference values
        self.minimumContourArea = 20
        self.offset = 11
        self.altOffset = 20

        # HSV colour reference values
        # TODO this must be modified: HSV values will be derived from
        # calibration, plus more complex algorithm (max liklihood) used to
        # determine best matches.
        self.lower_yellow = np.array([26,70,100], dtype=np.uint8)
        self.upper_yellow = np.array([36,255,255], dtype=np.uint8)
        self.lower_blue = np.array([101,110,100], dtype=np.uint8)
        self.upper_blue = np.array([150,255,255], dtype=np.uint8)
        self.lower_orange = np.array([10,140,100], dtype=np.uint8)
        self.upper_orange = np.array([24,255,255], dtype=np.uint8)
        self.lower_green = np.array([37,80,100], dtype=np.uint8)
        self.upper_green = np.array([100,255,255], dtype=np.uint8)
        self.lower_red1 = np.array([0,80,100], dtype=np.uint8)
        self.upper_red1 = np.array([7,255,255], dtype=np.uint8)
        self.lower_red2 = np.array([160,80,100], dtype=np.uint8)
        self.upper_red2 = np.array([179,255,255], dtype=np.uint8)

    def getCubeState(self):
        self.rawBRD = self.getImage(cameras['BRD'])
        self.rawRUF = self.getImage(cameras['RUF'])
        self.rawUBL = self.getImage(cameras['UBL'])

        self.imageBRD = self.cropRawImage(rawBRD, cameras['BRD'])
        self.imageRUF = self.cropRawImage(rawRUF, cameras['RUF'])
        self.imageUBL = self.cropRawImage(rawUBL, cameras['UBL'])

        self.heightimage, self.widthimage, self.channelsimage = self.imageBRD.shape
        self.portholeMask = createPortholeMask(self.heightimage, self.widthimage,
        self.channelsimage)

        # Initialise known/assumed centre cubies
        # TODO This needs to be reworked for the next iterations
        self.cubes[4 ] = "U"
        self.cubes[13] = "R"
        self.cubes[22] = "F"
        self.cubes[31] = "D"
        self.cubes[40] = "L"
        self.cubes[49] = "B"

        self.extractColours(imageBRD, self.cameras['BRD'])
        self.extractColours(imageRUF, self.cameras['RUF'])
        self.extractColours(imageUBL, self.cameras['UBL'])

        return self.cubes


    def getImage(cameraNumber):
        camera = cv2.VideoCapture(cameraNumber)

        for i in xrange(30):
            temp = camera.read()
        null, cameraCapture = camera.read()

        del(camera)
        return cameraCapture


    def cropRawImage(rawImage, cameraNumber):
        #TODO This needs to be reworked: independently configurable from the
        # calibration window
        if cameraNumber == 0:
            croppedImage = rawImage[55:455, 120:505]
        elif cameraNumber == 1:
            croppedImage = rawImage[50:450, 135:520]
        else:
            croppedImage = rawImage[45:445, 135:520]

        return croppedImage


def correlateCubePosition(cameraNum, contourX, contourY):
    positionCount = 0

    for coordinates in self.correlation[cameraNum,]:
    # TODO This is a square, not a circle!
        if (coordinates != 0):
        # TODO avoid NULL coordinate entries: Also, check list type?
            if (math.fabs(coordinates[0] - contourX) < self.offset and
                    math.fabs(coordinates[1] - contourY) < self.offset):
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

    if ( (listPos is None) or (listPos < 0) or (listPos > len(self.cubes)) ):
        print("Index in cubes list is not valid")
        error = True

    #if (cubes[listPos]):
    #    print("Cubelist is already populated in position")

    # TODO this check is not valid when the list is unpopulated (to start)
    #if (cubes[listPos] != colours[colour] ):
    #    print("Colour insertion disagrees with existing")
    #    error = True

    if (error == True):
        return

    self.cubes[listPos] = self.colours[colour]


    def extractColours(image, cameraNum):
    # TODO this needs reworked a lot
    #YELLOW cube detection
        yellowHSVMask = getColourMask(image ,self.lower_yellow, self.upper_yellow)

        yellowContours, hierarchy_y = cv2.findContours(yellowHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # TODO Is this correct?
        cnts = sorted(yellowContours, key = cv2.contourArea, reverse = True)[:25]

        # TODO Is this correct?
        for c in cnts:
            M = cv2.moments(c)
            area = cv2.contourArea(c)

            #TODO Why is the decision amde this way?
            if M["m00"] != 0 and area > self.minimumContourArea:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            listPosition = correlateCubePosition(cameraNum, cX, cY)
            if (listPosition is not None):
                self.listifyCubePosition(listPosition, 3)

    #BLUE cube detection
        blueHSVMask = getColourMask(image ,self.lower_blue, self.upper_blue)

        blueContours, hierarchy_b = cv2.findContours(blueHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(blueContours, key = cv2.contourArea, reverse = True)[:25]

        for c in cnts:
            M = cv2.moments(c)
            area = cv2.contourArea(c)

            if M["m00"] != 0 and area > self.minimumContourArea:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            listPosition = correlateCubePosition(cameraNum, cX, cY)
            if (listPosition is not None):
                self.listifyCubePosition(listPosition, 1)

    #ORANGE cube detection
        orangeHSVMask = getColourMask(image, self.lower_orange, self.upper_orange)
        orangeContours, hierarchy_o = cv2.findContours(orangeHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cnts = sorted(orangeContours, key = cv2.contourArea, reverse = True)[:25]

        for c in cnts:
            M = cv2.moments(c)
            area = cv2.contourArea(c)

            if M["m00"] != 0 and area > self.minimumContourArea:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            listPosition = correlateCubePosition(cameraNum, cX, cY)
            if (listPosition is not None):
                self.listifyCubePosition(listPosition, 5)

    #GREEN cube detection
        greenHSVMask = getColourMask(image, self.lower_green, self.upper_green)
        greenContours, hierarchy_g = cv2.findContours(greenHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cnts = sorted(greenContours, key = cv2.contourArea, reverse = True)[:25]

        for c in cnts:
            M = cv2.moments(c)
            area = cv2.contourArea(c)

            if M["m00"] != 0 and area > self.minimumContourArea:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            listPosition = correlateCubePosition(cameraNum, cX, cY)
            if (listPosition is not None):
                self.listifyCubePosition(listPosition, 4)

    #RED cube detection
        redHSVMask1 = getColourMask(image, self.lower_red1, self.upper_red1)
        redHSVMask2 = getColourMask(image, self.lower_red2, self.upper_red2)
        redHSVMask = cv2.bitwise_or(redHSVMask1, redHSVMask2)

        redContours , hierarchy_r = cv2.findContours(redHSVMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(redContours, key = cv2.contourArea, reverse = True)[:25]

        for c in cnts:
            M = cv2.moments(c)
            area = cv2.contourArea(c)

            if M["m00"] != 0 and area > self.minimumContourArea:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            listPosition = correlateCubePosition(cameraNum, cX, cY)
            if (listPosition is not None):
                self.listifyCubePosition(listPosition, 2)
