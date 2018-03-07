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

        self.Cuber = self.parentWindow.cuber

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

        self.colourNames = {    'Y': 'Yellow',
                                'B': 'Blue',
                                'O': 'Orange',
                                'G': 'Green',
                                'W': 'White',
                                'R': 'Red'}

        self.targetColoursRgbValues = self.cubr.getColourCorrelationValues()

        self.colourCalibrationActive = False
        self.colourCalibrationLastSelection = None
        self.colourCalibrationNewSelection = tk.StringVar()

        cvImage = self.cuber.getImage()
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
        self.cuber.setRoiHighlighting(False)
        self.cuber.setContourHighlighting(False)
        self.cuber.setColourConstancy(False)


    def updateFrame(self):
        cvImage = self.cuber.getImage()

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

        clickCoords = (event.x, event.y)

        if (self.colourCalibrationActive is True and self.colourCalibrationLastSelection is not None):
            print('colour calibration: colour: {}'.format(self.colourCalibrationLastSelection))

            self.cuber.calibrateColourHandler(self.colourCalibrationLastSelection, clickCoords)

            # Pull new colours from cv
            self.targetColoursRgbValues = self.cuber.getColourCorrelationValues()
            # Apply new colours to buttons
            self.updateColourCalibrationButtonColours()
        elif (self.highlightRoiBool.get() is True):
            # Only allow shifting of ROIs when their highlighting is active
            self.cuber.roiDragSet(clickCoords)


    def canvasMotionEventHandler(self, event):
        if (self.highlightRoiBool.get() is True):
            tempCoords = (event.x, event.y)
            self.cuber.roiDrag(tempCoords)


    def canvasReleaseEventHandler(self, event):
        if (self.highlightRoiBool.get() is True):
            self.cuber.roiDragEnd()


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


        # Create colour calibration buttons
        self.colourButtonsFrame = tk.Frame(self.sidebarFrame, borderwidth=2, relief = tk.RAISED)
        self.colourCalibrationButtons = []
        for index, colour in enumerate(self.targetColoursRgbValues):
            # Form hex code colour from RGB values
            tempColour = '#%02x%02x%02x' % (self.targetColoursRgbValues[colour][0], self.targetColoursRgbValues[colour][1], self.targetColoursRgbValues[colour][2])
            tempButton = tk.Radiobutton(self.colourButtonsFrame, text=self.colourNames[colour], indicatoron=False, bg=tempColour, selectcolor=tempColour, var=self.colourCalibrationNewSelection, value=colour, command=self.colourCalibrationHandler)
            self.colourCalibrationButtons.append(tempButton)

            self.colourCalibrationButtons[index].pack(anchor='nw', fill=tk.X)

        self.colourButtonsFrame.pack(side=tk.TOP, anchor='w', fill=tk.X)


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


    def updateColourCalibrationButtonColours(self):
        for index, colour in enumerate(self.targetColoursRgbValues):
            tempColour = '#%02x%02x%02x' % (self.targetColoursRgbValues[colour][0], self.targetColoursRgbValues[colour][1], self.targetColoursRgbValues[colour][2])

            self.colourCalibrationButtons[index].config(bg=tempColour, selectcolor=tempColour)


    def cancelCloseWindow(self):
        # Prompt user, disgregard all changes and destroy window
        if (msg.askokcancel("Confirm", "Changes will be discarded. \n Continue?")):
            # Call to reset discard all changes that were made in the solver:
            self.cuber.discardStateChanges()
            # Destroy the window
            self.teardownWindow()


    def applyCloseWindow(self):
        # Store all configuration changes, then destroy configuration window
        # TODO Handle configuration changes
        print("Configuration overwritten")
        self.cuber.saveState()

        self.teardownWindow()


    def teardownWindow(self):
        # Tidy up state of parent object which restricts this window being spawned
        self.parentWindow.calibrationWindowSpawned = False
        self.parentWindow.calibrateButton['state'] = 'normal'

        # Destroy calibration window
        self.master.destroy()


    def nextCameraView(self):
        self.cuber.goToNextViewingPosition()


    def highlightRoiHandler(self):
        # get tkinter bool state into temporary 'normal' bool:
        tempBool = self.highlightRoiBool.get()
        print("Roi Highlighting state toggled to {0}.".format(tempBool))

        # call API function to update
        self.cuber.setRoiHighlighting(tempBool)


    def highlightContoursHandler(self):
        tempBool = self.highlightContoursBool.get()
        print("Contour Highlighting state toggled to {0}.".format(tempBool))

        # Call API update function
        self.cuber.setContourHighlighting(tempBool)


    def applyColourConstancyHandler(self):
        tempBool = self.applyColourConstancyBool.get()
        print("Colour Constancy state toggled to {0}.".format(tempBool))

        # Call API update function
        self.cuber.setColourConstancy(tempBool)


    def colourCalibrationHandler(self):
        tempNewButtonValue = self.colourCalibrationNewSelection.get()

        if (tempNewButtonValue == self.colourCalibrationLastSelection):
            self.colourCalibrationActive = False
            self.colourCalibrationLastSelection = None
            for button in self.colourCalibrationButtons:
                # Deactivate all buttons
                button.deselect()
        else:
            self.colourCalibrationActive = True
            self.colourCalibrationLastSelection = tempNewButtonValue
