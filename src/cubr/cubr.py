
# cubr is the main class for the solver, including subclasses responsible for:
#   -computer vision on Rubik's cube
#   -solving algorithm for producing solution sequence
#   -motor control
#
# The cubr class itself should provide all of the API for the GUI, such as all
# the button bindings (solve etc), video stream provision and
# calibration/configuration API.

# This will also be the de-facto point for handling exceptions

# Theoretically, these logical units can be easily adapted/replaced to suit
# future iterations of the solvers.

from computerVision import computerVision
from motorController import motorController
from solver import cubeSolver

from random import randint

import time

class cubr():
    def __init__(self):

        # TODO handle exceptions of trying to create these objects
        self.cv = computerVision()
        self.solver = cubeSolver()
        self.mc = motorController()

        #TODO not sure where this should originate: for second iteration,
        # probably needs to be derived by CV, and passed on as required.
        self.colours = {0: 'U', 1: 'R', 2: 'F', 3: 'D', 4: 'L', 5: 'B'}


    def solveCube(self):
        start = time.time()
        # TODO Also add exception handling
        cubeState = self.cv.getCubeState()
        #TODO check if cubeState is already solved:
        read = time.time()
        solution = self.solver.solve(cubeState)
        #TODO must be valid string solution
        self.mc.sendString(solution)
        end = time.time()
        print("Elapsed time: {0}".format(end-start))
        print("Cube read in: {0}".format(read-start))


    def scramble(self):
        scramble = []

        moves = randint(10,30)

        for x in range(0, moves):
            operation = randint(0,5)

            # Perform half turn (2X) if 1
            double = randint(0,1)

            if double == 0 :
                scramble.append(self.colours[operation])
            else:
                scramble.append("2"+self.colours[operation])

        scrambleString = ' '.join(scramble)

        self.mc.sendString(scrambleString)


    def getImage(self):
        guiImage = self.cv.getGuiImage()

        return guiImage

    def goToNextViewingPosition(self):
        # This function causes the next 'viewing position' to be returned by getImage()
        # This could be:
        # - Progressing to the next camera (multi camera robots)
        # - Rotating the cube to the next position (single camera robots)
        self.cv.nextGuiImageSource()

        return


    def setRoiHighlighting(self, stateBool):
        self.cv.setRoiHighlighting(stateBool)


    def setContourHighlighting(self, stateBool):
        self.cv.setContourHighlighting(stateBool)


    def setColourConstancy(self, stateBool):
        self.cv.setColourConstancy(stateBool)


    def roiShiftHandler(self, coords):
        self.cv.roiShiftHandler(coords)


    def calibrateColourHandler(self, colour, coords):
        self.cv.calibrateColourHandler(colour, coords)
