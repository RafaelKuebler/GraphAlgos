from .graphalgo import GraphAlgo
from collections import deque


class BFS(GraphAlgo):
    def __init__(self, graph, start=None, target=None):
        super(BFS, self).__init__(graph, start, target)
        self.queue = deque()

    def step(self):
        self.queue.append(self.start)
        self.cost_so_far[self.start] = 0

        while self.queue:
            current = self.queue.popleft()

            for neighbor in self.graph.get_connected_nodes(current):
                if neighbor == self.target:
                    self.parent[self.target] = current
                    yield

                if neighbor not in self.cost_so_far:
                    self.cost_so_far[neighbor] = self.cost_so_far[current] + 1
                    self.queue.append(neighbor)
                    self.parent[neighbor] = current
                    print(self.start, current, neighbor)
                    yield (neighbor, self.cost_so_far[neighbor])
        yield
