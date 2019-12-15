import cv2
import numpy as np

def nothing(x):
    # any operation
    pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 26, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 52, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 36, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

yellow = {
    'Lower_Hue': 22,
    'Higher_Hue': 38,
    'Lower_Saturation': 92,
    'Higher_Saturation': 255,
    'Lower_Value': 117,
    'Higher_Value': 255
    }

#targetColor = yellow2

cap = cv2.VideoCapture(0)

while True:
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")
    
    # Grab the current frame
    _, frame = cap.read()
	
    # Convert image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_hsv = np.array([l_h, l_s, l_v])
    upper_hsv = np.array([u_h, u_s, u_v])

    # Define the lower and upper HSV
    #lower_hsv = np.array([targetColor['Lower_Hue'], targetColor['Lower_Saturation'], targetColor['Lower_Value']])
    #upper_hsv = np.array([targetColor['Higher_Hue'], targetColor['Higher_Saturation'], targetColor['Higher_Value']])

    # Blur the image. (parameters: image, (blue x, blur y) , 0)
    blur = cv2.GaussianBlur(hsv, (3,3) ,0)

    # Convert the iamge to the HSV color space
    mask = cv2.inRange(blur, lower_hsv, upper_hsv)

    # Find Contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if len(approx) == 3:
                tx,ty,tw,th = cv2.boundingRect(cnt)
                cv2.rectangle(frame,(tx,ty),(tx+tw,ty+th),(0,255,0),2)

            elif len(approx) == 4:
                rx,ry,rw,rh = cv2.boundingRect(cnt)
                cv2.rectangle(frame,(rx,ry),(rx+rw,ry+rh),(255,0,0),2)
            else:
                cx,cy,cw,ch = cv2.boundingRect(cnt)
                cv2.rectangle(frame,(cx,cy),(cx+cw,cy+ch),(0,0,255),2)
        
        #find the blob biggest area
        #biggest = max(contours, key = cv2.contourArea)

        #Get the location, width and height of the bounding box
        #x,y,w,h = cv2.boundingRect(biggest)
        
        #if __debug__:
            # Draw the bounding box around the contour in green
            #cv2.rectangle(frame,(tx,ty),(tx+tw,ty+th),(0,255,0),2)
            #cv2.rectangle(frame,(rx,ry),(rx+rw,ry+rh),(255,0,0),2)
            #cv2.rectangle(frame,(cx,cy),(cx+cw,cy+ch),(0,0,255),2)

            # Print the angle on the camera window (parameters: window, text, (bottomLeftCornerX,Y), font, fontScale, (fontColor), lineType)      
            #cv2.putText(frame, "X: " + str(rx) + "    Y: " + str(ry), (10,470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

    if __debug__:
        cv2.imshow("Frame",frame)
        cv2.imshow("Mask",mask)
        
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
