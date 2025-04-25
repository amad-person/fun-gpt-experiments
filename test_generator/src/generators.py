import numpy as np


class Integers:
    def __init__(self, low=0, high=100, seed=None):
        self.rng = np.random.default_rng(seed=seed)
        self.low = low
        self.high = high

    def generate(self, size=100):
        return self.rng.integers(low=self.low, high=self.high, size=size)
