from abc import ABCMeta, abstractmethod


class GraphAlgo:
    __metaclass__ = ABCMeta

    @abstractmethod
    def step(self):
        yield

    @abstractmethod
    def can_execute(self):
        return False
