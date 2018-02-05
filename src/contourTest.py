import cv2
import math
import numpy as np

cap = cv2.VideoCapture(0)

while(1):
    null, img = cap.read()
    cv2.imshow('original',img)

    height, width, channels = img.shape

    res2=img
    #maskImg = np.zeros((height, width, channels), np.uint8)
    #cv2.circle(maskImg, (320,240), 150, (255,255,255), -1)
    #maskImg = cv2.inRange(maskImg, (1,1,1), (255,255,255))


    #Z = cv2.bitwise_and(img, img, mask = maskImg)

    #cv2.imshow('masked', Z)
    #res2=Z

    #Z = Z.reshape((-1,3))
    #Z = np.float32(Z)

    ## define criteria, number of clusters(K) and apply kmeans()
    #criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    #K = 6

    #ret,label,center=cv2.kmeans(Z,K,criteria,10,0)

    #center = np.uint8(center)
    #res = center[label.flatten()]
    #res2 = res.reshape((img.shape))

    largestContour = 0
    largestContourArea = 0
    cX = 0
    cY = 0
    largestContourMask = 0
    for x in range(0, 180, 10):
        hsvImage = cv2.cvtColor(res2, cv2.COLOR_BGR2HSV)

        h,s,v = cv2.split(hsvImage)

        vEq = cv2.equalizeHist(v)
        sEq = cv2.equalizeHist(s)

        sImg = cv2.cvtColor(cv2.merge((h,sEq,v)), cv2.COLOR_HSV2BGR)
        vImg = cv2.cvtColor(cv2.merge((h,s,vEq)), cv2.COLOR_HSV2BGR)
        svImg =cv2.cvtColor( cv2.merge((h,sEq,vEq)),  cv2.COLOR_HSV2BGR)

        cv2.imshow('sEq',sImg)
        cv2.imshow('vEq',vImg)
        cv2.imshow('s and v Eq',svImg)

        #hsvImage = cv2.merge((h,sEq,vEq))
        hsvImage = cv2.merge((h,sEq,v))
        #hsvImage = cv2.merge((h,s,v))

        convertedImage = cv2.cvtColor(hsvImage, cv2.COLOR_HSV2BGR)
        cv2.imshow('ppost-equa', convertedImage)

        #thresholdMask = cv2.inRange(hsvImage, (x,10,40), (x+10,255,255))
        thresholdMask = cv2.inRange(hsvImage, (x,10,95), (x+10,255,255))

        kernel = np.ones((5,5),np.uint8)
        for y in range(4):
            thresholdMask = cv2.dilate(thresholdMask,kernel)
            thresholdMask = cv2.erode(thresholdMask,kernel)


        contours, hierarchy = cv2.findContours(thresholdMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            M = cv2.moments(contour)
            if cv2.contourArea(contour) > largestContourArea and M["m00"] != 0:
                largestContour = contour
                largestContourArea = cv2.contourArea(contour)
                largestContourMask = thresholdMask
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

    #cv2.drawContours(res2, largestContour, -1, (0,0,100), 4)
    cv2.drawContours(res2, largestContour, -1, cv2.mean(img, largestContourMask), 4)

    cv2.imshow('res2',res2)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    

cv2.destroyAllWindows()
