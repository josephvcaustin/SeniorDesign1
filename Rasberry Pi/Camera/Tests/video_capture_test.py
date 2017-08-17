from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time
import cv2

# initialize camera and grab ref
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
rawCapture= PiRGBArray(camera, size=(320, 240))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        image = cv2.threshold(image, 110, 240, cv2.THRESH_BINARY_INV)[1]
        #image = cv2.Canny(image, 20, 100)

        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        for c in cnts:
                #M = cv2.moments(c)
                #cX = int(M["m10"] / M["m00"])
                #cY = int(M["m01"] / M["m00"])
                
                cv2.drawContours(image, [c], -1,(0, 255, 0), 3)
                cv2.imshow("Frame", image)
                key = cv2.waitKey(1) & 0xFF
                rawCapture.truncate(0)

        if key == ord("q"):
                cv2.destroyAllWindows()
                break
