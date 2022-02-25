import cv2

img = cv2.imread("../../Resources/lena.png")
img = cv2.resize(img, None, fx=0.5, fy=0.5)
imgSize = (img.shape[1], img.shape[0])

center = (imgSize[0] / 2, imgSize[1] / 2)

rotateMatrix = cv2.getRotationMatrix2D(center, 45, 1)

rotatedImg = cv2.warpAffine(img, rotateMatrix, imgSize)

cv2.imshow("Image", img)
cv2.imshow("Rotated Image", rotatedImg)
cv2.waitKey()