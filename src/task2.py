# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip

import os
import matplotlib.image as mpimg

from src.parameters import *
from src.helpers import *
from src.pipeline import *


def Task2(sample_image, input_file, subclip=False, history_size=1):
    image = mpimg.imread(sample_image)
    size_x = image.shape[1]
    size_y = image.shape[0]
    print("Sample image is ", type(image), "with dimensions:", image.shape)

    parameters = Parameters(size_x, size_y)
    parameters.history_size = history_size
    print(parameters)

    def process_image(image):
        [_, _, _, _, _, weighted] = process(image, parameters)
        return weighted

    clip = None
    if subclip:
        clip = VideoFileClip(input_file).subclip(0, 5)
    else:
        clip = VideoFileClip(input_file)
    return clip.fl_image(process_image)
