import cv2
import random
import numpy as np

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range (0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)

                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)

            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def spnoise(image, amount):
    out = np.copy(image)

    # Salt mode
    num_salt = np.ceil(amount * image.size * .5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    out[coords] = 255

    # Pepper mode
    num_pepper = np.ceil(amount * image.size * (1. - .5))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    out[coords] = 0
    return out

def sp_noise(image, prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def onChange(value):
    img = cv2.imread("../../../Resources/lena.png")
    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # spimage = spnoise(img, value/200)
    spimage = sp_noise(img, value/200)
    median3 = cv2.medianBlur(spimage, 3)
    median5 = cv2.medianBlur(spimage, 5)
    median7 = cv2.medianBlur(spimage, 7)
    median9 = cv2.medianBlur(spimage, 9)
    median11 = cv2.medianBlur(spimage, 11)
    median13 = cv2.medianBlur(spimage, 13)

    img = cv2.putText(img, "Original", (20, 40), 1, 2, (0, 255, 0), 2)
    spimage = cv2.putText(spimage, "Salt&Pepper", (20, 40), 1, 2, (0, 255, 0), 2)
    median3 = cv2.putText(median3, "3", (20, 40), 1, 2, (0, 255, 0), 2)
    median5 = cv2.putText(median5, "5", (20, 40), 1, 2, (0, 255, 0), 2)
    median7 = cv2.putText(median7, "7", (20, 40), 1, 2, (0, 255, 0), 2)
    median9 = cv2.putText(median9, "9", (20, 40), 1, 2, (0, 255, 0), 2)
    median11 = cv2.putText(median11, "11", (20, 40), 1, 2, (0, 255, 0), 2)
    median13 = cv2.putText(median13, "13", (20, 40), 1, 2, (0, 255, 0), 2)

    cv2.imshow("Image", stackImages(0.75, ([img, median3, median5, median7], [spimage, median9, median11, median13])))

cv2.namedWindow("Tool")
cv2.createTrackbar("Amount", "Tool", 0, 100, onChange)

onChange(50)

cv2.waitKey()