import cv2
import math
import numpy as np

from correlation import *


class computerVision():
    def __init__(self):
        # Note this list is used to handle all variations in camera order.
        # In most instances, the index of this array is used, not the sequence
        # in the list itself.
        # ie. no matter the order of cameras in this list, the cameras are
        # iterated through in element order.
        self.cameras = [0, 1, 2]
        self.noOfCameras = len(self.cameras)

        # NB The capture objects are in the same index as self.cameras
        self.captureObjects = []
        for cameraNum in self.cameras:
            tempCamera = cv2.VideoCapture(cameraNum)

            # Set camera resolution to 320x240
            tempCamera.set(3, 320)
            tempCamera.set(4, 240)

            if not tempCamera.isOpened():
                raise Exception("Camera Index {0} could not be opened".format(cameraNum))

            self.captureObjects.append(tempCamera)

        self.colours = {0:'U',1:'R',2:'F',3:'D',4:'L',5:'B'}

        try:
            # Open correlation config file if it exists
            self.correlation = np.load('cfg/correlation.npy')
        except:
            self.correlation = correlation

        # TODO Hack: Backup versions of all configurable objects will be held:
        # This allows the 'current' variable to be reverted when changes are being discarded.
        # For not at least, it is easier that these objects are told to simply save or discard changes,
        # rather than creating backups (only as required) when config changes have been made to them.
        self.correlationBackup = np.copy(self.correlation)

        self.cubeState = [None]*54
        self.contourList = [None]*54

        # Some CV reference values
        self.minimumContourArea = 20
        self.offset = 11
        self.altOffset = 20

        # Draw values for visual debugging contours
        self.drawColourValues = {   'Y': (  0,255,255),
                                    'B': (255,  0,  0),
                                    'O': (  0,160,255),
                                    'G': (  0,255,  0),
                                    'R': (  0,  0,255)}

        #self.colourCorrelation = {  'Y': (( 28, 70,180), ( 41,255,255)),
        #                            'B': ((100, 90,100), (120,255,255)),
        #                            'O': (( 10,190,200), ( 28,255,255)),
        #                            'G': (( 50,100,100), ( 90,255,255)),
        #                            'R': ((  0, 80,100), ( 10,255,255))}

        self.colourCorrelation = {  'Y': (( 26, 70,180), ( 36,255,255)),
                                    'B': ((100, 60,100), (150,255,255)),
                                    'O': (( 10,140,200), ( 24,255,255)),
                                    'G': (( 37, 80,100), (100,255,255)),
                                    'R': ((  0, 80,100), ( 7,255,255))}

        # Defines which camera's image will be output to the GUI:
        # This is done to confine of the number of cameras, capture objects etc
        # inside this computerVision class
        self.guiDisplayCameraIndex = 0
        self.highlightRoiBool = False
        self.highlightContoursBool = False
        self.applyColourConstancyBool = False


################################################################################
## Main 'top level' functions
################################################################################

    def getCubeState(self):
        #   1) Get contour list: List of largest contour in each ROI
        #       Plus other information: - Area (used for insertion)
        #                                 Colour
        #
        #   2) Work out (or assume) relationship between colours and faces
        #
        #   3) Translate contour/colours list into colour notation
        #       produces cubeState list
        self.getMaskedImages()

        # Ensure cube lists are reset
        self.cubeState = [None]*54
        self.contourList = [None]*54

        # This section/loop acts on the gathered images to read the colours from the images
        print(self.contourList.count(None))
        for cameraNum in range(self.noOfCameras):
            self.extractColours(self.maskedImages[cameraNum], cameraNum)
            print(self.contourList.count(None))

        # TODO Assume the centre cubes (ie the orientation of the cube) in this iteration
        self.cubeState[4 ] = "U"
        self.cubeState[13] = "R"
        self.cubeState[22] = "F"
        self.cubeState[31] = "D"
        self.cubeState[40] = "L"
        self.cubeState[49] = "B"

        self.colourFaceCorrelation = self.getColourFaceCorrelation()

        position = 0
        for contour in self.contourList:
            if contour is not None:
                self.listifyCubePosition(position, self.colourFaceCorrelation[contour[2]])

            position += 1

        # TODO Assume all 'unmatched' cubies are white: White is not explicitly detected
        self.cubeState = [ x if x is not None else 'U' for x in self.cubeState]

        return self.cubeState

