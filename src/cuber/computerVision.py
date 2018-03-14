import cv2
import math
import os
import numpy as np
import colorsys as cs
import copy
import itertools

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

        # Work out the absolute paths to expected configuration files
        self.directoryPath = os.path.dirname(os.path.abspath( __file__ ))
        self.coordinateCorrelationRelPath = '/../cfg/correlation.npy'
        self.colourCorrelationRelPath = '/../cfg/colours.npy'
        self.coordinateCorrelationPath = self.directoryPath + self.coordinateCorrelationRelPath
        self.colourCorrelationPath = self.directoryPath + self.colourCorrelationRelPath

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

        # Load coordinate correlation configuration
        try:
            # Open correlation config file if it exists
            self.correlation = np.load(self.coordinateCorrelationPath)
            print('Coordinate correlation loaded from: {0}'.format(self.coordinateCorrelationPath))
        except:
            # Load 'default' python correlation if config file does not exist
            print('Loading default coordinate configuration')
            self.correlation = correlation

        # Load colour correlation configuration
        try:
            # Open correlation config file if it exists
            self.colourCorrelation = np.load(self.colourCorrelationPath).item()
            print('Colour correlation loaded from: {0}'.format(self.colourCorrelationPath))
        except:
            # Load 'default' python correlation if config file does not exist
            print('Loading default colour configuration')
            self.colourCorrelation = {  'Y': ( 26, 70,180),
                                        'B': (120, 60,100),
                                        'O': ( 10,140,200),
                                        'G': ( 90,200,100),
                                        'W': (100, 30,100),
                                        'R': (  0, 80,100)}

        # Backup versions of all configurable objects will be held:
        # This allows the 'current' variable to be reverted when changes are being discarded.
        # For now at least, it is easier that these objects are told to simply save or discard changes,
        # rather than creating backups (only as required) when config changes have been made to them.
        self.coordinateCorrelationBackup = np.copy(self.correlation)
        self.colourCorrelationBackup = self.colourCorrelation.copy()

        self.cubeState = None
        self.colourList = [None]*54

        # NOTE Contour list contains elemnts of [contour, area, cameraNum, averageHsvColour]
        self.contourList = [None]*54

        self.maskedImages = []
        self.hsvImages = []
        self.rawImages = []

        # Some CV reference values
        self.minimumContourArea = 20
        self.offset = 10
        self.altOffset = 20

        # Defines which camera's image will be output to the GUI:
        # This is done to confine of the number of cameras, capture objects etc
        # inside this computerVision class
        self.guiDisplayCameraIndex = 0
        self.highlightRoiBool = False
        self.highlightContoursBool = False
        self.applyColourConstancyBool = False

        self.dragActiveBool = False
        self.dragItemIndex = 0,0


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

        # Populate all the required image lists
        self.populateCvImages()

        # Ensure cube lists are reset
        self.cubeState = [None]*54
        self.contourList = [None]*54
        self.colourList = [None]*54

        # This section/loop acts on the gathered images to read the colours from the images
        for cameraNum in range(self.noOfCameras):
            self.extractContours(self.maskedImages[cameraNum], cameraNum)

        self.colourList = self.extractColoursFromContours(self.contourList, self.colourCorrelation)

        # NOTE: Assume the centre cubes (ie the orientation of the cube) in this iteration
        self.colourList[4 ] = "W"
        self.colourList[13] = "B"
        self.colourList[22] = "R"
        self.colourList[31] = "Y"
        self.colourList[40] = "G"
        self.colourList[49] = "O"

        self.colourList = [ x if x is not None else 'W' for x in self.colourList]

        # Figure out/assume the orienation of the cube
        # ie Correlate the colour letter to the face notation
        self.colourFaceCorrelation = self.getColourFaceCorrelation()

        # Use colour-face correlation to convert colour list into cube state
        self.cubeState = self.convertColoursToFaceNotation(self.colourList)
        print(self.cubeState)

        return self.cubeState


