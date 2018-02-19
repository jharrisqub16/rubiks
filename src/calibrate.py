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
        self.master.protocol("WM_DELETE_WINDOW", self.cancelCloseWindow)
        self.master.title("Configuration menu")

        #self.windowSize = parentSize
        # TODO accomodate scaling and ensure image is full size of canvas (for coordinates)
        self.windowSize = (320, 240)

        # Create the tk variables for widgets to interact with
        self.highlightRoiBool = tk.BooleanVar()
        self.highlightContoursBool = tk.BooleanVar()
        self.applyColourConstancyBool = tk.BooleanVar()

        cvImage = self.cubr.getImage()
        img = Image.fromarray(cvImage)
        self.image = ImageTk.PhotoImage(image=img)

        self.canvas = tk.Canvas(self.mainFrame, width=self.windowSize[0], height=self.windowSize[1])
        self.canvas.bind("<ButtonPress-1>", self.canvasClickEventHandler)
        self.canvas.bind("<ButtonRelease-1>", self.canvasReleaseEventHandler)
        self.canvas.bind("<B1-Motion>", self.canvasMotionEventHandler)
        self.canvasImage = self.canvas.create_image(self.windowSize[0]/2, self.windowSize[1]/2, image=self.image)
        self.canvas.pack(side=tk.LEFT)

        self.spawnWidgets()
        self.mainFrame.pack(side=tk.LEFT)

        self.updateFrame()

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

        tempCoords = (event.x, event.y)
        print(tempCoords)
        # TODO no colour calibration is active

        if (self.highlightRoiBool.get() is True):
            # Only allow shifting of ROIs when their highlighting is active
            self.cubr.roiDragSet(tempCoords)
        elif (False):
            pass
            # self.cubr.calibrateColourHandler(activeColourSelection, (event.x, event.y))


    def canvasMotionEventHandler(self, event):
        if (self.highlightRoiBool.get() is True):
            tempCoords = (event.x, event.y)
            self.cubr.roiDrag(tempCoords)


    def canvasReleaseEventHandler(self, event):
        if (self.highlightRoiBool.get() is True):
            self.cubr.roiDragEnd()


    def spawnWidgets(self):
        # Sidebar to contain all other widgets
        self.sidebarFrame = tk.Frame(self.mainFrame)

        # Create checkboxes on sidebar
        self.checkboxFrame = tk.Frame(self.sidebarFrame, borderwidth=2, relief=tk.RAISED)

        self.highlightRoiCheckbox = tk.Checkbutton(self.checkboxFrame, text="Highlight regions", command=self.highlightRoiHandler, variable=self.highlightRoiBool)
        self.highlightRoiCheckbox.grid(row=0, column=0, sticky=tk.W)

        self.highlightContoursCheckbox = tk.Checkbutton(self.checkboxFrame, text="Highlight contours", command=self.highlightContoursHandler, variable=self.highlightContoursBool)
        self.highlightContoursCheckbox.grid(row=1, column=0, sticky=tk.W)

        self.applyColourConstancyCheckbox = tk.Checkbutton(self.checkboxFrame, text="Show Colour Constancy", command=self.applyColourConstancyHandler, variable=self.applyColourConstancyBool)
        self.applyColourConstancyCheckbox.grid(row=2, column=0, sticky=tk.W)
        # Pack checkboxes into their parent container (to determine their relative positioning)
        self.checkboxFrame.pack()

        # Create Apply and Cancel buttons (packed into their own frame for placement)
        self.buttonFrame = tk.Frame(self.sidebarFrame)
        # Create button widgets
        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.cancelCloseWindow)
        self.applyButton = tk.Button(self.buttonFrame, text="Apply", command=self.applyCloseWindow)
        # Pack buttons into their parent in order
        self.cancelButton.pack(side=tk.LEFT)
        self.applyButton.pack(side=tk.LEFT)
        # Pack the button parent container into the sidebar
        self.buttonFrame.pack(side=tk.BOTTOM)

        self.sidebarFrame.pack(side=tk.LEFT, fill=tk.Y)

        # Make the 'next view' button in the top right corner, on top of the image/canvas
        self.nextViewButton = tk.Button(self.mainFrame, text="Next View", command=self.nextCameraView)
        self.canvas.create_window(0, 0, anchor='nw', window=self.nextViewButton)


    def cancelCloseWindow(self):
        # Prompt user, disgregard all changes and destroy window
        if (msg.askokcancel("Confirm", "Changes will be discarded. \n Continue?")):
            # Call to reset discard all changes that were made in the solver:
            self.cubr.discardStateChanges()
            # Destroy the window
            self.teardownWindow()


    def applyCloseWindow(self):
        # Store all configuration changes, then destroy configuration window
        # TODO Handle configuration changes
        print("Configuration overwritten")
        self.cubr.saveState()

        self.teardownWindow()


    def teardownWindow(self):
        # Tidy up state of parent object which restricts this window being spawned
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
