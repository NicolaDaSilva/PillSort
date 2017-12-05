# PROJECT:  Pill Sorter
# GROUP:    Nicola DaSilva, Natacha Barcala, Jacob Hazelbaker

import cv2
import numpy as np

# orange
lowerBound = np.array([0, 70, 170])
upperBound = np.array([75, 200, 255])

cam = cv2.VideoCapture(0)
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

font = (cv2.FONT_HERSHEY_SIMPLEX, 2, 0.5, 0, 3, 1)

while True:
    ret, img = cam.read()
    img = cv2.resize(img, (340, 220))

    # convert BGR to HSV
    # imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(img, lowerBound, upperBound)
    # morphology
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    conts = h

    ctr = np.array(conts).reshape((-1,1,2)).astype(np.int32)
    cv2.drawContours(img, [ctr], -1, (255, 0, 0), 3)

    # assume we have not found orange yet
    orange = False

    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i])
        # print(x, y, w, h)
        temp = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # The values for y, w, and h changes when a rectangle is created when it 
        # finds an orange object
        if (x == 0) and (y != 0) and (w != 0) and (h != 0):
            # found orange!
            orange = True
            print("ORANGE")
            # break out of the for loop and keep going
            break;
        else:
            print(" --- ")

    cv2.imshow("maskClose", maskClose)
    cv2.imshow("maskOpen", maskOpen)
    cv2.imshow("mask", mask)
    cv2.imshow("cam", img)

    # If we found orange, move the servo
    if orange:
        print("do stuff here")
        break;

    cv2.waitKey(10)
