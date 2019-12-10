import cv2
import numpy as np

yellow = {
    'Lower_Hue': 22,
    'Higher_Hue': 38,
    'Lower_Saturation': 92,
    'Higher_Saturation': 255,
    'Lower_Value': 117,
    'Higher_Value': 255
    }

targetColor = yellow

cap = cv2.VideoCapture(0)

while True:
    # Grab the current frame
    _, frame = cap.read()
	
    # Convert image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper HSV
    lower_hsv = np.array([targetColor['Lower_Hue'], targetColor['Lower_Saturation'], targetColor['Lower_Value']])
    upper_hsv = np.array([targetColor['Higher_Hue'], targetColor['Higher_Saturation'], targetColor['Higher_Value']])

    # Blur the image. (parameters: image, (blue x, blur y) , 0)
    blur = cv2.GaussianBlur(hsv, (3,3) ,0)

    # Convert the iamge to the HSV color space
    mask = cv2.inRange(blur, lower_hsv, upper_hsv)

    # Find Contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        #find the blob biggest area
        biggest = max(contours, key = cv2.contourArea)

        #Get the location, width and height of the bounding box
        x,y,w,h = cv2.boundingRect(biggest)
        
        if __debug__:
            # Draw the bounding box around the contour in green
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            # Print the angle on the camera window (parameters: window, text, (bottomLeftCornerX,Y), font, fontScale, (fontColor), lineType)      
            cv2.putText(frame, "X: " + str(x) + "    Y: " + str(y), (10,470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

    if __debug__:
        cv2.imshow("Frame",frame)
        cv2.imshow("Mask",mask)
        
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
