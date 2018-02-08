import cv2
import math
import numpy as np
import time

cap = cv2.VideoCapture(2)
cap.set(3, 320)
cap.set(4, 240)
startTime = 0
endTime = 0

null, img = cap.read()
height, width, channels = img.shape

cubiesMaskTemp = np.zeros((height, width, channels), np.uint8)
cv2.circle(cubiesMaskTemp, (160,120), 30, (255,255,255), -1)
## Create proper mask
maskFinal = cv2.inRange(cubiesMaskTemp, (1,1,1), (255,255,255))

while(1):
    startTime = time.time()
    # TODO TEMP Simulate the buffer delay
    for x in range(5):
        null, img = cap.read()

    null, img = cap.read()
    cv2.imshow('original',img)

    height, width, channels = img.shape

    hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h,s,v = cv2.split(hsvImage)
    sEq = cv2.equalizeHist(s)
    sImg = cv2.cvtColor(cv2.merge((h,sEq,v)), cv2.COLOR_HSV2BGR)

    cv2.imshow('sEq',sImg)

    hsvImage = cv2.merge((h,sEq,v))
    hsvImage = cv2.bitwise_and(hsvImage, hsvImage, mask = maskFinal)

    output = cv2.cvtColor(hsvImage, cv2.COLOR_HSV2BGR)
    cv2.imshow('test', output)

    largestContour = 0
    largestContourArea = 0
    cX = 0
    cY = 0
    largestContourMask = None
    increment = 10
    for x in range(0, 180, increment):
        #thresholdMask = cv2.inRange(hsvImage, (x,10,40), (x+10,255,255))
        print("lower:{0}, upper{1}".format(x-increment/2, x+increment/2))
        thresholdMask = cv2.inRange(hsvImage, (x,10,95), (x+increment,255,255))

        #kernel = np.ones((5,5),np.uint8)
        #for y in range(4):
        #    thresholdMask = cv2.dilate(thresholdMask,kernel)
        #    thresholdMask = cv2.erode(thresholdMask,kernel)


        contours, hierarchy = cv2.findContours(thresholdMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cnts = sorted(contours, key = cv2.contourArea)[-5:]
        contours = cnts

        for contour in contours:
            M = cv2.moments(contour)
            if cv2.contourArea(contour) > largestContourArea and M["m00"] != 0:
                largestContour = contour
                largestContourArea = cv2.contourArea(contour)
                largestContourMask = thresholdMask
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

    #cv2.drawContours(res2, largestContour, -1, (0,0,100), 4)
    if largestContourMask is not None:
        cv2.drawContours(output, largestContour, -1, cv2.mean(output, largestContourMask), 4)

    endTime = time.time()
    print("Elapsed: {0}".format(endTime-startTime))

    cv2.imshow('res', output)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    

cv2.destroyAllWindows()
