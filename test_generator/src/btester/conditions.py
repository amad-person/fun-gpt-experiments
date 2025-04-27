from abc import ABC
from abc import abstractmethod

import numpy as np


class AbstractCondition(ABC):
    @abstractmethod
    def check(self, expected, actual):
        raise NotImplementedError


class AssertEqual(AbstractCondition):
    def check(self, expected, actual):
        assert expected == actual


class AssertAllClose(AbstractCondition):
    def check(self, expected, actual):
        np.allclose(expected, actual)
