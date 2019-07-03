from .graphalgo import GraphAlgo
from collections import deque


class BFS(GraphAlgo):
    def __init__(self, graph, start=None, target=None):
        self.graph = graph
        self.start = start
        self.target = target
        self.queue = deque()
        self.visited = []

    def step(self):
        self.queue.append(self.start)

        while self.queue:
            current = self.queue.popleft()
            # print("current: {}".format(current))
            for neighbor in self.graph.get_connected_nodes(current):
                if neighbor == self.target:
                    yield
                if neighbor not in self.visited:
                    self.visited.append(neighbor)
                    self.queue.append(neighbor)
                    yield neighbor
