import cv2
import numpy as np
import math

def nothing(x):
    pass

img = cv2.imread("640_480.jpg", 1)


'''cv2.namedWindow("Trackbars")
cv2.createTrackbar("Low_Hue", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("High_Hue", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("Low_Sat", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("High_Sat", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Low_Value", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("High_Value", "Trackbars", 255, 255, nothing)'''

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
while True: 
    '''L_Hue = cv2.getTrackbarPos("Low_Hue", "Trackbars")
    H_Hue = cv2.getTrackbarPos("High_Hue", "Trackbars")
    L_Sat = cv2.getTrackbarPos("Low_Sat", "Trackbars")
    H_Sat = cv2.getTrackbarPos("High_Sat", "Trackbars")
    L_Value = cv2.getTrackbarPos("Low_Value", "Trackbars")
    H_Value=  cv2.getTrackbarPos("High_Value", "Trackbars")'''
        
    L_Hue = 22
    H_Hue = 38
    L_Sat = 92
    H_Sat = 255
    L_Value = 117
    H_Value =  255

    lower_red = np.array([L_Hue, L_Sat, L_Value])
    upper_red = np.array([H_Hue, H_Sat, H_Value])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    kernel = np.ones((5,5), 'uint8')
    dilate = cv2.dilate(mask, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img2 = img.copy()
    index = -1
    thickness = 4
    color = (255,0,255)

    cv2.drawContours(img2, contours, index, color, thickness)
    area = cv2.contourArea(contours[0])
    perimeter = cv2.arcLength(contours[0], True)
    radius = perimeter/(2*math.pi)
    M = cv2.moments(contours[0])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(img2, (cx,cy), 4, (0,0,255), -1)
    cv2.circle(img2, (cx,cy), int(radius), (0,0,255), 2)

    cv2.imshow("Img",img)
    cv2.imshow("Img2",img2)
    cv2.imshow("Mask",mask)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
##cv2.waitKey(0)

print(len(contours))
print("Contour Area:", area)
print("Perimeter:", perimeter)
print("Radius:", radius)

cv2.destroyAllWindows()
