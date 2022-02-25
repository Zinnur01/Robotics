import math
import cv2
import numpy as np

img = cv2.imread("../../../Resources/cards.jpg")

mousePosition: tuple[int, int] = (0, 0)
isMouseDrag: bool = False
isMouseDown: bool = False
rectStartPos: tuple[int, int] = (0, 0)
groups: list[tuple[int, int]] = [()]
selectedPointIndex: int = -1
selectedGroupIndex: int = 0


def distance(a, b):
    return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))


def onMouse(event, x, y, flags, param):
    global mousePosition
    global isMouseDrag
    global isMouseDown
    global rectStartPos
    global groups
    global selectedPointIndex
    global selectedGroupIndex

    mousePosition = (x, y)

    if event == cv2.EVENT_LBUTTONDOWN:
        rectStartPos = (x, y)
        isMouseDrag = True

    if event == cv2.EVENT_LBUTTONUP:
        groups[selectedGroupIndex] = [rectStartPos, (x, rectStartPos[1]), (x, y), (rectStartPos[0], y)]
        isMouseDrag = False

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, point in enumerate(groups[selectedGroupIndex]):
            if distance(point, (x, y)) < 20:
                selectedPointIndex = i
        isMouseDown = True

    if event == cv2.EVENT_RBUTTONUP:
        selectedPointIndex = -1
        isMouseDown = False

    if event == cv2.EVENT_MOUSEMOVE:
        if isMouseDown and selectedPointIndex != -1:
            groups[selectedGroupIndex][selectedPointIndex] = (x, y)


cv2.imshow("Image", img)
cv2.setMouseCallback("Image", onMouse)

while True:
    img = cv2.imread("../../../Resources/cards.jpg")
    img_copy = img.copy()

    for i, points in enumerate(groups):
        vertexColor = (0, 0, 255)
        lineColor = (0, 0, 255)
        if i == selectedGroupIndex:
            vertexColor = (255, 0, 0)
            lineColor = (0, 255, 0)

        if isMouseDrag and i == selectedGroupIndex:
            cv2.rectangle(img_copy, rectStartPos, (mousePosition[0], mousePosition[1]), (0, 255, 0), 2)
        else:
            if points:
                width = distance(points[0], points[1])
                height = distance(points[1], points[2])

                # Calculate perspective matrix
                fromMatrix = np.float32([points[0], points[1], points[2], points[3]])
                toMatrix = np.float32([
                    [0, 0],
                    [width, 0],
                    [width, height],
                    [0, height]
                ])
                perspectiveMatrix = cv2.getPerspectiveTransform(fromMatrix, toMatrix)
                # Warp perspective image
                out_image = cv2.warpPerspective(img, perspectiveMatrix, (width, height))
                cv2.imshow(f"Warped image {i}", out_image)

                # Draw frame lines
                cv2.line(img_copy, points[0], points[1], lineColor, 2)
                cv2.line(img_copy, points[1], points[2], lineColor, 2)
                cv2.line(img_copy, points[2], points[3], lineColor, 2)
                cv2.line(img_copy, points[3], points[0], lineColor, 2)

                # Draw frame vertices
                for point in points:
                    cv2.circle(img_copy, point, 5, vertexColor, -1)

    cv2.putText(img_copy, f"Selected group: {selectedGroupIndex}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                2)

    cv2.imshow("Image", img_copy)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        print("Clear points")
        groups[selectedGroupIndex] = []
    if key == ord('d'):
        selectedGroupIndex += 1
        if len(groups) <= selectedGroupIndex:
            groups.append(())
    if key == ord('a'):
        selectedGroupIndex -= 1
        if selectedGroupIndex < 0:
            selectedGroupIndex = 0
