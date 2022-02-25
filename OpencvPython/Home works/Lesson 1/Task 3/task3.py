import cv2
import numpy as np

videoIn = cv2.VideoCapture(0)
frame_size = int(videoIn.get(3)), int(videoIn.get(4))
videoOut = cv2.VideoWriter("Outputs/saved_video.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, frame_size)

recording = False

while videoIn.isOpened():
    res, frame = videoIn.read()

    if res:
        if recording:
            videoOut.write(frame)
            frame = cv2.circle(frame, (20, 20), 10, (0, 0, 255), -1)

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('r'):
            if not recording:
                print("Recording")
                recording = True
        if key == ord('s'):
            if recording:
                print("Stop Recording")
                recording = False
    else:
        break

videoIn.release()
videoOut.release()

cv2.destroyAllWindows()




