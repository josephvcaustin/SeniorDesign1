# import the necessary packages
from __future__ import print_function
from PiVideoStream import PiVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import imutils
import time
import cv2

# created a *threaded *video stream, allow the camera sensor to warmup
vs = PiVideoStream().start()
time.sleep(0.5)

while True:
    frame = vs.read()
    
    #preprocess image
    grayed_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(grayed_image, (21, 21), 0)
    
    #autothreshold using histogram
    equalized_image = cv2.equalizeHist(blurred_image, 50)
    hist = cv2.calcHist([equalized_image], [0], None, [256], [0, 256])
    weight = 0
    tot=0
    for idx, val in enumerate(hist):
        weight = weight+(idx * val)
        tot = tot+val
    mean = weight/tot
    threshold_image = cv2.threshold(equalized_image, mean, 255, cv2.THRESH_BINARY_INV)[1]
    
    #find contours of threshold_image
    contours = cv2.findContours(threshold_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    #convert back to BGR color space
    threshold_image = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)
    blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_GRAY2BGR)
    equalized_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)
    contour_image = threshold_image.copy()

    #draw contours and their centers
    for c in contours:

        #compute the center of the contours using contour "Moments"
        M = cv2.moments(c)
        if M["m00"] != 0:
            centerX = int(M["m10"] / M["m00"])
            centerY = int(M["m01"] / M["m00"])
        else:
            centerX, centerY = 0, 0
            
        #draw
        contour_image = cv2.drawContours(contour_image, [c], -1, (0, 255,0), -1)
        cv2.circle(contour_image, (centerX, centerY), 7, (255, 0, 255), -1)

    #show images on screen
    stacked_images = np.hstack((frame, blurred_image, equalized_image, threshold_image, contour_image))
    cv2.imshow("All Steps", stacked_images)
    key = cv2.waitKey(1)
