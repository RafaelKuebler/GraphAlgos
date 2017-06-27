from graphalgo import GraphAlgo


class DFS(GraphAlgo):
    def __init__(self, graph, start_pos, target_pos):
        self.graph = graph
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.stack = [self.start_pos]
        self.visited = []
        self.target_not_found = True

    def step(self):
        while self.stack and self.target_not_found:
            current = self.stack.pop()
            if current not in self.visited:
                self.visited.append(current)
                for neighbor in self.graph.get_connected_nodes(current):
                    if neighbor == self.target_pos:
                        print("found position!")
                        self.target_not_found = False
                        break
                    if neighbor not in self.visited and not self.graph.is_obstacle(neighbor):
                        self.stack.append(neighbor)
                        yield neighbor
        yield
