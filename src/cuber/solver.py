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

        print(f"Cube State before join: {self.cubeState}")
        self.cubeString = ''.join(self.cubeState)
        print(f"Cube String after join: {self.cubeString}")
        print(f"Now finding solution")

        # Find cube solution

        try:
            print(f"Cube String: {self.cubeString}")
            #self.solution = kociemba.solve("FLBFULDFULDRBRUDBBLRBDFDUBRFLFRDUDUUULFBLFLDLDURFBRRRB")
            self.solution = kociemba.solve(str(self.cubeString))
            print(f"String Solver: {self.solution}")

            return self.solution
        except ValueError as e:
            print(e)
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
