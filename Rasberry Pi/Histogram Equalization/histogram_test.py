from picamera import PiCamera
from time import sleep
from scipy import stats
import imutils
import cv2
import numpy as np
import time

#load image
image = cv2.imread("test_image.jpg", 0)

hist = cv2.calcHist([image], [0], None, [256], [0, 256])
#print(hist)
print("start")
weight = 0
tot=0
for idx, val in enumerate(hist):
    #print(idx, val)
    weight = weight+(idx * val)
    tot = tot+val
    #print(weight)

mean = weight/tot
print(mean)

image_1 = cv2.threshold(image, mean, 240, cv2.THRESH_BINARY)[1]
cv2.imshow("frame", image_1)
cv2.waitKey(0)
#histMed = np.mean(hist)
#print(histMed)
