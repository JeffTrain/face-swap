from tkinter import Label, filedialog, Tk, Button

import numpy as np
from PIL import ImageTk, Image
from PIL.Image import Resampling

from face_swaps.face_detect import face_marked, face_marked2
from face_swaps.face_swap import readLandmarkPoints, connectLandmarkPoints, showLandmarkPoints


def open_img():
    # Select the Imagename  from a folder
    x = openfilename()

    # opens the image
    img = Image.open(x)

    converted_img = np.array(img)
    showLandmarkPoints(converted_img)
    face_marked_img = face_marked2(converted_img)

    img = Image.fromarray(np.uint8(face_marked_img)).convert('RGB')

    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 250), Resampling.LANCZOS)

    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)

    # create a label
    panel = Label(root, image=img)

    # set the image as img
    panel.image = img
    panel.grid(row=2)


def openfilename():
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title='"pen')
    return filename


# Create a window
root = Tk()

# Set Title as Image Loader
root.title("Image Loader")

# Set the resolution of window
root.geometry("550x300+300+150")

# Allow Window to be resizable
root.resizable(width=True, height=True)

# Create a button and place it into the window using grid layout
Button(root, text='open image', command=open_img).grid(row=1, columnspan=4)
root.mainloop()