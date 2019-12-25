from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
cap.set(cv2.CAP_PROP_FPS, 40)
start = time.time()
for i in range(400):
    _, frame = cap.read()

    cv2.imshow("Frame",frame)
print("Time for {0} frames: {1} seconds".format(400, time.time() - start))
