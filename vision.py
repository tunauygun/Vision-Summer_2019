import cv2
import numpy as np
import math

L_Hue = 22
H_Hue = 38
L_Sat = 92
H_Sat = 255
L_Value = 117
H_Value =  255
    
def nothing(x):
    pass

cap = cv2.VideoCapture(0)

while True:

    _, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([L_Hue, L_Sat, L_Value])
    upper_red = np.array([H_Hue, H_Sat, H_Value])

    blur = cv2.GaussianBlur(hsv, (5,5) ,0)

    mask = cv2.inRange(blur, lower_red, upper_red)

    kernel = np.ones((3,3), 'uint8')
    erode = cv2.erode(mask, kernel, iterations=2)
    dilate = cv2.dilate(erode, kernel, iterations=2)


    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    index = -1
    thickness = 4
    color = (255,255,0)

    if len(contours) != 0:
        # draw in blue the contours that were founded
##        cv2.drawContours(frame, contours, index, color, thickness)

        #find the biggest area
        biggest = max(contours, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(biggest)
        # draw the  contour in green
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        M = cv2.moments(biggest)
        ((cx, cy), radius) = cv2.minEnclosingCircle(biggest)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
##        cv2.circle(frame, center, int(radius), (0, 0, 255), 2)

        area = cv2.contourArea(biggest)
##        print("Area: {}    Center: {}    Radius: {}    Width: {}    Height: {}" .format(area, center, int(radius),w,h))

        angle = math.degrees(math.atan((int(M["m10"] / M["m00"])-320)/554.3))

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText =(10,400)
        fontScale = 0.7
        fontColor = (255,255,255)
        lineType = 2
        cv2.putText(frame, str(round(angle,2))+" degrees", bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",mask)
    cv2.imshow("Erode",erode)
    cv2.imshow("Dilate",dilate)

        
    key = cv2.waitKey(1)
    if key == 27:
        print(hsv.shape)        
        break

cap.release()
cv2.destroyAllWindows()



























