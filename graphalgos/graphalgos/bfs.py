from graphalgo import GraphAlgo
from collections import deque


class BFS(GraphAlgo):
    def __init__(self, graph, start_pos, target_pos):
        self.graph = graph
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.queue = deque([self.start_pos])
        self.visited = []
        self.target_not_found = True

    def step(self):
        while self.queue and self.target_not_found:
            current = self.queue.popleft()
            # print("current: {}".format(current))
            for neighbor in self.graph.get_connected_nodes(current):
                if neighbor == self.target_pos:
                    print("found position!")
                    self.target_not_found = False
                    break
                if neighbor not in self.visited and not self.graph.is_obstacle(neighbor):
                    self.visited.append(neighbor)
                    self.queue.append(neighbor)
                    yield neighbor
        yield
