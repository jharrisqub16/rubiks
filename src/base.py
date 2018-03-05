#!/usr/bin/python2.7

import sys
import os
import inspect
import threading
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image
from PIL import ImageTk

from calibrate import Calibration


cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"cubr")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from cubr import cubr


class guiMain:
    def __init__(self, master, image):
        # Create cubr API object
        self.cubr = cubr()

        # tk.Tk() master
        self.master = master
        self.master.title("CubeSolver GUI v1")

        # Main parent container for this entire window
        self.mainFrame = tk.Frame(self.master)

        self.calibrationWindowSpawned = False

        # Hard code default window size
        self.windowSize = [320,320]

        # Variables to hold the current scaling ratios
        self.scaleFactor = [1,1]

        # Open main image and convert to tk format
        self.rawImage = Image.open(image)

        # Resize the image to the required size and convert to TK format
        # Since the original image must be preserved, store this in a separate variable
        self.image = self.rawImage.resize(self.windowSize, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)

        # Create main canvas and display image on it
        self.canvas = tk.Canvas(self.mainFrame, width=self.windowSize[0], height=self.windowSize[1])
        self.canvas.bind("<Button 1>", self.onClick)
        self.canvas.bind("<Configure>", self.resizeHandler)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvasImage = self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        # Add generic tag to add children of the canvas ( Used for scaling operations later)
        self.canvas.addtag_all("all")

        # Spawn UI buttons on the canvas using helper function
        self.spawnButtons(self.canvas)

        # Pack the main frame: NB Must set expand option to fill its parent
        self.mainFrame.pack(fill=tk.BOTH, expand=tk.YES)



    def onClick(self, event):
        pass


    def resizeHandler(self, event):
        # Calculate the scaling ratio which the new window size gives
        self.scaleFactor[0] = float(event.width)/self.windowSize[0]
        self.scaleFactor[1] = float(event.height)/self.windowSize[1]

        # Update windowSize variable
        self.windowSize[0] = event.width
        self.windowSize[1] = event.height

        self.image = self.rawImage.resize(self.windowSize, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvasImage, image = self.image)

        # Apply scaling factor to all of the canvas widgets
        self.canvas.scale("all", 0, 0, self.scaleFactor[0], self.scaleFactor[1])


    def spawnButtons(self, container):
        # Pack solve and scramble buttons into their own frame (for placement)
        self.buttonFrame = tk.Frame(container)

        self.scrambleButton = tk.Button(self.buttonFrame, text="Scramble", command=self.scrambleHandler)
        self.solveButton = tk.Button(self.buttonFrame, text="Solve", command=self.solveHandler)
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

            # Create independent window (toplevel), then create calibration object as its child
            self.calibrationWindow = tk.Toplevel(self.master)
            self.calibrationApp = Calibration(self.calibrationWindow, self, self.windowSize)

            self.calibrationWindowSpawned = True
            self.calibrateButton['state'] = 'disabled'

        else:
            # This should not be possible as the button should be inactive
            print("Already has an active child window")


    def scrambleHandler(self):
        scrambleThread = threading.Thread(target=self.cubr.scrambleCube, args=())
        scrambleThread.start()
        #self.cubr.scramble()


    def solveHandler(self):
        solveThread = threading.Thread(target=self.cubr.solveCube, args=())
        solveThread.start()
        #self.cubr.solveCube()


if __name__ == "__main__":
    root = tk.Tk()
    #root.resizable(False, False)

    # Force main window to be square
    root.aspect(1,1,1,1)

    # Form the absolute path of the image so script can be executed from anywhere.
    # Get the base path of this file, then add the assumed path (based on known dir structure)
    cwd = os.path.dirname(__file__)
    imagepath = os.path.join(cwd, 'images', 'rubiksCube.jpg')

    gui = guiMain(root, imagepath)
    root.mainloop()
