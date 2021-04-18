import numpy as np
import cv2

image = np.zeros((720, 1080), np.uint8)
line = cv2.line(image, (0, 0), (500, 0), (255, 255, 255), 10)
line = cv2.line(line, (0, 0), (0, 500), (255, 255, 255), 10)
line = cv2.rectangle(line, (50, 50), (250, 250), (255, 255, 255), -1)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()