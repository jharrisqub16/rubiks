import cv2
import numpy as np
#optional argument
def nothing(x):
    pass
cap = cv2.VideoCapture(2) #Cam 0,1,2
cv2.namedWindow('image')

#easy assigments
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'

cv2.createTrackbar(hl, 'image',0,179,nothing)
cv2.createTrackbar(hh, 'image',179,179,nothing)
cv2.createTrackbar(sl, 'image',0,255,nothing)
cv2.createTrackbar(sh, 'image',255,255,nothing)
cv2.createTrackbar(vl, 'image',0,255,nothing)
cv2.createTrackbar(vh, 'image',255,255,nothing)



null,frame=cap.read()
height, width, channels = frame.shape
cubiesMaskInitial = np.zeros((height, width, channels), np.uint8)
## Draw circle "view ports" on mask

## Radius of porthole circles that are drawn on a mask to show individual cubies
## TODO
portholeRadius = 11

cv2.circle(cubiesMaskInitial, (35 , 125), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (40 , 195), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (45 , 265), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (95 , 160), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (100, 300), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (155, 200), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (160, 290), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (165, 350), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (225, 200), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (225, 290), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (225, 350), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (295, 170), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (280, 310), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (355, 125), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (345, 195), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (345, 265), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (55 , 75 ), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (120, 100), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (190, 135), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (125, 40 ), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (260, 100), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (195, 15 ), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (260, 40 ), portholeRadius, (255,255,255), -1)
cv2.circle(cubiesMaskInitial, (330, 70 ), portholeRadius, (255,255,255), -1)

## Create proper mask
cubiesMaskFinal = cv2.inRange(cubiesMaskInitial, (1,1,1), (255,255,255))

#cv2.imshow('portholes',cubiesMarkFinal)

while(1):
    null,frame=cap.read()
    croppedImage = frame[55:455, 120:505]
    ##frame=cv2.GaussianBlur(frame,(5,5),0)
    #convert to HSV from BGR
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    firstImage = cv2.bitwise_and(hsv, hsv, mask = cubiesMaskFinal)

    #read trackbar positions for all
    hul=cv2.getTrackbarPos(hl, 'image')
    huh=cv2.getTrackbarPos(hh, 'image')
    sal=cv2.getTrackbarPos(sl, 'image')
    sah=cv2.getTrackbarPos(sh, 'image')
    val=cv2.getTrackbarPos(vl, 'image')
    vah=cv2.getTrackbarPos(vh, 'image')
    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    #apply the range on a mask
    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(frame,frame, mask =mask)

    cv2.imshow('image', res)
    cv2.imshow('yay', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
