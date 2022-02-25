import math
import cv2
import numpy as np

img = cv2.imread("../../../Resources/cards.jpg")

mousePosition: tuple[int, int] = (0, 0)
isMouseDrag: bool = False
isMouseDown: bool = False
rectStartPos: tuple[int, int] = (0, 0)
points: list[tuple[int, int]] = []
selectedPointIndex: int = -1

def distance(a, b):
    return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))


def onMouse(event, x, y, flags, param):
    global mousePosition
    global isMouseDrag
    global isMouseDown
    global selectedPointIndex
    global rectStartPos
    global points

    mousePosition = (x, y)

    if event == cv2.EVENT_LBUTTONDOWN:
        rectStartPos = (x, y)
        isMouseDrag = True

    if event == cv2.EVENT_LBUTTONUP:
        points = [rectStartPos, (x, rectStartPos[1]), (x, y), (rectStartPos[0], y)]
        isMouseDrag = False

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, point in enumerate(points):
            if distance(point, (x, y)) < 20:
                selectedPointIndex = i
        isMouseDown = True

    if event == cv2.EVENT_RBUTTONUP:
        selectedPointIndex = -1
        isMouseDown = False

    if event == cv2.EVENT_MOUSEMOVE:
        if isMouseDown and selectedPointIndex != -1:
            points[selectedPointIndex] = (x, y)


cv2.imshow("Image", img)
cv2.setMouseCallback("Image", onMouse)

while True:
    img = cv2.imread("../../../Resources/cards.jpg")

    if isMouseDrag:
        cv2.rectangle(img, rectStartPos, (mousePosition[0], mousePosition[1]), (0, 0, 255), 2)
    else:
        if len(points) == 4:
            width = distance(points[0], points[1])
            height = distance(points[0], points[3])

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
            cv2.imshow("Warped image", out_image)

            # Draw frame lines
            cv2.line(img, points[0], points[1], (0, 0, 255), 2)
            cv2.line(img, points[1], points[2], (0, 0, 255), 2)
            cv2.line(img, points[2], points[3], (0, 0, 255), 2)
            cv2.line(img, points[3], points[0], (0, 0, 255), 2)

            # Draw frame vertices
            for point in points:
                cv2.circle(img, point, 5, (255, 0, 0), -1)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        print("Clear points")
        points = []
    if key == ord('s'):
        if len(points) == 4:
            cv2.imwrite("Outputs/warped-image.jpg", out_image)
            break
