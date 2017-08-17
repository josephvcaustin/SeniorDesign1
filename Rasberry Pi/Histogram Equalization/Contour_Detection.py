from PiVideoStream import PiVideoStream
from scipy.signal import argrelextrema
from matplotlib import pyplot as plt
import numpy as np
import imutils, time, cv2

#create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start()
time.sleep(0.5)

while True:
    #grab and show image 
    image = vs.read()                                               
    #cv2.imshow("Unprocessed Image", image)
    
    #preprocess image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                 #grayscale
    image = cv2.GaussianBlur(image, (21, 21), 0)                    #blur
    #cv2.imshow("Unprocessed Image1", image)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])        #histogram calculation for dynamic thresholding

    gray = np.mean(argrelextrema(hist, np.less)[0])
    image = cv2.threshold(image, gray, 255, cv2.THRESH_BINARY)[1]   #threshold
    #plt.pause(0.01)
    #plt.ion()
    #plt.figure()
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()
    
    #find contours and their centers
    contours = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]     #no clue what this does
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)                 #convert back to BGR color for contour drawing only
    for c in contours:                                              #calculate "center of gravity" of contour
        moments = cv2.moments(c)                                    #calculate image moments
        if moments["m00"] != 0:                                     #handle case where moment = 0
            centerX = int(moments["m10"] / moments["m00"])          #set x coor
            centerY = int(moments["m01"] / moments["m00"])          #set y coor
        else:
            centerX, centerY = 0, 0

        #draw contours and centers to image
        cv2.drawContours(image, [c], -1, (128, 0, 128), -1)
        cv2.circle(image, (centerX, centerY), 4, (255, 255, 255), -1)

    #show image on screen
    #cv2.imshow("Processed Image", image)
    cv2.waitKey(1)
    
