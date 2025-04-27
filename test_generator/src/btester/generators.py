from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional

import numpy as np


class AbstractGenerator(ABC):
    @abstractmethod
    def generate(self, size: int) -> list[Any]:
        raise NotImplementedError


class Integers(AbstractGenerator):
    def __init__(self, low: int = 0, high: int = 100, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed=seed)
        self.low = low
        self.high = high

    def generate(self, size: int = 100):
        return self.rng.integers(low=self.low, high=self.high, size=size)
