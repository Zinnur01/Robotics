import cv2
import numpy as np
import random

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

img = cv2.imread('../../../Resources/lena.png', 0)
img = cv2.resize(img, None, fx=0.25, fy=0.25)
# img = sp_noise(img, 0.1)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitudeSpectrum = np.log(np.abs(fshift))
magnitudeSpectrum /= magnitudeSpectrum.max()

crow,ccol = img.shape[0]//2, img.shape[1]//2
fshift[crow-30:crow+31, ccol-30:ccol+31] = 0
f_ishift = np.fft.ifftshift(fshift)
imgBack = np.fft.ifft2(f_ishift)
imgBack = np.real(imgBack)
imgBack /= imgBack.max()

cv2.imshow("Input Image", img)
cv2.imshow("Magnitude Spectrum", magnitudeSpectrum)
cv2.imshow("Image after HPF", imgBack)
cv2.waitKey()