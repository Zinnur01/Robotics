import cv2
import numpy as np

img = cv2.imread("../../Resources/map.png")

kernel = np.array([
    [-0.5, -0.5, -0.5,-0.5,-0.5, -0.5,-0.5,-0.5,-0.5,-0.5,-0.5, -0.5,-0.5,-0.5,-0.5,-0.5, 17,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5 ]
])

out = cv2.filter2D(img, -1, kernel)


cv2.imshow("Filtered", out)
cv2.waitKey()