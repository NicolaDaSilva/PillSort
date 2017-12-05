# PROJECT:  Pill Sorter
# GROUP:    Nicola DaSilva, Natacha Barcala, Jacob Hazelbaker

import cv2
import numpy as np

# Location to save the picture
file = "my_image.png"

# How mnay frames to skip while the camera first takes take to focus its lens
startDelay = 10

# For default camera, set to 0.  Will usually be the integrated laptop camera.
# For USB cameras, set to USB port number as shown in Device Manager
camPort = 0

# Creates an OpenCV object for using an attached camera
cam = cv2.VideoCapture(camPort)

# Takes a single picture and returns it using PILLOW (PIL) data format
def takePic():
    # "success" boolean variable will be "true" if it took a picture
    success, myPic = cam.read()
    return myPic  # Returns the image as PIL data


# Disregard the first few images since they will be super dark or super bright
for i in range(startDelay):
    temp = takePic()

print("Program Launched...")

#while (True):
# Takes a picture with the specified camera
camPic = takePic()

# Saves the image (camPic) in the specified path and name of "file"
cv2.imwrite(file, camPic)

# load the image
image = cv2.imread(file)

# define the list of boundaries
boundaries = [
    ([26, 90, 90], [46, 110, 110]),
    ([86, 31, 4], [220, 88, 50]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
]

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, camPic, mask = mask)

    # show the images
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)


# Release use of the web camera so that other programs may potentially use it
del (cam)