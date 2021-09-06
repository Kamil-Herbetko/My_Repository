import numpy as np
import cv2, imutils, pyautogui

image = pyautogui.screenshot()
image = cv2.resize(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR), (0, 0), fx=0.25, fy=0.25)
cv2.imshow("screenshot", image)
cv2.waitKey(0)
cv2.destroyAllWindows()