################################################################################
# Quick script to generate a pseudo-random sequence of moves and send over
# serial to the arduino motor controller.
################################################################################
import serial

from random import randint

########################################
## MISC VARIABLES
########################################
colours = {0:"U",
           1:"R",
           2:"F",
           3:"D",
           4:"L",
           5:"B",
           }

def main():
    scramble = list()

    # Random number of scrambling moves: At least 10
    #moves = randint(30,40)
    moves = randint(10,30)

    for x in range(0, moves):
        operation = randint(0,5)
        
        # Perform half turn (2X) if 1
        double = randint(0,1)
       
        if double == 0 :
            scramble.append(colours[operation])
        else:
            scramble.append("2"+colours[operation])
        
    scrambleString = ' '.join(scramble)

    print(scrambleString)

    arduino = serial.Serial('/dev/ttyACM0', 9600)
    arduino.write(scrambleString)

main()
