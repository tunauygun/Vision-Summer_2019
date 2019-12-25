from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
    cv2.imshow("Picamera", image)

    rawCapture.truncate(0)
    key = cv2.waitKey(1)
    if key == 27:       
        break

camera.close()
cv2.destroyAllWindows()
