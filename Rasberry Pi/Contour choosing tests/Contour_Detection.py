from PiVideoStream import PiVideoStream
import numpy as np
import imutils, time, cv2

def preprocessImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                 #grayscale
    image = cv2.GaussianBlur(image, (11, 11), 0)                    #blur
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])        #histogram calculation for dynamic thresholding
    weight, mean, tot = 0, 0, 0                                     #calculate threshold using arithmetic mean
    for idx, val in enumerate(hist):                                #
        weight += idx*val                                           #
        tot += val                                                  #
    mean = weight/tot                                               #
    image = cv2.threshold(image, mean+50, 255, cv2.THRESH_BINARY)[1]
    return image

def detectContours(image):
    contours = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]     #no clue what this does
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)                 #convert back to BGR color for contour drawing only
    bigContour = 0
    bigContourSize = 0
    for ind, c in enumerate(contours):                                              #calculate "center of gravity" of contour
        contourArea = cv2.contourArea(c, True)
        #print(contourArea)
        if abs(contourArea) > bigContourSize:
            bigContour = ind
            bigContourSize = abs(contourArea)
    if len(contours) != 0:
        moments = cv2.moments(contours[bigContour])                                    #calculate image moments
        if moments["m00"] != 0:                                     #handle case where moment = 0
            centerX = int(moments["m10"] / moments["m00"])          #set x coor
            centerY = int(moments["m01"] / moments["m00"])          #set y coor
        else:
            centerX, centerY = 0, 0
        rotatedBoundingRect = cv2.minAreaRect(contours[bigContour])
#        print(rotatedBoundingRect[2])
        rotatedBoundRectCoor = cv2.boxPoints(rotatedBoundingRect)
        rotatedBoundRectCoor = np.int0(rotatedBoundRectCoor)
        #draw contours and centers to image
        cv2.drawContours(image, [rotatedBoundRectCoor], 0, (0, 106, 255), 2)
        cv2.drawContours(image, contours, bigContour, (128, 0, 128), -1)
        cv2.circle(image, (centerX, centerY), 4, (255, 255, 255), -1)

        return image
#create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start()
time.sleep(0.5)

while True:                                            
    image = preprocessImage(vs.read())
    image = detectContours(image)
    #find contours and their centers
    

    #show image on screen
    cv2.imshow("Processed Image", image)
    cv2.waitKey(1)

   #threshold
