import cv2
import math
import numpy as np

img = np.ones((510, 510, 3), np.uint8)
mousePos = None
hsv = None
value: int = 128


def onValueChange(args):
    global value
    value = args


def distance(a, b):
    return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))


def onMouse(event, x, y, flags, param):
    global mousePos
    if event == cv2.EVENT_LBUTTONUP:
        mousePos = (x, y)


cv2.namedWindow("Image")
cv2.setMouseCallback("Image", onMouse)

cv2.namedWindow("Toolbar")
cv2.createTrackbar("Value", "Toolbar", 0, 255, onValueChange)

while True:
    for x in range(510):
        for y in range(510):
            ox = x - 255
            oy = y - 255

            h = math.atan2(ox, oy)
            if h < 0:
                h = 2 * math.pi + h
            h *= 180 / (2 * math.pi)

            s = distance((0, 0), (ox, oy))

            v = value
            if s > 255:
                v = 0

            img[x, y] = (h, s, v)

            if mousePos:
                hsv = (h, s, v)

    imgHSV = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

    if mousePos:
        ox = mousePos[1] - 255
        oy = mousePos[0] - 255

        h = math.atan2(ox, oy)
        if h < 0:
            h = 2 * math.pi + h
        h *= 180 / (2 * math.pi)

        s = distance((0, 0), (ox, oy))

        v = value
        if s > 255:
            v = 0

        hsv = (h, s, v)
        break

    cv2.imshow("Image", imgHSV)
    cv2.waitKey(1)

cv2.destroyAllWindows()

imgC = np.zeros((510, 510, 3), np.uint8)
imgC[:, :] = hsv
imgC = cv2.cvtColor(imgC, cv2.COLOR_HSV2BGR)
cv2.imshow("Image", imgC)
cv2.waitKey()