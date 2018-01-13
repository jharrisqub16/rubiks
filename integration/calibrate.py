import sys
import os
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image
from PIL import ImageTk

def temp():
    print("Testing callback")


class Calibration:
    def __init__(self, master, parent, parentSize):
        self.master = master
        self.parentWindow = parent

        self.cubr = self.parentWindow.cubr

        self.mainFrame = tk.Frame(self.master)

        # Handler for closing event
        self.master.protocol("WM_DELETE_WINDOW", self.teardownWindow)
        self.master.title("Configuration menu")

        # TODO This should probably be initialised to the size of the rpi screen
        # Also, should the window be adjustable by the user?
        #self.size_x = 500
        #self.size_y = 500
        self.windowSize = parentSize

        #TODO temporary hack until videostream implementation
        #cwd = os.path.dirname(__file__)
        #imagepath = os.path.join(cwd, 'images', 'todo.png')

        #self.image = Image.open(imagepath)
        #self.image = self.image.resize(self.windowSize, Image.ANTIALIAS)
        #self.image = ImageTk.PhotoImage(self.image)
        #TODO testing
        cvImage = self.cv.getImage()
        img = Image.fromarray(cvImage)
        self.image = ImageTk.PhotoImage(image=img)

        self.canvas = tk.Canvas(self.mainFrame, width=self.windowSize[0], height=self.windowSize[1])
        self.canvas.bind("<Button 1>", self.onClick)
        self.canvas.pack()
        self.canvasImage = self.canvas.create_image(self.windowSize[0]/2, self.windowSize[1]/2, image=self.image)

        self.mainFrame.pack()
        self.spawnWidgets()

        # TODO Add threading
        self.updateFrame()

    def updateFrame(self):
        cvImage = self.cv.getImage()

        if cvImage is not None:
            img = Image.fromarray(cvImage)
            cvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cvImage)
            self.image = ImageTk.PhotoImage(image=img)

            #lmain.imgtk = imgtk
            #lmain.configure(image=imgtk)
            # TODO Testing
            self.canvas.itemconfig(self.canvasImage, image = self.image)

        self.canvas.after(30, self.updateFrame)
        print("loop")

    def onClick(self, event):
        # TODO This assumes that:
        #   - The image is presented as the full size of the canvas/window
        #   - The image is not scaled
        print(event.x, event.y)


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
        self.applyRoiHighlighting = tk.BooleanVar()
        self.showRoiCheckbox = tk.Checkbutton(self.canvas, text="Highlight regions", variable=self.applyRoiHighlighting)
        self.canvas.create_window(0, self.windowSize[1], anchor='sw', window=self.showRoiCheckbox)

        self.nextViewButton = tk.Button(self.canvas, text="Next Camera View", command=self.nextCameraView)
        self.canvas.create_window(self.windowSize[0], self.windowSize[1]/2, window=self.nextViewButton)


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


    def nextCameraView():
        self.cubr.goToNextViewingPosition()

