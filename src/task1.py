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

    parameters["history_size"] = 10
    parameters["debug"] = False
    parameters["y_bottom"] = size_y
    parameters["y_top"] = 320
    parameters["vertices"] = np.array(
        [
            [
                (100, size_y),
                (430, parameters["y_top"]),
                (540, parameters["y_top"]),
                (size_x - 50, size_y),
            ]
        ],
        dtype=np.int32,
    )

    cnt = 1
    parameters["debug"] = True
    for filename in os.listdir("test_images/"):
        reset_history(parameters)
        image = mpimg.imread("test_images/" + filename)
        [gray, blurred, cannied, masked, houghed, weighted] = process(image, parameters)
        draw(image, gray, blurred, cannied, masked, houghed, weighted, parameters, cnt)
        cv2.imwrite(
            "test_images_output/" + filename, cv2.cvtColor(weighted, cv2.COLOR_RGB2BGR)
        )
        cnt += 1

    print("Completed.")
