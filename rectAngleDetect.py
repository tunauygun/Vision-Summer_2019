import cv2
import numpy as np
import math

# Read the image
img = cv2.imread("CargoAngledDark48in.jpg", 1)
originalImg = img.copy()

# Convert image to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define the lower and upper HSV
lower_hsv = np.array([63, 192, 126])
upper_hsv = np.array([87, 255, 255])

# Blur the image. (parameters: image, (blue x, blur y) , 0)
blur = cv2.GaussianBlur(hsv, (5,5) ,0)

# Convert the iamge to the HSV color space
mask = cv2.inRange(blur, lower_hsv, upper_hsv)

kernel = np.ones((3,3), 'uint8')
erode = cv2.erode(mask, kernel, iterations=2)
dilate = cv2.dilate(erode, kernel, iterations=2)

contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

targets = []

for cnt in contours:
	rect = cv2.minAreaRect(cnt)
	pts = cv2.boxPoints(rect)
	pts = np.int0(pts)
	cv2.drawContours(img, [pts], 0, (0 , 0, 255), 2)

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

print("Coordinates of the target:")

for i in targets:
	target_x, target_y = i
	cv2.circle(img,(target_x, target_y), 5, (0,255,0), -1)
	print("x:", target_x, " y:", target_y)



cv2.imshow("Original Img", originalImg)
cv2.imshow("Img",img)
cv2.imshow("Dilate",dilate)

cv2.waitKey(0)
cv2.destroyAllWindows()