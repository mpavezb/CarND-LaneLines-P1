import matplotlib.pyplot as plt
import numpy as np
import cv2

from src.helpers import *


def process(image, parameters):
    gray = grayscale(image)
    blurred = gaussian_blur(gray, 7)
    cannied = canny(blurred, 50, 150)
    masked = region_of_interest(cannied, parameters["vertices"])
    houghed = hough_lines(masked, 1, np.pi / 180, 30, 1, 10, parameters)
    weighted = weighted_img(houghed, image, α=0.8, β=1.0, γ=0.0)
    return gray, blurred, cannied, masked, houghed, weighted


def draw(image, gray, blurred, cannied, masked, houghed, weighted, parameters, cnt):
    if parameters["debug"]:
        mask = np.copy(blurred)
        cv2.polylines(mask, parameters["vertices"], True, (0, 0, 0), thickness=10)
        fig = plt.figure(cnt, figsize=(30, 10))
        fig.add_subplot(2, 3, 1)
        plt.imshow(image)
        fig.add_subplot(2, 3, 2)
        plt.imshow(mask, cmap="gray")
        fig.add_subplot(2, 3, 3)
        plt.imshow(cannied, cmap="gray")
        fig.add_subplot(2, 3, 4)
        plt.imshow(masked, cmap="gray")
        fig.add_subplot(2, 3, 5)
        plt.imshow(houghed, cmap="gray")
        fig.add_subplot(2, 3, 6)
        plt.imshow(weighted)
    else:
        fig = plt.figure(cnt, figsize=(40, 30))
        fig.add_subplot(1, 2, 1)
        plt.imshow(image)
        fig.add_subplot(1, 2, 2)
        plt.imshow(weighted)

    return weighted
