from PiVideoStream import PiVideoStream
import numpy as np
import imutils, time, cv2

def main():
    vs = PiVideoStream().start()
    time.sleep(0.5)

    while True:                                            
        image = preprocessImage(vs.read())
        contours = detectContours(image)
        if len(contours) != 0:
            bigContour = findBigContour(contours)
            centerX, centerY = 0, 0#findContourCenter(contours, bigContour)
            image = drawContours(contours, bigContour, centerX, centerY, image)
        cv2.imwrite('/home/pi/Desktop/Senior Project/presentation_thickest.jpg', image)
        cv2.imshow("Processed Image", image)
        cv2.waitKey(1)
        
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
    return contours

def findBigContour(contours):
    bigContour = 0
    bigContourSize = 0
    for ind, c in enumerate(contours):                                              #calculate "center of gravity" of contour
        contourArea = cv2.contourArea(c, False)
        if abs(contourArea) > bigContourSize:
            bigContour = ind
            bigContourSize = contourArea
    return bigContour

def findContourCenter(contours, bigContour):
    moments = cv2.moments(contours[bigContour])                                    #calculate image moments
    if moments["m00"] != 0:                                     #handle case where moment = 0
        centerX = int(moments["m10"] / moments["m00"])          #set x coor
        centerY = int(moments["m01"] / moments["m00"])          #set y coor
    else:
        centerX, centerY = 0, 0
    return centerX, centerY

def drawContours(contours, bigContour, centerX, centerY, image):
    cv2.drawContours(image, contours, bigContour, (128, 0, 128), -1)
    bC = cv2.boundingRect(contours[bigContour])
    xDots = np.zeros(bC[2])
    yDots = np.zeros(bC[3])
    for x in range(bC[2]/4):
        for y in range(bC[3]/4):
            if cv2.pointPolygonTest(contours[bigContour], (bC[0]+(4*x), bC[1]+(4*y)), measureDist=False) == 1:
                xDots[x*4]+=1
                yDots[y*4]+=1
    cv2.line(image, (bC[0]+np.argmax(xDots), 0), (bC[0]+np.argmax(xDots), 240), (255, 255, 255), 1)
    cv2.line(image, (0, bC[1]+np.argmax(yDots)), (320, bC[1]+np.argmax(yDots)), (255, 255, 255), 1)
    return image


main()


