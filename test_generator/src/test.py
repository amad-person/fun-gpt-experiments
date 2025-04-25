from code import compute_elementwise_sum, compute_mean

import numpy as np

from decorators import test_data, test_settings
from generators import Integers


@test_settings(n_times=10)
@test_data(Integers())
def test_mean(x):
    expected = np.mean(x)
    actual = compute_mean(x)
    np.allclose(expected, actual)


@test_settings(n_times=10)
@test_data(Integers(), Integers(low=-10, high=10))
def test_elementwise_sum(x, y):
    expected = np.sum([x, y], axis=0)
    actual = compute_elementwise_sum(x, y)
    np.allclose(expected, actual)


if __name__ == "__main__":
    test_mean()
    test_elementwise_sum()
