import serial

class motorController:
# TODO: in the future, this could be made smarter eg:
#   - configurable speed/acceleration of the arduino motor controller.
#   - Ack from the arduino to confirm move completion. This would be used to
#       allow the GUI to be smarter (update the current state automatically, etc)

    def __init__(self):
        # TODO This should probably be configurable from the GUI/settings menu
        # Creation should fail but not fatally: changing the serial device

        self.serialPort = "/dev/ttyACM0"
        self.serialBaudRate = 9600

        self.serialDevice = serial.Serial(self.serialPort, self.serialBaudRate)

    def sendString(self, solutionString, waitForAck=False, timeoutLen=10):

        # Workaround for motorController falling over if string does not end
        # with space
        if (not solutionString.endswith(' ')):
            solutionString += ' '

        self.serialDevice.write(solutionString)

        if (waitForAck == True):
            self.waitForAck(timeoutLen)


    def waitForAck(self, timeoutLen):
        self.serialDevice.timeout = timeoutLen
        print("Serial timeout set to {0}".format(self.serialDevice.timeout))

        readin = self.serialDevice.readline()

        if len(readin) > 0:
            # Valid response/ACK returned
            return
        else:
            # TODO No valid ack: Timeout occured
            print("NO ACK!")
