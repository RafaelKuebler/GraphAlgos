from abc import ABCMeta, abstractmethod


class Graph:
    __metaclass__ = ABCMeta

    @abstractproperty
    def nodes(self):
        pass

    @abstractproperty
    def edges(self):
        pass

    @abstractmethod
    def get_connected_nodes(self, node):
        pass
