import numpy as np


def compute_mean(x):
    return np.mean(x)


def compute_elementwise_sum(x, y):
    assert len(x) == len(y)
    return np.sum([x, y], axis=0)
