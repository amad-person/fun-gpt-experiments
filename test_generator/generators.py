import numpy as np


def generate_random_integers(low=0, high=1000, size=100):
    rng = np.random.default_rng()
    return rng.integers(low=low, high=high, size=size)
