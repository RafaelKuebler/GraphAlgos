from abc import ABCMeta, abstractmethod, abstractproperty


class GraphAlgo:
    __metaclass__ = ABCMeta

    @abstractmethod
    def step(self):
        yield
