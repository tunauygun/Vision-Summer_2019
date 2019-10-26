import cv2
import numpy as np

img = cv2.imread("640_480", 1)

cv2.imshow("test_image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
