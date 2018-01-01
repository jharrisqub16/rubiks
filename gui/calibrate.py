#!/usr/bin/python3

import sys
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image
from PIL import ImageTk

def temp():
    print("Testing callback")


class Calibration(tk.Tk):
    def __init__(self, parent, parentSize):
        #super().__init__()
        tk.Toplevel.__init__(self)

        # Handler for closing event
        self.protocol("WM_DELETE_WINDOW", self.teardownWindow)

        self.parentWindow = parent

        self.title("TODO calibration window")

        # TODO This should probably be initialised to the size of the rpi screen
        # Also, should the window be adjustable by the user?
        #self.size_x = 500
        #self.size_y = 500
        self.windowSize = parentSize

        self.image = Image.open('images/todo.png')
        self.image = self.image.resize(self.windowSize, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(self, width=self.windowSize[0], height=self.windowSize[1])
        self.canvas.bind("<Button 1>", self.onClick)
        self.canvas.pack()
        self.canvas.create_image(self.windowSize[0]/2, self.windowSize[1]/2, image=self.image)

        self.spawnButtons()

    def onClick(self, event):
        # TODO This assumes that:
        #   - The image is presented as the full size of the canvas/window
        #   - The image is not scaled
        print(event.x, event.y)


    def spawnButtons(self):
        # Pack solve and scramble buttons into a frame (for placement)
        self.buttonFrame = tk.Frame(self)

        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.cancelCloseWindow)
        self.applyButton = tk.Button(self.buttonFrame, text="Apply", command=self.applyCloseWindow)
        self.cancelButton.pack(side=tk.LEFT)
        self.applyButton.pack(side=tk.LEFT)
        # Place packed frame into a window on the main canvas
        self.buttonWindow = self.canvas.create_window(self.windowSize[0], self.windowSize[1], anchor='se', window=self.buttonFrame)


    def cancelCloseWindow(self):
        # Prompt user, disgregard all changes and destroy window
        if (msg.askokcancel("Confirm", "Changes will be discarded. \n Continue?")):
            self.teardownWindow()


    def applyCloseWindow(self):
        # Store all configuration changes, then destroy configuration window
        # TODO Handle configuration changes
        print("Configuration overwritten")

        self.teardownWindow()


    def teardownWindow(self):
        self.destroy()
        # Tidy up state of parent object which restricts this window being spawned
        # TODO Does not really make sense to reset this here
        self.parentWindow.calibrationWindowSpawned = False
        self.parentWindow.calibrateButton['state'] = 'normal'
