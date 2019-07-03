from .graphalgo import GraphAlgo


class DFS(GraphAlgo):
    def __init__(self, graph, start=None, target=None):
        self.graph = graph
        self.start = start
        self.target = target
        self.stack = []
        self.visited = []

    def step(self):
        self.stack.append(self.start)

        while self.stack:
            current = self.stack.pop()
            if current not in self.visited:
                self.visited.append(current)
                for neighbor in self.graph.get_connected_nodes(current):
                    if neighbor == self.target:
                        yield
                    if neighbor not in self.visited:
                        self.stack.append(neighbor)
                        yield neighbor
