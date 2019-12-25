import cv2
import numpy as np

#Preset HSV(Hue-Saturation-Value) Values
yellow = {
    'Lower_Hue': 22,
    'Higher_Hue': 38,
    'Lower_Saturation': 92,
    'Higher_Saturation': 255,
    'Lower_Value': 117,
    'Higher_Value': 255
    }
orange = {
    'Lower_Hue': 0,
    'Higher_Hue': 11,
    'Lower_Saturation': 161,
    'Higher_Saturation': 252,
    'Lower_Value': 0,
    'Higher_Value': 255
    }

# Use a preset color as the target color
targetColor = orange

# Starts the camera
cap = cv2.VideoCapture(0)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
#cap.set(cv2.CAP_PROP_FPS,40)

while True:    
    # Grab the current frame
    _, frame = cap.read()

    # Rotates the frame 180 degrees
    # Uncomment the following line if the camera is mounted upside down
    frame = cv2.flip(frame, -1)
    
    # Convert image from BGR(Blue-Green-Red) to HSV(Hue-Saturation-Value) color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper HSV based on selected color
    lower_hsv = np.array([targetColor['Lower_Hue'], targetColor['Lower_Saturation'], targetColor['Lower_Value']])
    upper_hsv = np.array([targetColor['Higher_Hue'], targetColor['Higher_Saturation'], targetColor['Higher_Value']])

    # Blur the image. (parameters: image, (blue x, blur y) , 0)
    blur = cv2.GaussianBlur(hsv, (3,3) ,0)

    # Filters the image based on the HSV values
    mask = cv2.inRange(blur, lower_hsv, upper_hsv)

    # Get the boundaries of continuous pixels in defined range
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sorts the contours by their area (biggest to smallest)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    if len(contours) != 0:
        for cnt in contours:

            # Draws a polygon around the contours (Change the multiplier to adjust the sensitivity)
            approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)
            
            # Checks the number of sides and draws a bounding rectangle
            if len(approx) == 3:
                tx,ty,tw,th = cv2.boundingRect(cnt)
                cv2.rectangle(frame,(tx,ty),(tx+tw,ty+th),(0,255,0),2)
            elif len(approx) == 4:
                rx,ry,rw,rh = cv2.boundingRect(cnt)
                cv2.rectangle(frame,(rx,ry),(rx+rw,ry+rh),(255,0,0),2)
            else:
                cx,cy,cw,ch = cv2.boundingRect(cnt)
                cv2.rectangle(frame,(cx,cy),(cx+cw,cy+ch),(0,0,255),2)
        
        if __debug__:
            # Print the angle on the camera window (parameters: window, text, (bottomLeftCornerX,Y), font, fontScale, (fontColor), lineType)      
            cv2.putText(frame, "X: " + str(rx) + "    Y: " + str(ry), (15,225), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,255), 2)
        
    if __debug__:
    	# Displays the frames from camera
        cv2.imshow("Frame",frame)
        cv2.imshow("Mask",mask)
                 
    # Exit the loop when ESC is pressed           
    key = cv2.waitKey(1)
    if key == 27:
        break

# Close the camera and all open windows
cap.release()
cv2.destroyAllWindows()
