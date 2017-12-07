# PROJECT:  Pill Sorter
# GROUP:    Nicola DaSilva, Natacha Barcala, Jacob Hazelbaker

import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Initialize servo GPIO control pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

angleMin = 5    # Position if Orange pill found
angleMax = 75   # Position if Orange pill not found
angleCurr = angleMax    # Initialized position



# Initialize the video camera
cam = cv2.VideoCapture(0)
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

# Orange color range - BGR format
lowerBound = np.array([0, 70, 170])
upperBound = np.array([75, 200, 255])



while True:
    ret, img = cam.read()
    img = cv2.resize(img, (340, 220))

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
        if (x != 0) and (y != 0) and (w != 0) and (h != 0):
            # found orange!
            orange = True
            print("ORANGE")
            # break out of the for loop and keep going
            break;
        else:
            print(" --- ")

    # If we found orange, move the servo
    if orange:
        print("Updating angle to open for orange pill to pass")
        angle = angleMin
        duty = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(duty)
        # Give pill time to pass through
        cv2.waitKey(1000)
        # Move servo back to default position
        angle = angleMax
        duty = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(duty)
        # Give the servo time to move back into place
        print("Closing servo gate again")
        cv2.waitKey(1000)

    cv2.imshow("maskClose", maskClose)
    cv2.imshow("maskOpen", maskOpen)
    cv2.imshow("mask", mask)
    cv2.imshow("cam", img)

    cv2.waitKey(10)