################################################################################
## Camera interface functions
################################################################################

    def getMaskedImages(self):
        # Get masked images from all cameras, and populate these into list (for later use)
        self.maskedImages = []
        self.rawImages = []
        for cameraNum in range(self.noOfCameras):
            # Get image from camera
            rawImage = self.getCvImage(cameraNum)
            self.rawImages.append(rawImage)

            # Get required sizes and create 'porthole' RoI mask
            imageHeight, imageWidth, imageChannels = rawImage.shape
            portholeMask = self.createPortholeMask(imageHeight, imageWidth, imageChannels, cameraNum)

            # Apply mask to image, and add into list of images
            self.maskedImages.append(cv2.bitwise_and(rawImage, rawImage, mask = portholeMask))

        # Output debug images
        for cameraNum in range(self.noOfCameras):
            cv2.imwrite("outputImages/mask{0}.jpg".format(cameraNum), self.maskedImages[cameraNum])


    def getCvImage(self, cameraNum):
        rawImage = self.captureImage(cameraNum)

        return rawImage


    def getGuiImage(self):
        # - Get image from relevant camera
        # - Convert from BGR to RGB
        # - Apply filters and debug info as required

        frame = self.getCvImage(self.guiDisplayCameraIndex)

        # Draw the visual debug information onto the frame
        frame = self.drawGuiDebug(frame)

        # Convert from BGR (opencv) to RGB representation
        displayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        return displayImage

    def drawGuiDebug(self, image):
        # Helper function for returning the GUI image:
        # Optionally draws the various visual debug onto the returned image

        if self.applyColourConstancyBool:
            # TODO
            print("Constancy")

        if self.highlightRoiBool:
            # self.cameras is used to obtain ACTUAL camera number, not the index
            # Hence, the index in correlation also refers to the actual camera number
            for coordinates in self.correlation[self.cameras[self.guiDisplayCameraIndex]]:
                if (coordinates != 0 and coordinates is not None):
                    # Draw Region of Interest Circle on the GUI image (in black)
                    cv2.circle(image, coordinates, self.offset, (0, 0, 0) , 2)

        if self.highlightContoursBool:
            if self.cubeState == [None]*len(self.cubeState):
                # cubestate has not yet been retrieved
                print("Forced to initialise cubeState")
                null = self.getCubeState()

            for contour in self.contourList:
                if (contour is not None and contour[1] == self.guiDisplayCameraIndex):
                    cv2.drawContours(image, contour[0], -1, (contour[3]), 2)

        return image


    def captureImage(self, cameraNumber):
        # Helper function for retrieving all images from cameras
        tempCamera = self.captureObjects[cameraNumber]

        # Taking at least 1 'dummy' capture is often required to 'normalise' the camera
        for i in xrange(1):
            temp, dumpCapture = tempCamera.read()
            #cv2.imwrite("outputImages/rawcamera{0}{1}.jpg".format(cameraNumber, i), dumpCapture)
        null, cameraCapture = tempCamera.read()

        return cameraCapture

################################################################################
## Misc API handler functions
################################################################################

    def nextGuiImageSource(self):
        if self.guiDisplayCameraIndex == (len(self.captureObjects) -1):
            # Wrap to start of camera list
            self.guiDisplayCameraIndex = 0

        else:
            self.guiDisplayCameraIndex += 1


    def setRoiHighlighting(self, stateBool):
        self.highlightRoiBool = stateBool


    def setContourHighlighting(self, stateBool):
        self.highlightContoursBool = stateBool


    def setColourConstancy(self, stateBool):
        self.applyColourConstancyBool = stateBool


    def roiShiftHandler(self, eventCoordinates):
        print("Clicked on camera {0}, coords{1}".format(self.cameras[self.guiDisplayCameraIndex], eventCoordinates))

        positionCount = 0
        for coordinates in self.correlation[self.cameras[self.guiDisplayCameraIndex], ]:
            if (coordinates != 0 and coordinates is not None):
                if (math.fabs(coordinates[0] - eventCoordinates[0]) < self.offset and
                        math.fabs(coordinates[1] - eventCoordinates[1]) < self.offset):
                    # We have found the region that was clicked in: Break from loop
                    break
            positionCount += 1

        if positionCount < len(self.correlation[self.cameras[self.guiDisplayCameraIndex], ]):
            # If valid (ie in range) region is found, update the correlation of this clicked
            # region to the new coordinate values
            print("Clicked in region index {0}".format(positionCount))
            self.correlation[self.cameras[self.guiDisplayCameraIndex], positionCount] = eventCoordinates
        else:
            # Valid RoI could not be found.
            print("Valid region could not be found")


    def calibrateColourHandler(self, colour, coords):
        # Handler function to change expected colour values based on where the user has clicked on the
        # currently displayed image.
        # TODO none of this is implemented currently
        print("Recalibrated to coords {0} on camera{1}".format(self.cameras[self.guiDisplayCameraIndex], coords))


