from code import compute_mean

import numpy as np

from decorators import test_data, test_settings
from generators import generate_random_integers


@test_settings(n_times=10)
@test_data(generator_func=generate_random_integers)
def test_mean(x):
    expected = np.mean(x)
    actual = compute_mean(x)
    assert expected == actual


test_mean()
