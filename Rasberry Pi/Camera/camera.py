from picamera import PiCamera
from time import sleep
import cv2, imutils
from matplotlib import pyplot as plt

camera = PiCamera()
camera.resolution = (320, 240)
#camera.rotation = 180
camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/Senior Project/presentation_image1.jpg')
camera.stop_preview()
image = cv2.imread('/home/pi/Desktop/Senior Project/presentation_image1.jpg', 0)
cv2.imwrite('/home/pi/Desktop/Senior Project/presentation_grayscale.jpg', image)
image = cv2.GaussianBlur(image, (21, 21), 0)
cv2.imwrite('/home/pi/Desktop/Senior Project/presentation_blurred.jpg', image)
hist = cv2.calcHist([image], [0], None, [256], [0, 256])        #histogram calculation for dynamic thresholding
plt.plot(hist)
plt.xlim([0, 256])
plt.show()
savefig('/home/pi/Desktop/Senior Project/presentation_hist.jpg')
weight, mean, tot = 0, 0, 0                                     #calculate threshold using arithmetic mean
for idx, val in enumerate(hist):                                #
    weight += idx*val                                           #
    tot += val                                                  #
mean = weight/tot                                               #
image = cv2.threshold(image, mean+50, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('/home/pi/Desktop/Senior Project/presentation_threshold.jpg', image)
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
cv2.imwrite('/home/pi/Desktop/Senior Project/presentation_contours.jpg', image)

