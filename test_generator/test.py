from code import compute_mean

import numpy as np

from decorators import test_with
from generators import generate_random_integers


@test_with(generator_func=generate_random_integers, n_times=100)
def test_mean(x):
    expected = np.mean(x)
    actual = compute_mean(x)
    assert expected == actual


test_mean()
