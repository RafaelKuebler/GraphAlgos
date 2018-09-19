from .graphalgo import GraphAlgo
from collections import deque


class BFS(GraphAlgo):
    def __init__(self, graph, start=None, target=None):
        self.graph = graph
        self.start = start
        self.target = target
        self.queue = deque()
        self.visited = []
        self.target_not_found = True
        self.running = False

    def step(self):
        self.queue.append(self.start)

        while self.queue and self.target_not_found:
            current = self.queue.popleft()
            # print("current: {}".format(current))
            for neighbor in self.graph.get_connected_nodes(current):
                if neighbor == self.target:
                    print("found position!")
                    self.target_not_found = False
                    break
                if neighbor not in self.visited and not self.graph.is_obstacle(neighbor):
                    self.visited.append(neighbor)
                    self.queue.append(neighbor)
                    yield neighbor
        yield

    def can_execute(self):
        print("Can execute!")
        return (self.start is not None) and (self.target is not None) and self.running
