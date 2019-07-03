from abc import ABCMeta, abstractmethod


class GraphAlgo:
    __metaclass__ = ABCMeta

    def __init__(self, graph, start, target):
        self.graph = graph
        self.start = start
        self.target = target
        self.parent = {}
        self.cost_so_far = {}

    @abstractmethod
    def step(self):
        yield

    @abstractmethod
    def can_execute(self):
        return False

    @abstractmethod
    def shortest_path(self):
        if self.target not in self.parent:
            return None

        path = []
        current = self.target
        while self.parent[current] != self.start:
            path.append(self.parent[current])
            current = self.parent[current]

        return path
