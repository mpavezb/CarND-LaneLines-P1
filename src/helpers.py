import math
import cv2
import numpy as np


def grayscale(img):
    """Applies the Grayscale transform"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """Applies an image mask."""
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def get_slope(line):
    for x1, y1, x2, y2 in line:
        if (x2 - x1) < 0.01:
            return 9999
        return (y2 - y1) / (x2 - x1)


def get_offset(line):
    for x1, y1, x2, y2 in line:
        slope = get_slope(line)
        return y2 - slope * x2


def merge_lines(lines, parameters, slope_history, offset_history):
    b = parameters.y_bottom
    t = parameters.y_top
    n_lines = len(lines)

    slope = 0
    offset = 0
    for line in lines:
        slope += get_slope(line) / n_lines
        offset += get_offset(line) / n_lines

    # -------------------------------------------
    # moving average
    history_size = parameters.history_size
    slope_history.append(slope)
    offset_history.append(offset)
    if len(slope_history) > history_size:
        slope_history.pop(0)
        offset_history.pop(0)
    avg_slope = sum(slope_history) / len(slope_history)
    avg_offset = sum(offset_history) / len(offset_history)
    # --------------------------------------------

    x1 = (b - avg_offset) / avg_slope
    x2 = (t - avg_offset) / avg_slope
    return np.array([[x1, b, x2, t]], dtype=np.int32)


def extract_lr_lines(lines, parameters):
    left_candidates = []
    right_candidates = []
    for line in lines:
        if get_slope(line) < 0:
            left_candidates.append(line)
        else:
            right_candidates.append(line)

    left_line = merge_lines(
        left_candidates, parameters, parameters.l_slopes, parameters.l_offsets
    )
    right_line = merge_lines(
        right_candidates, parameters, parameters.r_slopes, parameters.r_offsets
    )
    return [left_line, right_line]


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap, parameters):
    """Returns an image with hough lines drawn."""
    lines = cv2.HoughLinesP(
        img,
        rho,
        theta,
        threshold,
        np.array([]),
        minLineLength=min_line_len,
        maxLineGap=max_line_gap,
    )
    merged_lines = extract_lr_lines(lines, parameters)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, merged_lines, thickness=10)
    return line_img


def weighted_img(img, initial_img, α=0.8, β=1.0, γ=0.0):
    """Linear merge of 2 images."""
    return cv2.addWeighted(initial_img, α, img, β, γ)
