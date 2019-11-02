import cv2
import numpy as np
import math

# Lower ang Higher HSV Values
L_Hue = 73
H_Hue = 106
L_Sat = 87
H_Sat = 232
L_Value = 33
H_Value = 255

cap = cv2.VideoCapture(0)

while True:

    # Grab the current frame
    _, frame = cap.read()

    # Convert image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper HSV
    lower_hsv = np.array([L_Hue, L_Sat, L_Value])
    upper_hsv = np.array([H_Hue, H_Sat, H_Value])

    # Blur the image. (parameters: image, (blue x, blur y) , 0)
    blur = cv2.GaussianBlur(hsv, (5,5) ,0)

    # Convert the iamge to the HSV color space
    mask = cv2.inRange(blur, lower_hsv, upper_hsv)

    kernel = np.ones((3,3), 'uint8')
    erode = cv2.erode(mask, kernel, iterations=2)
    dilate = cv2.dilate(erode, kernel, iterations=2)

    unsorted_contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(unsorted_contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
    targets = []

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        pts = cv2.boxPoints(rect)
        pts = np.int0(pts)
        cv2.drawContours(frame, [pts], 0, (0 , 0, 255), 2)

    for i in range(len(contours)-1):
        left = contours[i]
        right = contours[i+1]
        l_center, l_dimentions, l_angle = cv2.minAreaRect(left)
        r_center, r_dimentions, r_angle = cv2.minAreaRect(right)

        if l_angle<=-70 and l_angle>=-80 and r_angle<=-10 and r_angle>=-20:
            l_center_x, l_center_y = l_center
            r_center_x, r_center_y = r_center
            x_midPoint = int((l_center_x+r_center_x)/2)
            y_midPoint = int((l_center_y+r_center_y)/2)

            targets.append((x_midPoint,y_midPoint))

        

    for i in targets:
        target_x, target_y = i
        cv2.circle(frame,(target_x, target_y), 5, (0,255,0), -1)
        print("x:", target_x, " y:", target_y)

    cv2.imshow("Frame",frame)
    cv2.imshow("Dilate",dilate)

    key = cv2.waitKey(1)
    if key == 27:       
        break

cap.release()
cv2.destroyAllWindows()