################################################################################
## Camera interface functions
################################################################################

    def populateCvImages(self):
        # Get masked images from all cameras, and populate these into list (for later use)
        self.maskedImages = []
        self.hsvImages = []
        self.rawImages = []

        for cameraNum in range(self.noOfCameras):
            # Get image from camera
            rawImage = self.getCvImage(cameraNum)
            self.rawImages.append(rawImage)

            # Convert to HSV
            hsvImage = cv2.cvtColor(rawImage, cv2.COLOR_BGR2HSV)

            equalisedImage = self.applyColourConstancyHSV(hsvImage)

            self.hsvImages.append(equalisedImage)

            # Apply mask to image, and add into list of images
            imageHeight, imageWidth, imageChannels = rawImage.shape
            portholeMask = self.createPortholeMask(imageHeight, imageWidth, imageChannels, cameraNum)

            #self.maskedImages.append(cv2.bitwise_and(rawImage, rawImage, mask = portholeMask))
            self.maskedImages.append(cv2.bitwise_and(equalisedImage, equalisedImage, mask = portholeMask))

        # Output debug images
        for cameraNum in range(self.noOfCameras):
            cv2.imwrite("outputImages/mask{0}.jpg".format(cameraNum), self.maskedImages[cameraNum])


    def getCvImage(self, cameraNum):
        # Get image using helper function:
        # It is required to ensure the camera buffer is empty so we can be sure
        # that we get an image that is actually 'live'
        rawImage = self.captureImage(cameraNum, True)

        return rawImage


    def getGuiImage(self):
        # - Get image from relevant camera
        # - Convert from BGR to RGB
        # - Apply filters and debug info as required

        # Use helper function to grab image from camera. Since frames are being
        # streamed to the GUI, we do not need to worry about emptying the
        # buffer totally: That will sort itself out.
        frame = self.captureImage(self.guiDisplayCameraIndex, False)

        # Draw the visual debug information onto the frame
        frame = self.drawGuiDebug(frame)

        # Convert from BGR (opencv) to RGB representation
        displayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        return displayImage

    def drawGuiDebug(self, image):
        # Helper function for returning the GUI image:
        # Optionally draws the various visual debug onto the returned image

        if self.applyColourConstancyBool:
            image = self.applyColourConstancyRGB(image)

        if self.highlightRoiBool:
            # self.cameras is used to obtain ACTUAL camera number, not the index
            # Hence, the index in correlation also refers to the actual camera number
            for coordinates in self.correlation[self.cameras[self.guiDisplayCameraIndex]]:
                if (coordinates != 0 and coordinates is not None):
                    # Draw Region of Interest Circle on the GUI image (in black)
                    cv2.circle(image, coordinates, self.offset, (0, 0, 0) , 2)

        if self.highlightContoursBool:
            if self.cubeState is None:
                # cubestate has not yet been retrieved
                print("Forced to initialise cubeState")
                null = self.getCubeState()

            for contour in self.contourList:
                if contour is not None:
                    contourCameraNum = contour[2]
                    if (contour is not None and contourCameraNum == self.guiDisplayCameraIndex):
                        contourArray = contour[0]
                        # Draw contour outline in the average colour of the contour contents
                        contourHsvColour = np.copy(contour[3])

                        # Brighten  the draw colour slightly for visibility
                        contourHsvColour[2] += 10

                        # Convert average HSV colour to RGB for drawing
                        rgbDrawColour = cs.hsv_to_rgb(contourHsvColour[0]/180, contourHsvColour[1]/255, contourHsvColour[2]/255)
                        # Reverse RGB for opencv draw function as this operates on BGR basis
                        rgbDrawColour = rgbDrawColour[::-1]
                        rgbDrawColour = [i*255 for i in rgbDrawColour]


                        cv2.drawContours(image, contourArray, -1, (rgbDrawColour), 2)

        return image


    def captureImage(self, cameraNumber, clearBufferBool):
        # Helper function for retrieving all images from cameras
        tempCamera = self.captureObjects[cameraNumber]

        if clearBufferBool:
            # NOTE WORKAROUND
            # The buffer of the camera stream often causes an old image to be used,
            # which competely ruins the computer vision.
            # Several dummy images are taken to clear this buffer, hence fixing
            # incorrect computer vision output which is made based on old images.
            #
            # On the bright side, this generally only requires significantly more time on the
            # first use of the capture object: During 'normal' usage, these 'excess'
            # frames are only pulled from the buffer (to empty it). Therefore,
            # this does not actually take that much more time compared to
            # taking a single 'fresh' frame.

            # NOTE Setting the buffer length of the capture object is apparently not
            # working or not available for all cameras
            # Another 'valid' solution is to use another thread to continuously pull frames
            # from the camera as fast as possible to keep the buffer empty, to eliminate this
            # problem. This should use 'captureObject.grab()' as this has less overhead

            for i in xrange(4):
                temp, dumpCapture = tempCamera.read()
                cv2.imwrite("outputImages/rawcamera{0}{1}.jpg".format(cameraNumber, i), dumpCapture)
        else:
            # A short (single frame) is needed to normalise some lighting in images:
            # First image often has streaks
            # However, this is intended to be used only for the GUI, so only
            # one dummie image is taken. In this case, emptying the buffer is less
            # important than minimising the wait for each frame, as this
            # ultimately affects the output framerate
            for i in xrange(1):
                temp, dumpCapture = tempCamera.read()
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


    def roiDragSet(self, eventCoordinates):
        # Initialise the drag operation in computer vision:
        # Find the region that the initial click was inside (if any), and keep
        # track of it for continued motion operations

        # Find the element in correlation (if any) that matches the clicked
        # coordinates, within the distance of the RoI radius

        cubePosition = self.correlateCubePosition(self.guiDisplayCameraIndex, eventCoordinates[0], eventCoordinates[1])

        if cubePosition is not None and cubePosition < len(self.correlation[self.cameras[self.guiDisplayCameraIndex], ]):
            # If valid (ie in range) region is found, update the correlation of this clicked
            # region to the new coordinate values
            self.dragActiveBool = True
            self.dragItemIndex = self.guiDisplayCameraIndex, cubePosition
            self.correlation[self.dragItemIndex] = eventCoordinates
        else:
            # Valid RoI could not be found.
            print("Valid region could not be found")

    def roiDrag(self, eventCoordinates):
        # Continuously update the coorelation coordinates according to the
        # stream of motion events

        if self.dragActiveBool:
            self.correlation[self.dragItemIndex] = eventCoordinates


    def roiDragEnd(self):
        # Disable the drag operation
        self.dragActiveBool = False
        self.dragItemIndex = 0,0


    def calibrateColourHandler(self, colourInitial, coords):
        # Handler function to change expected colour values based on where the user has clicked on the
        # currently displayed image.

        # TODO is this number actually correct?
        cameraNum = self.cameras[self.guiDisplayCameraIndex]
        print("Recalibrated colour {} to coords {} on camera {}".format(colourInitial, coords, cameraNum))

        # Update images to ensure we are referencing the latest state
        self.populateCvImages()

        # TODO why do the coordinates want to be reversed here?
        #colourHsvValue = self.hsvImages[cameraNum][coords]
        colourHsvValue = self.hsvImages[cameraNum][coords[1], coords[0]]
        self.colourCorrelation[colourInitial] = colourHsvValue


    def getColourCorrelationValues(self):
        #self.colourCorrelation:

        # Translate HSV correlation into HSV before return
        rgbConvertedDict = {}
        for colour in self.colourCorrelation:
                # Note *1.0 is added to ensure float division. Other options exist but require modification of other sections
                rgbColour = cs.hsv_to_rgb(self.colourCorrelation[colour][0]/(180*1.0), self.colourCorrelation[colour][1]/(255*1.0), self.colourCorrelation[colour][2]/(255*1.0))
                rgbColour = [i*255 for i in rgbColour]
                rgbConvertedDict[colour] = rgbColour

        return rgbConvertedDict


