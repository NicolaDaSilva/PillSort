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
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    # morphology
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    conts = h

    ctr = np.array(conts).reshape((-1,1,2)).astype(np.int32)
    cv2.drawContours(img, [ctr], -1, (255, 0, 0), 3)
    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #cv2.putText(img, str(i + 1), (x, y + h), font, (0, 255, 255))
    cv2.imshow("maskClose", maskClose)
    cv2.imshow("maskOpen", maskOpen)
    cv2.imshow("mask", mask)
    cv2.imshow("cam", img)
    cv2.waitKey(10)