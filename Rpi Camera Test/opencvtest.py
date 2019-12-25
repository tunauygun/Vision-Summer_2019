import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
#cap.set(cv2.CAP_PROP_FPS,30)

while True:

    # Grab the current frame
    _, frame = cap.read()
    img = cv2.flip(frame, -1)
    cv2.imshow("Frame",img)

    key = cv2.waitKey(1)
    if key == 27:       
        break

cap.release()
cv2.destroyAllWindows()
