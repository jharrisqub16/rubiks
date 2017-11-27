#!/usr/bin/python3

import sys
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image
from PIL import ImageTk

if sys.version_info[0] != 3:
    print("This application requires python3+")
    sys.exit(1)


def temp():
    print("Testing callback")


class Cubr(tk.Tk):
    def __init__(self, image):
        super().__init__()

        #delf.image = tk.PhotoImage(file=image)
        self.title("CubeSolver GUI v1")

        # TODO This should probably be initialised to the size of the rpi screen
        # Also, should the window be adjustable by the user?
        self.size_x = 500
        self.size_y = 500
        self.window_size = 500,500

        self.image = Image.open(image)
        self.image = self.image.resize(self.window_size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(self, width=self.size_x, height=self.size_y)
        self.canvas.bind("<Button 1>", self.onClick)
        self.canvas.pack()
        self.canvas.create_image(self.size_x/2, self.size_y/2, image=self.image)

        #self.solve_button = tk.Button(text="Help")
        #self.solve_button.pack(fill=tk.X, padx=500)

        #self.buttonFrame = tk.Frame(self, height=500, width=32)
        #self.buttonFrame.pack()

        self.solveButton = tk.Button(self.canvas, text="Solve Button example", command=temp)

        solve_button_window = self.canvas.create_window(self.size_x, self.size_y, anchor='se', window=self.solveButton)
        #self.solveButton.pack()

    def onClick(self, event):
        # TODO This assumes that:
        #   - The image is presented as the full size of the canvas/window
        #   - The image is not scaled
        print("clicked")
        print(event.x, event.y)
        msg.showinfo("Information","something something")

if __name__ == "__main__":
    cubr = Cubr("images/rubiks.png")
    cubr.mainloop()
