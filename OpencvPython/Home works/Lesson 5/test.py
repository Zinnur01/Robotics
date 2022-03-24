import cv2

img = cv2.imread("../../Resources/lena.png")

cv2.imshow("Image", img)
cv2.waitKey()
cv2.destroyAllWindows()