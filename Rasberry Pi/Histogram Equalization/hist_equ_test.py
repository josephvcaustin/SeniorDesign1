from scipy import stats
import imutils
import cv2
import numpy as np

from scipy.signal import argrelextrema
from scipy import signal
from scipy.interpolate import interp1d


#load image
image = cv2.imread("test_image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#image = cv2.GaussianBlur(image, (15, 15), 0)

hist = cv2.calcHist([image], [0], None, [256], [0, 256])
print(hist.flatten())
hist_mean = np.convolve(hist.flatten(), np.ones((256,))/256)[255:]
print(hist_mean)
#idx = find_peaks_cwt(hist_mean, np.arange(1, 20,1))
#idx = argrelextrema(hist_mean, np.greater)

prevdiff = hist_mean[1] - hist_mean[0]
i = 2
while i < len(hist_mean)-1:
    i+=1
    diff = hist_mean[i] - hist_mean[i-1]
    if diff > 0 and prevdiff < 0:
        print("Critical dec -> inc at %d" % i)
    elif diff < 0 and prevdiff > 0:
        print("Critical inc -> dec at %d" % i)
        
#thresh = np.mean(idx)
#print(thresh)

#image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
#cv2.imshow("frame", image)
#cv2.waitKey(0)
