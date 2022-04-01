import cv2

img = cv2.imread("../../../Resources/lena.png", 0)
img = cv2.resize(img, None, fx=0.5, fy=0.5)

edges = cv2.Canny(img, 200, 200)

cv2.imshow("Image", edges)
cv2.waitKey()
