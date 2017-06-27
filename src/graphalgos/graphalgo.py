from abc import ABCMeta, abstractmethod


class GraphAlgo:
    __metaclass__ = ABCMeta

    @abstractproperty
    def graph(self):
        pass

    @abstractproperty
    def start_pos(self):
        pass

    @abstractproperty
    def target_pos(self):
        pass
