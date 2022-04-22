import cv2
import numpy as np

img = cv2.imread("../../Resources/1.jpg")

value = 0
def onChange(arg):
    global value
    value = arg

cv2.namedWindow("Image")
cv2.createTrackbar("Value", "Image", value, 10, onChange)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgGray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

index = 0
max = 0
maxIndex = 0
for a in contours:
    if max < len(a):
        max = len(a)
        maxIndex = index
    index += 1

mask = np.zeros_like(img)
cv2.drawContours(mask, contours, maxIndex, (255, 255, 255), -1)

out = np.zeros_like(img)
out[mask == 255] = img[mask == 255]

while True:
    size = 1 + (value / 10)
    print(size)

    out2 = cv2.resize(out, None, fx=size, fy=size)

    cv2.imshow("Image", out2)
    cv2.waitKey(1)