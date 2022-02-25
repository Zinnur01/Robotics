import math

import cv2
import time

img = cv2.imread("../../Resources/lena.png")
img = cv2.resize(img, None, fx=0.5, fy=0.5)
imgSize = (img.shape[1], img.shape[0])

center = (imgSize[0] / 2, imgSize[1] / 2)

pTime = 0

while True:
    img = cv2.imread("../../Resources/lena.png")
    img = cv2.resize(img, None, fx=0.5, fy=0.5)

    cTime = time.time()
    fps = int(1 / (cTime - pTime))
    pTime = cTime

    rotateMatrix = cv2.getRotationMatrix2D(center, time.time() * 90, 1/math.sqrt(2))
    rotatedImg = cv2.warpAffine(img, rotateMatrix, imgSize)

    cv2.putText(rotatedImg, f"{fps}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Rotated Image", rotatedImg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()