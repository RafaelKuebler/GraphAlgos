from graphalgo import GraphAlgo


class DFS(GraphAlgo):
    def __init__(self, graph, start=None, target=None):
        self.graph = graph
        self.start = start
        self.target = target
        self.stack = []
        self.visited = []
        self.target_not_found = True
        self.running = False

    def step(self):
        self.stack.append(self.start)

        while self.stack and self.target_not_found:
            current = self.stack.pop()
            if current not in self.visited:
                self.visited.append(current)
                for neighbor in self.graph.get_connected_nodes(current):
                    if neighbor == self.target:
                        print("found position!")
                        self.target_not_found = False
                        break
                    if neighbor not in self.visited and not self.graph.is_obstacle(neighbor):
                        self.stack.append(neighbor)
                        yield neighbor
        yield

    def can_execute(self):
        return (self.start is not None) and (self.target is not None) and self.running
