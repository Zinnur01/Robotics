import cv2

videoPath: str = "../../../Resources/crossroad.mp4"
cap = cv2.VideoCapture(videoPath)

pause = False
recording = False
waitText = False
annotations = []

startFrame: int = 0
annotationText: str = ""

while cap.isOpened():
    if not pause:
        success, frame = cap.read()

        if not success:
            break

        if recording:
            cv2.circle(frame, (40, 40), 20, (0, 0, 255), -1)

        cv2.imshow("Image", frame)

    key = cv2.waitKey(5) & 0xFF
    if key == 115:
        print(key)
        if not recording:
            print("Start")
            recording = True
            startFrame = cap.get(1)
        else:
            print("End")
            annotationText = input("Enter annotation text: ")
            annotations.append((startFrame, cap.get(1), annotationText))
            recording = False
    if key == ord('q'):
        break
    if key == 32:
        print("Pause")
        pause = not pause


if recording:
    annotationText = input("Enter annotation text: ")
    annotations.append((startFrame, cap.get(7), annotationText))
    recording = False

print("End!!!")


cap = cv2.VideoCapture(videoPath)
frame_size = int(cap.get(3)), int(cap.get(4))
saveVideo = cv2.VideoWriter("Outputs/saved_video.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60, frame_size)

currentAnnotation = None

while cap.isOpened():
    success, frame = cap.read()
    frameIndex = cap.get(1)

    if not success:
        break

    print(frameIndex)

    for a in annotations:
        if a[1] == frameIndex:
            currentAnnotation = None
        if a[0] == frameIndex:
            currentAnnotation = a

    if currentAnnotation:
        cv2.putText(frame, currentAnnotation[2], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

    saveVideo.write(frame)


cap.release()
saveVideo.release()
cv2.destroyAllWindows()