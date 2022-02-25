import cv2
import numpy as np

# Image acquisition and resizing
img = cv2.imread("../../../Resources/lena.png")
img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)

pre_crop_img = img.copy()
grid_size = (3, 3)

# Size of one part
frameWidth = int(img.shape[0]/grid_size[0])
frameHeight = int(img.shape[1]/grid_size[1])

# Draw the cut lines
for x in range(0, grid_size[0]):
    cv2.line(pre_crop_img, (x * frameWidth, 0), (x * frameWidth, img.shape[1]), (0, 0, 0), 1)
for y in range(0, grid_size[1]):
    cv2.line(pre_crop_img, (0, y * frameHeight), (img.shape[0], y * frameHeight), (0, 0, 0), 1)

# Show a pre-cut image
cv2.imshow("Pre Crop Img", pre_crop_img)

cv2.waitKey()
cv2.destroyAllWindows()

# Cutting and saving an image
for x in range(0, grid_size[0]):
    for y in range(0, grid_size[1]):
        cropped_image = img[int(frameWidth*x):int(frameWidth*(x+1)), int(frameHeight*y):int(frameHeight*(y+1))]
        cv2.imwrite(f"Outputs/Image ({x}, {y}).jpg", cropped_image)