################################################################################
## Computer vision processing and helper functions
################################################################################

    def createPortholeMask(self, height, width, channels, cameraNum):
        # Create blank 'white' mask
        cubiesMaskTemp = np.zeros((height, width, channels), np.uint8)

        for coordinates in self.correlation[cameraNum,]:
            if (coordinates != 0 and coordinates is not None):
                cv2.circle(cubiesMaskTemp, coordinates, self.offset, (255,255,255), -1)

        ## Create proper mask
        cubiesMaskFinal = cv2.inRange(cubiesMaskTemp, (1,1,1), (255,255,255))

        return cubiesMaskFinal


    def correlateCubePosition(self, cameraNum, contourX, contourY):
        positionCount = 0

        for coordinates in self.correlation[cameraNum,]:
        # TODO This is a square, not a circle!
            if (coordinates != 0 and coordinates is not None):
            # TODO avoid NULL coordinate entries: Also, check list type?
                if (math.fabs(coordinates[0] - contourX) < self.offset and
                        math.fabs(coordinates[1] - contourY) < self.offset):
                    return positionCount
            positionCount += 1


    def listifyCubePosition(self, listPos, colour):
        # Insert cube colour into the cube state list with the appropriate
        # validation.

        # This should validate that:
        #   - listPos is a number, and within limits.
        #   - Contour is not attempted to be inserted twice? At the very least, it
        #       should not disagree with existing.

        # TODO For now this just returns silently but this should probably be fatal
        #   by returning an Input/CV exception

        error = False

        # The index for insertion must be valid
        if ( (listPos is None) or (listPos < 0) or (listPos > len(self.cubeState)) ):
            print("Index in cubes list is not valid")
            error = True

        # If the desired element of the array is already populated, it should
        # not disagree with any further insertions.
        # This should not even apply to most solvers: However, it might help to
        # indicate issues where the coordinates/cube position correlation are
        # totally incorrect
        if (self.cubeState[listPos] and self.cubeState[listPos] != colour ):
            print("Colour insertion disagrees with existing")
            error = True

        if (error == True):
            return

        # Validation passed: Insert colour in the cubeState list
        self.cubeState[listPos] = colour


    def extractColours(self, image, cameraNum):
        for colourValueCorrelation in self.colourCorrelation:

            tempLowerLimit = self.colourCorrelation[colourValueCorrelation][0]
            tempUpperLimit = self.colourCorrelation[colourValueCorrelation][1]

            tempMask = self.getColourMask(image, tempLowerLimit, tempUpperLimit)

            contours, hierarchy = cv2.findContours(tempMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Sort contours such that insertion of largest contours will occur last
            cnts = sorted(contours, key = cv2.contourArea)[:25]

            for c in cnts:
                M = cv2.moments(c)
                area = cv2.contourArea(c)

                if M["m00"] != 0 and area > self.minimumContourArea:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                # TODO why is this else needed?
                else:
                    cX, cY = 0, 0

                listPosition = self.correlateCubePosition(cameraNum, cX, cY)
                if (listPosition is not None):
                    if (self.contourList[listPosition] is None or cv2.contourArea(self.contourList[listPosition][0]) < area):
                        # Insert this contour into the contour list

                        # Contour inserted as 'contour, cameraNum, colourName, drawColourList'
                        self.contourList[listPosition] = [c, cameraNum, colourValueCorrelation, self.drawColourValues[colourValueCorrelation]]


    def getColourMask(self, colouredImage, lowerThreshold, upperThreshold):
        hsvImage = cv2.cvtColor(colouredImage, cv2.COLOR_BGR2HSV)
        thresholdContour = cv2.inRange(hsvImage, lowerThreshold, upperThreshold)
        null, thresholdImage = cv2.threshold(thresholdContour, 127,255,3)

        return thresholdImage


    def getColourFaceCorrelation(self):
        # For the list of contours (namely including colours in positional list)
        # work out (or assume in this case) the relationship between the colour
        # of the faces, and what face notation that corresponds to.
        temp = {    'Y':'D',
                    'B':'R',
                    'O':'B',
                    'G':'L',
                    'R':'F',
                    'W':'U'}

        return temp


################################################################################
## Handle persistent changes to config
################################################################################


    def discardCorrelationChanges(self):
        # Reset correlation to the 'pre-changes' version
        self.correlation = np.copy(self.correlationBackup)
        print("discarding")


    def saveCorrelation(self):
        # TODO
        # Update both the current and the backup to the 'updated' state:
        # This is to expect/handle further changes being made
        print("saving")
        self.correlationBackup = np.copy(self.correlation)
        np.save('cfg/correlation.npy', self.correlation)
