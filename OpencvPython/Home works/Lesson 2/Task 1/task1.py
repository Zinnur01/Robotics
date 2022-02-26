import cv2
import math


img = cv2.imread("../../../Resources/map.png")

helpText: str
stage: int = 0

startPos: tuple[int, int] = None
endPos: tuple[int, int] = None
path: list[tuple[int, int]] = []
pathLength: float = 0


def distance(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


def onMouse(event, x, y, flags, param):
    global stage
    global startPos
    global endPos
    global path

    if event == cv2.EVENT_LBUTTONUP:
        if stage == 0:
            startPos = (x, y)
        elif stage == 1:
            endPos = (x, y)
        elif stage == 2:
            path.append((x, y))

        if stage < 2:
            stage += 1


cv2.imshow("Map", img)
cv2.setMouseCallback("Map", onMouse)


while True:
    img = cv2.imread("../../../Resources/map.png")

    if startPos:
        cv2.circle(img, startPos, 10, (0, 255, 0), -1)
    if endPos:
        cv2.circle(img, endPos, 10, (0, 0, 255), -1)
    if path:
        for i in range(0, len(path) - 1):
            cv2.line(img, path[i], path[i+1], (255, 0, 0), 2)

    # Calculate help text
    if stage == 0:
        helpText = "Select start."
    elif stage == 1:
        helpText = "Select end."
    elif stage == 2:
        helpText = "Draw a path and press the Space."
    elif stage == 3:
        helpText = f"Path length = {pathLength} meters."

    cv2.putText(img, helpText, (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Map", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == 32:
        if stage == 2:
            stage = 3
            for i in range(0, len(path) - 1):
                pathLength += distance(path[i], path[i+1])

            pathLength *= 2.2125
            pathLength = int(pathLength)

cv2.destroyAllWindows()