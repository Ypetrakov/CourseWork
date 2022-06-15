from abc import ABC, abstractmethod


class Algorithm(ABC):
    """ Abstract function class, function classes inherit from it """
    @abstractmethod
    def solve(self, a, c):
        pass
