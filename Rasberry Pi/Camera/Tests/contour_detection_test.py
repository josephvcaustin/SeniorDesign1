import imutils
import cv2
import numpy as np

#load image
image = cv2.imread("turn2.png")

#preprocess image
grayed_image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(grayed_image, (5, 5), 0)
threshold_image = cv2.threshold(blurred_image, 60, 255, cv2.THRESH_BINARY)[1]

#find contours of threshold_image
contours = cv2.findContours(threshold_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if imutils.is_cv2() else contours[1]

#convert back to BGR for contour drawing
threshold_image = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)

#loop over the countours contained in "contours"
for c in contours:

    #compute the center of the contours using contour "Moments"
    M = cv2.moments(c)
    centerX = int(M["m10"] / M["m00"])
    centerY = int(M["m01"] / M["m00"])

    #compute contour bounding rectangles
    boundRectCoor = cv2.boundingRect(c)
    rotatedBoundingRect = cv2.minAreaRect(c)
    rotatedBoundRectCoor = cv2.boxPoints(rotatedBoundingRect)
    rotatedBoundRectCoor = np.int0(rotatedBoundRectCoor)

    #compute and print signed contour area; negative-ccw, positive-cc
    contour_area = cv2.contourArea(c, True)
    print(contour_area)
    
    #draw the contours and their centers
    #draw the bounding box and their centers
    cv2.drawContours(threshold_image, [c], -1, (0, 255,0), 2)
    cv2.drawContours(threshold_image, [rotatedBoundRectCoor], 0, (0, 106, 255), 2)
    cv2.circle(threshold_image, (centerX, centerY), 7, (255, 0, 0), -1)
    cv2.circle(threshold_image, ((rotatedBoundRectCoor[1][0]+rotatedBoundRectCoor[3][0])/2, (rotatedBoundRectCoor[0][1]+rotatedBoundRectCoor[2][1])/2), 7, (255, 255, 0))
    cv2.rectangle(threshold_image, (boundRectCoor[0], boundRectCoor[1]),(boundRectCoor[0]+boundRectCoor[2],boundRectCoor[1]+boundRectCoor[3]), (0, 0, 255), 2)

    #show the image
    cv2.imshow("Processed image", threshold_image)
    cv2.waitKey(0)
