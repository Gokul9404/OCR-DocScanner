import cv2 
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('t2.jpg')

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 360, 240)
cv2.createTrackbar("Threshold1", "Trackbars", 200,255, nothing)
cv2.createTrackbar("Threshold2", "Trackbars", 200, 255, nothing)

while True:
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    # src = Threshold1,Threshold2

    Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    Gray_blur = cv2.GaussianBlur(Gray,(5,5), 1)

    Edges = cv2.Canny(Gray_blur,Threshold1,Threshold2)

    # contour
    contour, heirarchy = cv2.findContours(Edges, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    img_ = img.copy()

    cv2.drawContours(img_, contour , -1,(0,0,255), 5)


    cv2.imshow("Original Image", img)
    cv2.imshow("Object Edge", Edges)
    cv2.imshow("mask", img_)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
# cap.release()
cv2.destroyAllWindows()