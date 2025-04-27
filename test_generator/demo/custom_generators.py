from typing import Optional

import numpy as np

from btester.generators import AbstractGenerator


class NormalFloats(AbstractGenerator):
    def __init__(
        self, loc: float = 0.0, scale: float = 1.0, seed: Optional[int] = None
    ):
        self.rng = np.random.default_rng(seed=seed)
        self.loc = loc
        self.scale = scale

    def generate(self, size: int = 100) -> list[float]:
        return self.rng.normal(loc=self.loc, scale=self.scale, size=size)
