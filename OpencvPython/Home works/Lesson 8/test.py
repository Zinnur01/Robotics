import math

import cv2
import numpy as np

def distance(pt1, pt2):
    return int(math.sqrt((pt1[0] - pt2[0]) * (pt1[0] - pt2[0]) + (pt1[1] - pt2[1]) * (pt1[1] - pt2[1])))

cellSize = 2

img = cv2.imread("../../Resources/1.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 0, 0.02, 10)
corners = np.int0(corners)

points: list[tuple[int, int]] = []

for i in corners:
    x, y = i.ravel()
    points.append((x, y))
    cv2.circle(img, (x, y), 3, 255, -1)




coin = cv2.imread("../../Resources/2.jpg")
cannyCoin = cv2.Canny(coin, 650, 650)
contours, hierarchy = cv2.findContours(cannyCoin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

index = 0
max = 0
maxIndex = 0
for a in contours:
    if max < len(a):
        max = len(a)
        maxIndex = index
    index += 1

mask = np.zeros_like(coin)
cv2.drawContours(mask, contours, maxIndex, (255, 255, 255), -1)

out = np.zeros_like(coin)
out[mask == 255] = coin[mask == 255]

minX = 1000000
maxX = 0

minY = 1000000
maxY = 0

for a in contours[maxIndex]:
    b = a[0]
    if b[0] < minX:
        minX = b[0]

    if b[0] > maxX:
        maxX = b[0]

    if b[1] < minY:
        minY = b[1]

    if b[1] > maxY:
        maxY = b[1]

cv2.rectangle(coin, (minX, minY), (maxX, maxY), (255, 0, 0), 1)

corners = [(minX, minY), (minX, maxY), (maxX, maxY), (maxX, minY)]
corners2 = []

for a in corners:
    minDistance = 1000000
    index = 0
    for i in range(len(points)):
        if distance(a, points[i]) < minDistance:
            minDistance = distance(a, points[i])
            index = i

    corners2.append(index)

cv2.rectangle(coin, points[corners2[0]], points[corners2[2]], (0, 0, 255), 1)

cellWidth = distance(points[corners2[1]], points[corners2[2]])
cellHeight = distance(points[corners2[0]], points[corners2[1]])

coinWidth = distance(corners[1], corners[2])
coinHeight = distance(corners[0], corners[1])

w = math.floor((coinWidth * cellSize) / cellWidth * 100) / 100
h = math.floor((coinHeight * cellSize) / cellHeight * 100) / 100

print(f'Width: {w}sm\nHeight: {h}sm')

cv2.imshow("Image", coin)
cv2.waitKey(0)