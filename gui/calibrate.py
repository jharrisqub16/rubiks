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
        self.protocol("WM_DELETE_WINDOW", self.eventWindowClose)

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

        # Create buttons
        self.cancelButton = tk.Button(self.canvas, text="Cancel")#, command=temp)
        self.cancelButtonWindow = self.canvas.create_window(self.windowSize[0], self.windowSize[1], anchor='se', window=self.cancelButton)

        self.applyButton = tk.Button(self.canvas, text="OK")#, command=temp)
        self.applyButtonWindow = self.canvas.create_window(0, 0, anchor='nw', window=self.applyButton)

    def onClick(self, event):
        # TODO This assumes that:
        #   - The image is presented as the full size of the canvas/window
        #   - The image is not scaled
        print(event.x, event.y)

    def eventWindowClose(self):
        self.destroy()
        #TODO Would make more sense if this is not handled here
        self.parentWindow.calibrationWindowSpawned = False
        self.parentWindow.calibrateButton['state'] = 'normal'
