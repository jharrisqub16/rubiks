################################################################################
# Script to prompt user to input move to pass on to the arduino.
# Can be used to debug motor issues
################################################################################
import serial

from random import randint

########################################
## MISC VARIABLES
########################################

validMoves={"U","F","D","R","L","B","U'","F'","D'","R'","L'","B'","U2","F2","D2","R2","L2","B2"}

def main():
    print("Enter cube move:")

    arduino = serial.Serial('/dev/ttyACM0', 9600)

    while (1):

        userInput = str(raw_input())
        if userInput in validMoves: 
            arduino.write(userInput+" ")
        else:
            print("Not a valid move")

main()
