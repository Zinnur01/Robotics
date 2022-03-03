import cv2
import numpy as np
import math
import time

cap = cv2.VideoCapture("../../..//Resources/crossroad.mp4")
frameSize = int(cap.get(3)), int(cap.get(4))
frame = cap.read()[1]

points: list[tuple[int, int]] = []
mousePosition: tuple[int, int] = (0, 0)
isMouseDrag: bool = False
isMouseDown: bool = False
rectStartPos: tuple[int, int] = (0, 0)
selectedPointIndex: int = -1
cTime: float
pTime: float = 0


def distance(a, b):
    return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))


def onMouse(event, x, y, flags, param):
    global mousePosition
    global isMouseDrag
    global isMouseDown
    global rectStartPos
    global selectedPointIndex
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


cv2.namedWindow("Crossroad")
cv2.setMouseCallback("Crossroad", onMouse)


while True:
    success, frame = cap.read()

    if not success:
        break

    if cap.get(1) == cap.get(7):
        cap.set(1, 0)

    if points:
        width = distance(points[0], points[1])
        height = distance(points[1], points[2])

        # Calculate perspective matrix
        fromMatrix = np.float32([points[0], points[1], points[2], points[3]])
        toMatrix = np.float32([
            [frameSize[0] / 2 - width / 2, frameSize[1] / 2 - height / 2],
            [frameSize[0] / 2 + width / 2, frameSize[1] / 2 - height / 2],
            [frameSize[0] / 2 + width / 2, frameSize[1] / 2 + height / 2],
            [frameSize[0] / 2 - width / 2, frameSize[1] / 2 + height / 2]
        ])
        perspectiveMatrix = cv2.getPerspectiveTransform(fromMatrix, toMatrix)

        # Warp perspective image
        topView = cv2.warpPerspective(frame, perspectiveMatrix, frameSize)
        cv2.imshow(f"Crossroad top view", topView)

    cTime = time.time()
    fps = int(1 / (cTime - pTime))
    pTime = cTime

    cv2.putText(frame, f"{fps}", (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    if isMouseDrag:
        cv2.rectangle(frame, rectStartPos, (mousePosition[0], mousePosition[1]), (0, 255, 0), 2)
    else:
        if points:
            # Draw frame lines
            cv2.line(frame, points[0], points[1], (0, 255, 0), 2)
            cv2.line(frame, points[1], points[2], (0, 255, 0), 2)
            cv2.line(frame, points[2], points[3], (0, 255, 0), 2)
            cv2.line(frame, points[3], points[0], (0, 255, 0), 2)

            # Draw frame lines
            for point in points:
                cv2.circle(frame, point, 5, (255, 0, 0), -1)

    cv2.imshow("Crossroad", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()