import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image
from PIL import ImageTk


class Calibration:
    def __init__(self, master, parent, parentSize):
        self.master = master
        self.parentWindow = parent

        self.cubr = self.parentWindow.cubr

        self.mainFrame = tk.Frame(self.master)

        # Handler for closing event
        self.master.protocol("WM_DELETE_WINDOW", self.teardownWindow)
        self.master.title("Configuration menu")

        #self.windowSize = parentSize
        # TODO Size according to the image and account for scaling
        # TODO How can it be assured that image is the full size of the canvas
        #self.windowSize = (480, 360)
        self.windowSize = (320, 240)

        cvImage = self.cubr.getImage()
        img = Image.fromarray(cvImage)
        self.image = ImageTk.PhotoImage(image=img)

        self.canvas = tk.Canvas(self.mainFrame, width=self.windowSize[0], height=self.windowSize[1])
        self.canvas.bind("<Button 1>", self.canvasClickEventHandler)
        self.canvas.pack()
        self.canvasImage = self.canvas.create_image(self.windowSize[0]/2, self.windowSize[1]/2, image=self.image)

        self.mainFrame.pack()
        self.spawnWidgets()

        # TODO threading
        #self.updateFrame()
        stopEvent = threading.Event()
        thread = threading.Thread(target=self.updateFrame, args=())
        thread.start()

        # Always start calibration window with visual debug disabled:
        # This also prevents the GUI and cv getting out of sync
        self.cubr.setRoiHighlighting(False)
        self.cubr.setContourHighlighting(False)
        self.cubr.setColourConstancy(False)

    def updateFrame(self):
        cvImage = self.cubr.getImage()

        if cvImage is not None:
            # Convert image to TkInter format
            img = Image.fromarray(cvImage)
            self.image = ImageTk.PhotoImage(image=img)

            # Update image on canvas
            self.canvas.itemconfig(self.canvasImage, image = self.image)

        # Configure next update call
        self.canvas.after(50, self.updateFrame)


    def canvasClickEventHandler(self, event):
        # TODO This assumes that:
        #   - The image is presented as the full size of the canvas/window
        #   - The image is not scaled
        print(event.x, event.y)
        # TODO no colour calibration is active
        # if we are currently handling roi shifts:
        self.cubr.roiShiftHandler((event.x, event.y))


    def spawnWidgets(self):
        # Pack solve and scramble buttons into a frame (for placement)
        self.buttonFrame = tk.Frame(self.mainFrame)

        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.cancelCloseWindow)
        self.applyButton = tk.Button(self.buttonFrame, text="Apply", command=self.applyCloseWindow)
        self.cancelButton.pack(side=tk.LEFT)
        self.applyButton.pack(side=tk.LEFT)
        # Place packed frame into a window on the main canvas
        self.canvas.create_window(self.windowSize[0], self.windowSize[1], anchor='se', window=self.buttonFrame)

        # TODO this should be used later for the calibration video stream
        self.checkboxFrame = tk.Frame(self.mainFrame)

        self.highlightRoiBool = tk.BooleanVar()
        self.highlightRoiCheckbox = tk.Checkbutton(self.checkboxFrame, text="Highlight regions", command=self.highlightRoiHandler, variable=self.highlightRoiBool)
        self.highlightRoiCheckbox.grid(row=0, column=0, sticky=tk.W)

        self.highlightContoursBool = tk.BooleanVar()
        self.highlightContoursCheckbox = tk.Checkbutton(self.checkboxFrame, text="Highlight contours", command=self.highlightContoursHandler, variable=self.highlightContoursBool)
        self.highlightContoursCheckbox.grid(row=1, column=0, sticky=tk.W)

        self.applyColourConstancyBool = tk.BooleanVar()
        self.applyColourConstancyCheckbox = tk.Checkbutton(self.checkboxFrame, text="Apply Colour Constancy", command=self.applyColourConstancyHandler, variable=self.applyColourConstancyBool)
        self.applyColourConstancyCheckbox.grid(row=2, column=0, sticky=tk.W)

        self.canvas.create_window(0, self.windowSize[1], anchor='sw', window=self.checkboxFrame)

        # TODO Add buttons to apply largest contour highlighting (instead of showing ROIs)
        # TODO Add button to apply Colour constancy algorithm to images

        self.nextViewButton = tk.Button(self.mainFrame, text="Next Camera View", command=self.nextCameraView)
        #self.canvas.create_window(self.windowSize[0]/2, self.windowSize[1], anchor='s', window=self.nextViewButton)
        self.canvas.create_window(0, 0, anchor='nw', window=self.nextViewButton)



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
        # Tidy up state of parent object which restricts this window being spawned
        # TODO Does not really make sense to reset this here
        self.parentWindow.calibrationWindowSpawned = False
        self.parentWindow.calibrateButton['state'] = 'normal'

        # Destroy calibration window
        self.master.destroy()


    def nextCameraView(self):
        self.cubr.goToNextViewingPosition()


    def highlightRoiHandler(self):
        # get tkinter bool state into temporary 'normal' bool:
        tempBool = self.highlightRoiBool.get()
        print("Roi Highlighting state toggled to {0}.".format(tempBool))

        # call API function to update
        self.cubr.setRoiHighlighting(tempBool)


    def highlightContoursHandler(self):
        tempBool = self.highlightContoursBool.get()
        print("Contour Highlighting state toggled to {0}.".format(tempBool))

        # Call API update function
        self.cubr.setContourHighlighting(tempBool)

    def applyColourConstancyHandler(self):
        tempBool = self.applyColourConstancyBool.get()
        print("Colour Constancy state toggled to {0}.".format(tempBool))

        # Call API update function
        self.cubr.setColourConstancy(tempBool)
