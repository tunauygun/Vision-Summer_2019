import cv2
import numpy as np
import math

def nothing(x):
    # any operation
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Tresh1", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Tresh2", "Trackbars", 0, 255, nothing)

cap = cv2.VideoCapture(0)

while True:

    # Grab the current frame
    _, frame = cap.read()

    # Blur the image. (parameters: image, (blue x, blur y) , 0)
    blur = cv2.GaussianBlur(frame, (5,5) ,0)

    #kernel = np.ones((5,5), 'uint8')
    #erode = cv2.erode(edges, kernel, iterations=2)
    #dilate = cv2.dilate(erode, kernel, iterations=2)

    tresh1 = cv2.getTrackbarPos("Tresh1", "Trackbars")
    tresh2 = cv2.getTrackbarPos("Tresh2", "Trackbars")

    edges = cv2.Canny(blur,tresh1,256)

    unsorted_contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(unsorted_contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    font = cv2.FONT_HERSHEY_DUPLEX
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(frame, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if len(approx) == 3:
            cv2.putText(frame, "Triangle", (x, y), font, 1, (0))
        elif len(approx) == 4:
            cv2.putText(frame, "Rectangle", (x, y), font, 1, (0))
        elif len(approx) == 5:
            cv2.putText(frame, "Pentagon", (x, y), font, 1, (0))
        elif 6 < len(approx) < 15:
            cv2.putText(frame, "Ellipse", (x, y), font, 1, (0))
        else:
            cv2.putText(frame, "Circle", (x, y), font, 1, (0))

    cv2.imshow("Frame",frame)
    cv2.imshow("Edges",edges)
    #cv2.imshow("Dilate",dilate)

    key = cv2.waitKey(1)
    if key == 27:       
        break
    
cap.release()
cv2.destroyAllWindows()
    
'''    targets = []

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
        #print("x:", target_x, " y:", target_y)
        displayInfo ="x: " + str(target_x) + "   y: " + str(target_y)
        cv2.putText(frame, displayInfo, (10,470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

    cv2.imshow("Frame",frame)
    cv2.imshow("Dilate",dilate)

    key = cv2.waitKey(1)
    if key == 27:       
        break

cap.release()
cv2.destroyAllWindows()
'''
