from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional

import numpy as np
from faker import Faker


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


class FakerValues(AbstractGenerator):
    def __init__(
        self,
        faker_func_name: str = "first_name",
        faker_func_kwargs: dict = None,
        seed: Optional[int] = None,
    ):
        self.fake = Faker()
        self.faker_func_name = faker_func_name
        self.faker_func_kwargs = faker_func_kwargs or {}

        # validate faker_func_name
        try:
            getattr(self.fake, self.faker_func_name)
        except AttributeError:
            raise

        # validate faker_func_args
        try:
            func = getattr(self.fake, self.faker_func_name)
            func(**self.faker_func_kwargs)
        except TypeError:
            raise

        Faker.seed(seed)

    def generate(self, size: int = 100) -> list[Any]:
        faker_func = getattr(self.fake, self.faker_func_name)
        values = []
        for _ in range(size):
            values.append(faker_func(**self.faker_func_kwargs))
        return values
