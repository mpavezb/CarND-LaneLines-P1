import os
import matplotlib.image as mpimg

from src.parameters import *
from src.helpers import *
from src.pipeline import *


def Task1():
    image = mpimg.imread("test_images/solidWhiteRight.jpg")
    size_x = image.shape[1]
    size_y = image.shape[0]
    print("This image is:", type(image), "with dimensions:", image.shape)

    cnt = 1
    parameters = Parameters(size_x, size_y)
    parameters.debug = True
    for filename in os.listdir("test_images/"):
        image = mpimg.imread("test_images/" + filename)
        [gray, blurred, cannied, masked, houghed, weighted] = process(image, parameters)
        draw(image, gray, blurred, cannied, masked, houghed, weighted, parameters, cnt)
        cv2.imwrite(
            "test_images_output/" + filename, cv2.cvtColor(weighted, cv2.COLOR_RGB2BGR)
        )
        cnt += 1

    print("Completed.")