################################################################################
## Colour Constancy helpers
################################################################################

    def applyColourConstancyRGB(self, image):
        # Convert the passed image to HSV colourspace:
        # It is assumes that all colour constancy will be performed in HSV
        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Apply colour constancy algorithm in the HSV space
        equalisedImage = self.applyColourConstancyHSV(hsvImage)

        # Convert image back to RGB for return
        returnImage = cv2.cvtColor(equalisedImage, cv2.COLOR_HSV2BGR)

        return returnImage

    def applyColourConstancyHSV(self, hsvImage):
        # Histogram equalisation
        h, s, v = cv2.split(hsvImage)

        # Equalise the s and v channels
        s = cv2.equalizeHist(s)
        #v = cv2.equalizeHist(v)

        # Recombine channels to produce final, equalised image
        equalisedImage = cv2.merge((h, s, v))

        return equalisedImage


################################################################################
## Computer vision processing and helper functions
################################################################################

    def createPortholeMask(self, height, width, channels, cameraNum):
        # Create blank 'white' mask
        cubiesMaskTemp = np.zeros((height, width, channels), np.uint8)

        for coordinates in self.correlation[self.cameras[cameraNum]]:
            if (coordinates != 0 and coordinates is not None):
                cv2.circle(cubiesMaskTemp, coordinates, self.offset, (255,255,255), -1)

        ## Create proper mask
        cubiesMaskFinal = cv2.inRange(cubiesMaskTemp, (1,1,1), (255,255,255))

        return cubiesMaskFinal


    def correlateCubePosition(self, cameraNum, contourX, contourY):
        # Return the cube position that corresponds to a particular camera and
        # set of coordinates:
        # Returns None if no corresponding cube position is found
        positionCount = 0

        for coordinates in self.correlation[cameraNum,]:
        # NOTE This is a square, not a circle!
        # It does not matter though since the portholes are circular, which
        # limits the contours anyway.
            if (coordinates != 0 and coordinates is not None):
                if (math.fabs(coordinates[0] - contourX) < self.offset and
                        math.fabs(coordinates[1] - contourY) < self.offset):
                    return positionCount
            positionCount += 1


    def listifyCubePosition(self, listPos, colour, colourFaceCorrelation):
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


    def extractContours(self, image, cameraNum):
        # Find the largest contour that exists at each RoI (within the given camera)
        # Key data about each contour is populated into self.contourList for
        # Further processing elsewhere.

        hIncrement = 10

        # Loop through entire H spectrum (circle) in increments
        for h in range(0, 180, hIncrement):

            tempMask = cv2.inRange(image, (h,0,110), (h+hIncrement,255,255))

            contours, hierarchy = cv2.findContours(tempMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Sort contours such that insertion of largest contours will occur last
            cnts = sorted(contours, key = cv2.contourArea)[-25:]

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
                    # Contour exists at a valid cube location
                    if ((self.contourList[listPosition] is None) or (self.contourList[listPosition][1] < area)):
                        # Insert this contour into the contour list if that element is currently empty, or
                        # has smaller area than the new contour

                        # Create individual mask for each validcontour, then
                        # find the average colour it contains
                        contourMask = np.zeros(image.shape, np.uint8)
                        cv2.drawContours(contourMask, c, -1, (255,255,255), thickness=-1)
                        contourMask = cv2.inRange(contourMask, (1,1,1), (255,255,255))

                        averageHsv = np.rint(cv2.mean(image, contourMask))[:3]

                        # Add entry to contour list
                        # NOTE Contour inserted as 'contour, area, cameraNum, averageHsvColour'
                        self.contourList[listPosition] = [c, area, cameraNum, averageHsv]


    def getColourMask(self, hsvImage, lowerThreshold, upperThreshold):
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


    def extractColoursFromContours(self, contourList, colourCorrelation):
        # Convert contour average colour into colour letter representation
        colourList = [None]*len(contourList)
        sortingList = []

        numGroups = 6

        groupWidth = len(contourList)/numGroups
        # NOTE Exclude centres for this robot version
        groupWidth -= 1

        # Form more concise list to make this sorting easier
        # We only care about the average colour, and its cube position
        for index, contour in enumerate(contourList):
            if contour is not None:
                #sortingList.append([contour, index])
                sortingList.append([contour[3], index])

        # Initially sort list according to saturation
        # NOTE: White is difficult to seprate from green/blue by Hue.
        # We are going to assume that white group has the lowest Saturation value instead.
        sortingList = sorted(sortingList, key= lambda sortingList: int(sortingList[0][1]))
        whiteGroup = sortingList[:groupWidth]
        # Now we sort the rest of the list 'normally' by Hue
        sortingList = sorted(sortingList[groupWidth:], key= lambda sortingList: int(sortingList[0][0]))

        bestStdDev = None
        bestPosition = 0
        for position in range(groupWidth):
            # Iterate group position through the list
            totalStdDev = 0
            for group in range(numGroups-1):
                # For each positon, iterate through each group
                tempList = self.getSubList(sortingList, position+(group*groupWidth), groupWidth, True)
                #Add up total std dev of H values
                # TODO S needs to be considered as well
                totalStdDev += np.std([x[0][0] for x in tempList])
                #totalStdDev += np.std(tempList)

            if (bestStdDev is None) or (totalStdDev < bestStdDev):
                bestStdDev = totalStdDev
                bestPosition = position

        # Store according to the smallest colour groupings:
        # Each entry in colourGroupings should represent a set of coherent
        # coloured cubies/positions
        colourGroupings =[]
        averageGroupingColours = []
        for groupNum in range(numGroups-1):
            colourGroupings.append(self.getSubList(sortingList, bestPosition+(groupNum*groupWidth), groupWidth, False))

            averageGroupingColours.append(np.mean([x[0] for x in colourGroupings[groupNum]], axis=0).astype(int))

        # Add the white group back into the mix (it was removed previously)
        colourGroupings.append(whiteGroup)
        averageGroupingColours.append(np.mean([x[0] for x in whiteGroup], axis=0).astype(int))

        # Find all possible orderings of the expected colours
        permutations = list(itertools.permutations(self.colourCorrelation, len(self.colourCorrelation)))
        bestDiff = None
        bestPermutationIndex = 0

        # Find the ordering(permutation) of colours which matches most closely
        # to the measured colour groupings
        for index, perm in enumerate(permutations):
            # For each permutation of the colour correlation dict
            difference = 0
            for count, avgColour in enumerate(averageGroupingColours):
                # Sum difference in H values to find groups closest to template colours
                key = perm[count]
                difference += math.fabs(self.colourCorrelation[key][0] - avgColour[0])

            if bestDiff is None or difference < bestDiff:
                bestDiff = difference
                bestPermutationIndex = index

        bestPermutation = permutations[bestPermutationIndex]
        print(bestPermutation)

        # We now know:
        #   - How the cubies across the cube are grouped into coherent groupings
        #   - A most-likely relationship between these groups and the expected colours
        # Hence, we now expand this relationship to obain the colours of all the cubies
        # across the cube.
        for groupCount, group in enumerate(colourGroupings):
            for colourCount, colour in enumerate(group):
                # Position of this colour in the cube list
                key = colour[1]
                colourList[key] = bestPermutation[groupCount]

        return colourList


    def getSubList(self, completeList, index, groupSize, applyWrapCompensation):
        # Form sublists from a larger list, using an index and an offset.
        # NOTE: In some cases, deviation calculations are required on the sublist,
        # so 'wrapping' is also applied optionally. This subtracts 180 from the Hue value
        # so, while the list values are not completely correct, they present the proper
        # relative deviation between the values.

        # Take a completely new copy to ensure that nothing in the original list gets broken
        tempList = copy.deepcopy(completeList)

        if (index+groupSize <= len(completeList)):
            sublist = tempList[index: (index+groupSize)]

        else:
            # Create list such that it wraps around: negative values for the
            # deviation calculation
            if applyWrapCompensation:
                # Copy 'positive index elements as is
                start = tempList[ : (index+groupSize)%groupSize]

                # Copy 'wrapped' index elements, and -180 to simulate wrapping (for calculations)
                wrapped = tempList[index: ]
                for element in wrapped:
                    element[0][0] -= 180

                # Form complete sublist
                sublist = wrapped + start

            else:
                sublist = tempList[index: ] + tempList[ : (index+groupSize)%groupSize]

        return sublist


    def convertColoursToFaceNotation(self, colourList):
        cubeStateList = [None]*54

        index = 0
        for colour in colourList:
            if colour is not None:
                cubeStateList[index] = self.colourFaceCorrelation[colour]

            index += 1

        return cubeStateList


################################################################################
## Handle persistent changes to config
################################################################################


    def discardCorrelationChanges(self):
        # Reset correlation to the 'pre-changes' version
        print("CV: Discarding coordinate correlation changes")
        self.correlation = np.copy(self.coordinateCorrelationBackup)

        print("CV: Discarding colour correlation changes")
        self.colourCorrelation = self.colourCorrelationBackup.copy()

    def saveCorrelation(self):
        # Update both the current and the backup to the 'updated' state:
        # This is to expect/handle further changes being made
        print("CV: Saving coordinate correlation changes")
        self.coordianteCorrelationBackup = np.copy(self.correlation)
        np.save(self.coordinateCorrelationPath, self.correlation)

        print("CV: Saving colour correlation changes")
        self.colourCorrelationBackup = self.colourCorrelation.copy()
        np.save(self.colourCorrelationPath, self.colourCorrelation)
