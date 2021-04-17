import cv2
import numpy as np

img = cv2.imread('asstets/Landscape-Color.jpg', cv2.IMREAD_UNCHANGED)

tag = img[425:525, 700:900]
img[225:325, 300:500] = tag

cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()



