# Cuber is the main class for the solver, including subclasses responsible for:
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

class Cuber():
    def __init__(self):

        # TODO handle exceptions of trying to create these objects
        self.cv = computerVision()
        self.solver = cubeSolver()
        self.mc = motorController()

        # Pre-defined list of the solved state: used for verification
        self.solvedState = ('U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U',
                            'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R',
                            'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F',
                            'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D',
                            'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L',
                            'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B')

        #TODO not sure where this should originate: for second iteration,
        # probably needs to be derived by CV, and passed on as required.
        self.colours = {0: 'U', 1: 'R', 2: 'F', 3: 'D', 4: 'L', 5: 'B'}


    def solveCube(self):
        startTime = time.time()
        # TODO Also add exception handling
        cubeState = self.cv.getCubeState()
        readTime = time.time()

        if (tuple(cubeState) == self.solvedState):
            print("Cube already in solved state.")
            return

        solution = self.solver.solve(cubeState)
        if solution is None:
            raise Exception("No cube solution could be found")

        solveTime = time.time()

        self.mc.sendString(solution, waitForAck=True)
        endTime = time.time()

        faceTurnLength = self.solver.calculateFaceTurnLength(solution)
        quarterTurnLength = self.solver.calculateQuarterTurnLength(solution)

        # Calculate the relevant time intervals
        totalTime = endTime-startTime
        cvReadTime = readTime-startTime
        algorithmTime = solveTime-readTime
        motorTime = endTime-solveTime

        # Print some formatted timing output
        print("########################################")
        print("Elapsed time: {0}".format(totalTime))
        print("CV Read time: {0}".format(cvReadTime))
        print("Solve time:   {0}".format(algorithmTime))
        print("Motor time:   {0}".format(motorTime))
        print("Solution:     {0}".format(solution))
        print("Face-turns:   {0}".format(faceTurnLength))
        print("Quarter-turns:{0}".format(quarterTurnLength))
        print("########################################")

        # Verify solution
        verifyState = self.cv.getCubeState()
        print("post state: {0}".format(verifyState))

        if (tuple(verifyState) == self.solvedState):
            print("Cube solved")
        else:
            print("Could not verify solution success")


    def scrambleCube(self):
        scrambleSequence = []

        moves = randint(10,30)

        operation = None
        lastOperation = None

        for x in range(0, moves):
            operation = randint(0,5)
            while (operation == lastOperation):
                operation = randint(0,5)

            lastOperation = operation

            # Perform half turn (2X) if 1
            rotation = randint(0,2)

            if rotation == 0 :
                # Apply ACW rotation
                scrambleSequence.append(self.colours[operation] + "'")
            elif rotation == 1:
                # Apply half turn (180 degree) rotation
                scrambleSequence.append(self.colours[operation] + "2")
            else:
                # Normal CW rotation
                scrambleSequence.append(self.colours[operation])

        scrambleString = ' '.join(scrambleSequence)
        print("scramble:{}".format(scrambleString))

        self.mc.sendString(scrambleString, waitForAck=True)

        # Update state of cube (for user view) once motor rotations are complete
        null = self.cv.getCubeState()


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

    def roiDragSet(self, coords):
        self.cv.roiDragSet(coords)


    def roiDrag(self, coords):
        self.cv.roiDrag(coords)


    def roiDragEnd(self):
        self.cv.roiDragEnd()


    def calibrateColourHandler(self, colour, coords):
        self.cv.calibrateColourHandler(colour, coords)


    def getColourCorrelationValues(self):
        return self.cv.getColourCorrelationValues()


    def discardStateChanges(self):
        self.cv.discardCorrelationChanges()

    def saveState(self):
        self.cv.saveCorrelation()
