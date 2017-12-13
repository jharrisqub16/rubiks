import serial

class motorController:
# TODO For now this is just a replacement of existing functionality,
#   consolidated into one class.

# However, in the future, this could be made smarter eg:
#   - configurable speed/acceleration of the arduino motor controller.
#   - Ack from the arduino to confirm move completion. This can be used for
#       timing the solution (as well as smarted operation and feedback to the GUI)

    def __init__(self):
        # TODO This should probably be configurable from the GUI/settings menu
        self.serialPort = "/dev/ttyACM0"
        self.serialBaudRate = 9600

        self.serialDevice = serial.Serial(self.serialPort, self.serialBaudRate)

    def sendString(self, solutionString):
        self.serialDevice.write(solutionString)

