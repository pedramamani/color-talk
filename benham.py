import cv2
import numpy as np
import os
import pathlib

DIR = pathlib.Path(os.path.dirname(__file__))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / 'assets'


def rotate_image(image, angle):
    imageCenter = tuple(np.array(image.shape[1::-1]) / 2)
    rotationMatrix = cv2.getRotationMatrix2D(imageCenter, angle, 1.0)
    return cv2.warpAffine(image, rotationMatrix, image.shape[1::-1], flags=cv2.INTER_LINEAR)


if __name__ == '__main__':
    dim = 450
    step = 20
    image = cv2.imread(str(ASSETS_DIR / 'benham-disc.png'), cv2.IMREAD_GRAYSCALE)
    rotatedImages = np.zeros((360 // step, dim, dim), dtype='uint8')

    for index, angle in enumerate(np.arange(0, 360, step)):
        rotatedImages[index] = rotate_image(image, angle)

    index = 0
    while cv2.waitKey(1) != ord('q'):
        cv2.imshow('Illusion', rotatedImages[index])
        index = (index + 1) % len(rotatedImages)

