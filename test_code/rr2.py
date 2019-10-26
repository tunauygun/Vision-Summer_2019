import cv2
import numpy as np
import math

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Low_Hue", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("High_Hue", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("Low_Sat", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("High_Sat", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Low_Value", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("High_Value", "Trackbars", 255, 255, nothing)

while True:

    cap = cv2.VideoCapture(0)
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    L_Hue = cv2.getTrackbarPos("Low_Hue", "Trackbars")
    H_Hue = cv2.getTrackbarPos("High_Hue", "Trackbars")
    L_Sat = cv2.getTrackbarPos("Low_Sat", "Trackbars")
    H_Sat = cv2.getTrackbarPos("High_Sat", "Trackbars")
    L_Value = cv2.getTrackbarPos("Low_Value", "Trackbars")
    H_Value=  cv2.getTrackbarPos("High_Value", "Trackbars")
        
    L_Hue = 0
    H_Hue = 22
    L_Sat = 70
    H_Sat = 160
    L_Value = 230
    H_Value =  255

    lower_red = np.array([L_Hue, L_Sat, L_Value])
    upper_red = np.array([H_Hue, H_Sat, H_Value])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    kernel = np.ones((5,5), 'uint8')
    dilate = cv2.dilate(mask, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    index = -1
    thickness = 4
    color = (255,0,255)
    
    for c in contours:
        cv2.drawContours(frame, [c], index, color, thickness)
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)

        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        radius = perimeter/(2*math.pi)
        cv2.circle(frame, (cx,cy), int(radius), (0,0,255), 2)  
##        cv2.circle(frame, (cx,cy), 4, (0,0,255), -1)




    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

print(len(contours))
print("Contour Area:", area)
print("Perimeter:", perimeter)
print("Radius:", radius)

cap.release()
cv2.destroyAllWindows()
