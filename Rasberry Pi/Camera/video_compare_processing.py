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
        cv2.imshow("Frame", image)
        
        image_1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_1 = cv2.GaussianBlur(image_1, (5, 5), 0)
        image_1 = cv2.threshold(image_1, 110, 240, cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(image_1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]    

        for c in cnts:
                cv2.drawContours(image_1,[c], -1, (122, 255, 0), 2)
                cv2.imshow("Frame2", image_1)
                
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        if key == ord("q"):
                cv2.destroyAllWindows()
                break
