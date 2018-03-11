import kociemba

from collections import Counter


class cubeSolver():
    def __init__(self):
        pass

    def solve(self, cubeState):
        self.cubeState = cubeState

        # Rough validation of cube state
        self.cubieCounts = Counter(self.cubeState)

        colours = {0: 'U', 1: 'R', 2: 'F', 3: 'D', 4: 'L', 5: 'B'}

        print("Cubie counts")
        print(self.cubieCounts)

        for colour in colours:
            if (self.cubieCounts[colours[colour]] != 9):
                print("Incorrect number of colours detected")
                raise Exception("Expected 9 cubies of each colour")

        self.cubeString = ''.join(self.cubeState)
        # Find cube solution
        try:
            self.solution = kociemba.solve(self.cubeString)
            return self.solution
        except ValueError:
            pass
            # TODO Exception handling


    def calculateFaceTurnLength(self, solutionString):
        # Takes space-delimited solution sequence and calculates its cost, based
        # on the face-turn metric
        solutionLength = (solutionString.count(' ')) if (solutionString.endswith(' ')) else (solutionString.count(' ') + 1)

        return solutionLength


    def calculateQuarterTurnLength(self, solutionString):
        # Takes space-delimited solution sequence and calculates its cost, based
        # on the quarter-turn metric

        # Get the base number of moves in the sequence
        solutionLength = self.calculateFaceTurnLength(solutionString)

        # Add *2 moves
        solutionLength += solutionString.count("2")

        return solutionLength
