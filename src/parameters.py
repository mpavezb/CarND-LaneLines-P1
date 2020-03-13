import numpy as np


class Parameters:
    def __init__(self, size_x, size_y):
        self.l_slopes = []
        self.r_slopes = []
        self.l_offsets = []
        self.r_offsets = []
        self.history_size = 10

        self.debug = False

        self.y_top = 320
        self.y_bottom = size_y
        self.vertices = np.array(
            [
                [
                    (100, size_y),
                    (430, self.y_top),
                    (540, self.y_top),
                    (size_x - 50, size_y),
                ]
            ],
            dtype=np.int32,
        )
