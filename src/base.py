#!/usr/bin/python2.7

import sys
import os
import inspect
import threading
import tkinter as tk
import tkinter.font as TkFont
import tkinter.messagebox as msg
from PIL import Image
from PIL import ImageTk

from calibrate import Calibration


cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"cuber")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from cuber import Cuber


class guiMain:
    def __init__(self, master, image):
        # Create cuber API object
        self.cuber = Cuber()

        self.font= TkFont.Font(size=20)

        # tk.Tk() master
        self.master = master
        self.master.title("CubeSolver GUI v1")

        # Main parent container for this entire window
        self.mainFrame = tk.Frame(self.master)

        self.calibrationWindowSpawned = False

        # Hard code default window size
        # NOTE: This is stored separately to the fullscreen status: Going in and
        # out of fullscreen should still obey the size that the user dragged to.
        self.windowSize = [320,320]
        self.fullscreenBool = False

        # Set fullscreen attributes and bind escape to toggle it
        self.master.attributes("-fullscreen", self.fullscreenBool)
        self.master.bind('<Double-Button-1>', self.toggleFullscreen)

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
        # NOTE: Make the canvas background white to blend with the image (when
        # the image is not fully scaled)
        self.canvas.configure(background='white')
        self.canvas.bind("<Configure>", self.resizeHandler)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvasImage = self.canvas.create_image(self.windowSize[0]/2, 0, image=self.image, anchor='n')

        # Add generic tag to add children of the canvas ( Used for scaling operations later)
        self.canvas.addtag_all("all")

        # Spawn UI buttons on the canvas using helper function
        self.spawnButtons(self.canvas)

        # Pack the main frame: NB Must set expand option to fill its parent
        self.mainFrame.pack(fill=tk.BOTH, expand=tk.YES)


    def toggleFullscreen(self, event):
        self.fullscreenBool = not self.fullscreenBool
        self.master.attributes("-fullscreen", self.fullscreenBool)


    def resizeHandler(self, event):
        # Calculate the scaling ratio which the new window size gives
        self.scaleFactor[0] = float(event.width)/self.windowSize[0]
        self.scaleFactor[1] = float(event.height)/self.windowSize[1]

        # Update windowSize variable
        self.windowSize[0] = event.width
        self.windowSize[1] = event.height

        #self.image = self.rawImage.resize(self.windowSize, Image.ANTIALIAS)
        # NOTE: We assume that hte height will be the smaller of the 2 dimensions
        # and scale 1:1 in this dimension
        self.image = self.rawImage.resize((self.windowSize[1], self.windowSize[1]), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvasImage, image = self.image)

        # Apply scaling factor to all of the canvas widgets
        self.canvas.scale("all", 0, 0, self.scaleFactor[0], self.scaleFactor[1])


    def spawnButtons(self, container):
        # Pack solve and scramble buttons into their own frame (for placement)
        self.buttonFrame = tk.Frame(container)

        self.scrambleButton = tk.Button(self.buttonFrame, font=self.font, text="Scramble", command=self.scrambleHandler)
        self.solveButton = tk.Button(self.buttonFrame, font=self.font, text="Solve", command=self.solveHandler)
        self.scrambleButton.pack(side=tk.LEFT)
        self.solveButton.pack(side=tk.LEFT)
        # Place packed frame into a window on the main canvas
        self.buttonWindow = self.canvas.create_window(self.windowSize[0], self.windowSize[1], anchor='se', window=self.buttonFrame)

        # Place calibration button directly onto main canvas
        self.calibrateButton = tk.Button(self.canvas, font = self.font, text="Settings menu", command=self.spawnCalibrationWindow)
        self.calibrateButtonWindow = self.canvas.create_window(0, 0, anchor='nw', window=self.calibrateButton)


    def spawnCalibrationWindow(self):
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
        scrambleThread = threading.Thread(target=self.cuber.scrambleCube, args=())
        scrambleThread.setDaemon(True)
        scrambleThread.start()
        #self.cuber.scramble()


    def solveHandler(self):
        solveThread = threading.Thread(target=self.cuber.solveCube, args=())
        solveThread.setDaemon(True)
        solveThread.start()
        #self.cuber.solveCube()


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
