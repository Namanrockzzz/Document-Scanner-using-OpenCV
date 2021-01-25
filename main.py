import cv2
import numpy as np

########################################
widthImg = 640
heightImg = 480
########################################
cap = cv2.VideoCapture('http://192.168.1.65:4747/mjpegfeed?640x480')
cap.set(3,widthImg) # set width to 1920 (width has id=3)
cap.set(4,heightImg) # set height to 1080 (height has id=4)
cap.set(10,150) # set brightness to 100

def preProcess(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>5000:
            # cv2.drawContours(imgContour, cnt, -1, (255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area>maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255,0,0),20)
    return biggest

def getWarp(img,biggest):
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput = cv2.warpPerspective(img,matrix,(widthImg,heightImg))
    return imgOutput

while True:
    success , img = cap.read()
    cv2.resize(img,(widthImg,heightImg))
    imgContour = img.copy()
    imgThres = preProcess(img)
    biggest = getContours(imgThres)
    imgWarped = getWarp(img,biggest)
    #print(biggest)
    cv2.imshow("Video", imgWarped)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

