import threading
import time
import numpy as np
import cv2
import Tkinter as tk
#import Image, ImageTk
from PIL import Image
from PIL import ImageTk

#cameraIndexes = [0,1,2]
cameraIndexes = [2,1,0]

cameraObjects = []
for camera in cameraIndexes:
    print(cameraIndexes[camera])
    
    cameraObjects.append(cv2.VideoCapture(cameraIndexes[camera]))

for camera in cameraIndexes:
    if cameraObjects[camera].isOpened() == True:
        print("Openend")

        cameraObjects[camera].set(3, 320)
        cameraObjects[camera].set(4, 240)
    else:
        print("FAILED")

cameraNumber = 0
def nextImage():
    global cameraNumber
    
    if cameraNumber == (len(cameraObjects) -1):
        cameraNumber = 0
    else:
        cameraNumber += 1
        

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
#lmain.grid(row=0, column=0)
lmain.pack()

secondLabel = tk.Label(imageFrame)
secondLabel.pack()

button = tk.Button(imageFrame, text="Testing", command=nextImage)
button.pack()


def show_frame():
    #_, frame = cap.read()
    _, frame = cameraObjects[cameraNumber].read()
    #frame = cv2.flip(frame, 1)
    print(frame.shape[:2])

    #####################################################      
    ## First Label
    #####################################################      
    channels = []
    convertedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    channels = cv2.split(convertedImage)
    channels[1] = cv2.equalizeHist(channels[1])
    equalizedImage = cv2.merge(channels)

    cv2image = cv2.cvtColor(equalizedImage, cv2.COLOR_HSV2RGB)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)

    #####################################################      
    ## Second label
    #####################################################      
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img2 = Image.fromarray(cv2image)
    imgtk2 = ImageTk.PhotoImage(image=img2)
    secondLabel.imgtk = imgtk2
    secondLabel.configure(image=imgtk2)


    # Set loop callback
    lmain.after(30, show_frame) 

stopEvent = threading.Event()
thread = threading.Thread(target=show_frame, args=())
thread.start()
#show_frame()  #Display 2

window.mainloop()  #Starts GUI
