#!/usr/bin/python3

import sys
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image
from PIL import ImageTk

from calibrate import Calibration

if sys.version_info[0] != 3:
    print("This application requires python3+")
    sys.exit(1)


def temp():
    print("Testing callback")


class guiMain(tk.Tk):
    def __init__(self, image):
        super().__init__()

        self.title("CubeSolver GUI v1")

        self.calibrationWindowSpawned = False

        # TODO This should probably be initialised to the size of the rpi screen
        # Also, should the window be adjustable by the user?
        #self.size_x = 500
        #self.size_y = 500
        self.windowSize = 500,500

        self.image = Image.open(image)
        self.image = self.image.resize(self.windowSize, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(self, width=self.windowSize[0], height=self.windowSize[1])
        self.canvas.bind("<Button 1>", self.onClick)
        self.canvas.pack()
        self.canvas.create_image(self.windowSize[0]/2, self.windowSize[1]/2, image=self.image)

        self.spawnButtons()


    def onClick(self, event):
        pass


    def spawnButtons(self):
        # Pack solve and scramble buttons into a frame (for placement)
        self.buttonFrame = tk.Frame(self)

        self.scrambleButton = tk.Button(self.buttonFrame, text="Scramble", command=temp)
        self.solveButton = tk.Button(self.buttonFrame, text="Solve", command=temp)
        self.scrambleButton.pack(side=tk.LEFT)
        self.solveButton.pack(side=tk.LEFT)
        # Place packed frame into a window on the main canvas
        self.buttonWindow = self.canvas.create_window(self.windowSize[0], self.windowSize[1], anchor='se', window=self.buttonFrame)

        # Place calibration button directly onto main canvas
        self.calibrateButton = tk.Button(self.canvas, text="Settings menu", command=self.spawnCalibrationWindow)
        self.calibrateButtonWindow = self.canvas.create_window(0, 0, anchor='nw', window=self.calibrateButton)


    def spawnCalibrationWindow(self):
        # TODO This validation would need to be validated correctly
        # with regard to future excaption handling
        if self.calibrationWindowSpawned == False:
            self.calibrationWindow = Calibration(self, self.windowSize)

            self.calibrationWindowSpawned = True
            self.calibrateButton['state'] = 'disabled'

            #TODO I don't think this should use a mainloop?
            #self.calibrationWindow.mainloop()
        else:
            # This should not be possible as the button should be inactive
            print("Already has an active child window")

if __name__ == "__main__":
    gui = guiMain("images/rubiksCube.jpg")
    gui.mainloop()
