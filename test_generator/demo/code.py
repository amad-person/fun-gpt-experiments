import numpy as np


def compute_mean(x):
    return np.mean(x)


def compute_elementwise_sum(x, y):
    assert len(x) == len(y)
    return np.sum([x, y], axis=0)


def concat_elementwise_strings(x, y, delim=";"):
    assert len(x) == len(y)
    result = []
    for x_i, y_i in zip(x, y):
        result.append(x_i + delim + y_i)
    return result
