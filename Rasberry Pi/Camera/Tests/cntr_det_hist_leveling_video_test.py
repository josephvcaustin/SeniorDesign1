from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import cv2
import numpy as np
import time
from scipy.signal import find_peaks_cwt

#load image
#image = cv2.imread("turn.png")
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
rawCapture= PiRGBArray(camera, size=(320, 240))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array

        #preprocess image
        grayed_image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(grayed_image, (5, 5), 0)
        
        #autothreshold using histogram
        
        hist = cv2.calcHist([blurred_image], [0], None, [256], [0, 256])
        hist_mean = np.convolve(hist.flatten(), np.ones((256,))/256)[255:]
        idx = find_peaks_cwt(hist_mean, np.arange(1, 20,1))
        thresh = np.mean(idx)
        
##        weight = 0
##        tot=0
##        for idx, val in enumerate(hist):
##            weight = weight+(idx * val)
##            tot = tot+val
##        mean = weight/tot
        threshold_image = cv2.threshold(blurred_image, thresh, 255, cv2.THRESH_BINARY_INV)[1]
            
        #find contours of threshold_image
        contours = cv2.findContours(threshold_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]

        #convert back to BGR for contour drawing
#        threshold_image = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)

        #loop over the countours contained in "contours"
        for c in contours:

            #compute the center of the contours using contour "Moments"
            M = cv2.moments(c)
            if M["m00"] != 0:
                centerX = int(M["m10"] / M["m00"])
                centerY = int(M["m01"] / M["m00"])
            else:
                centerX, centerY = 0, 0

            #compute contour bounding rectangles
            #boundRectCoor = cv2.boundingRect(c)
#            rotatedBoundingRect = cv2.minAreaRect(c)
#            rotatedBoundRectCoor = cv2.boxPoints(rotatedBoundingRect)
#            rotatedBoundRectCoor = np.int0(rotatedBoundRectCoor)

            #compute and print signed contour area; negative-ccw, positive-cc
            contour_area = cv2.contourArea(c, True)
            #print(contour_area)

            #draw the contours and their centers
            #draw the bounding box and their centers
#            cv2.drawContours(threshold_image, [c], -1, (0, 255,0), 2)
#            cv2.drawContours(threshold_image, [rotatedBoundRectCoor], 0, (0, 106, 255), 2)
#            cv2.circle(threshold_image, (centerX, centerY), 7, (255, 0, 0), -1)
#            cv2.circle(threshold_image, ((rotatedBoundRectCoor[1][0]+rotatedBoundRectCoor[3][0])/2, (rotatedBoundRectCoor[0][1]+rotatedBoundRectCoor[2][1])/2), 7, (255, 255, 0))
            #cv2.rectangle(threshold_image, (boundRectCoor[0], boundRectCoor[1]),(boundRectCoor[0]+boundRectCoor[2],boundRectCoor[1]+boundRectCoor[3]), (0, 0, 255), 2)

            #show the image
            cv2.imshow("Processed image", threshold_image)
            cv2.waitKey(1)&0xFF
            rawCapture.truncate(0)
