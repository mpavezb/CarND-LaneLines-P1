import numpy as np

# Parameters
parameters = dict()
parameters["l_slopes"] = []
parameters["r_slopes"] = []
parameters["l_offsets"] = []
parameters["r_offsets"] = []


def reset_history(parameters):
    parameters["l_slopes"] = []
    parameters["r_slopes"] = []
    parameters["l_offsets"] = []
    parameters["r_offsets"] = []


class Parameters(object):
    pass
