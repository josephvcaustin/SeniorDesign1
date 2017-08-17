from matplotlib import pyplot as plt
import cv2
import numpy as np
from scipy.signal import argrelextrema

image = cv2.imread("test_imag.jpg", 0)
image = cv2.GaussianBlur(image, (43, 43), 0)
#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist([image], [0], None, [128], [0, 256])
print(hist)

#hist = np.convolve(hist.flatten(), np.ones((256,))/256)[255:]
hist_max = np.amax(hist)

weight, mean, tot = 0, 0, 0                                     #calculate threshold using arithmetic mean
for idx, val in enumerate(hist):                                #
    if val < hist_max/20:
        hist[idx] = 0
k = 0
lowerThresh = 0
upperThresh = 255
humpStart = 0
humpMid = 0
humpEnd = 255 # end of the first big lump

flat = hist.flatten()
##while i < len(flat)-1:
##    if flat[i] == 0 and flat[i+1] != 0:
##        print("Transition at %d" %i)
##        lowerTransition = i
##    elif flat[i] != 0 and flat[i+1] == 0:
##        upperTransition = i
##    i+=1    

##while k < len(flat)-1:
##    if flat[k+1] > flat[k]:
##        humpStart = k
##        print("Hump start %d" %k)
##        break
##    k+=1
##
##while k < len(flat)-1:
##    if flat[k+1] < flat[k]:
##        humpMid = k
##        print("Hump middle %d" %k)
##        break
##    k+=1
##
##while k < len(flat)-1:
##    if flat[k+1] == 0:
##        humpEnd = k
##        print("Hump end %d" %k)
##        break
##    k+=1    

#Threshold 
##for j in range(1000):
##    for i in range(1919):
##        if image[j][i] < humpMid or image[j][i] > humpEnd:
##            image[j][i] = 0
##        else:
##            image[j][i] = 255
#cv2.imwrite("test_image.jpg", image)


#idx = argrelextrema(hist, np.greater)
#print(idx)
#gray = np.mean(idx[0])
#print(gray)
#image = cv2.threshold(image, transition-1, 255, cv2.THRESH_BINARY)[1]   #threshold
#mage = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, -10)


plt.figure()
plt.ion()
plt.plot(hist, 'go')
#plt.xlim([0, 256])
plt.show()
cv2.imshow("frame", cv2.resize(image, (960, 540)))
cv2.waitKey(0)
