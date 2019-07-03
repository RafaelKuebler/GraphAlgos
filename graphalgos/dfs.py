from .graphalgo import GraphAlgo


class DFS(GraphAlgo):
    def __init__(self, graph, start=None, target=None):
        super(DFS, self).__init__(graph, start, target)
        self.stack = []

    def step(self):
        self.stack.append(self.start)
        self.cost_so_far[self.start] = 0

        while self.stack:
            current = self.stack.pop()

            for neighbor in self.graph.get_connected_nodes(current):
                if neighbor == self.target:
                    self.parent[self.target] = current
                    yield

                if neighbor not in self.cost_so_far:
                    self.cost_so_far[neighbor] = self.cost_so_far[current] + 1
                    self.stack.append(neighbor)
                    self.parent[neighbor] = current
                    yield (neighbor, self.cost_so_far[neighbor])
        yield
