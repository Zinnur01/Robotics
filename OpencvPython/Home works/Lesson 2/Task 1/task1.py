import cv2
import math

img = cv2.imread("../../../Resources/map.png")
mapRatio: float = 2.2125

helpText: str
pathDrawing: bool = True
path: list[tuple[int, int]] = []
pathLength: float = 0


def distance(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


def onMouse(event, x, y, flags, param):
    global path

    if event == cv2.EVENT_LBUTTONUP:
        if pathDrawing:
            path.append((x, y))


cv2.imshow("Map", img)
cv2.setMouseCallback("Map", onMouse)


while True:
    img = cv2.imread("../../../Resources/map.png")

    if path:
        for i in range(0, len(path) - 1):
            cv2.line(img, path[i], path[i+1], (255, 0, 0), 2)

        cv2.circle(img, path[0], 10, (0, 255, 0), -1)
        if not pathDrawing:
            cv2.circle(img, path[len(path)-1], 10, (0, 0, 255), -1)

    # Calculate help text
    if pathDrawing:
        helpText = "Draw a path and press the Space."
    else:
        helpText = f"Path length = {pathLength} meters."

    cv2.putText(img, helpText, (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Map", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == 32:
        if pathDrawing:
            pathDrawing = False
            for i in range(0, len(path) - 1):
                pathLength += distance(path[i], path[i+1])

            pathLength *= mapRatio
            pathLength = int(pathLength)

cv2.destroyAllWindows()