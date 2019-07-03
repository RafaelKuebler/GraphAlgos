from .graphalgo import GraphAlgo
import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class AStar(GraphAlgo):
    def __init__(self, graph, start=None, target=None):
        super(AStar, self).__init__(graph, start, target)
        self.queue = PriorityQueue()

    @staticmethod
    def heuristic(start, target):
        (x1, y1) = start
        (x2, y2) = target
        return abs(x1 - x2) + abs(y1 - y2)

    def step(self):
        self.queue.put(self.start, 0)
        self.cost_so_far[self.start] = 0

        while not self.queue.empty():
            current = self.queue.get()

            for neighbor in self.graph.get_connected_nodes(current):
                if neighbor == self.target:
                    self.parent[self.target] = current
                    yield

                new_cost = self.cost_so_far[current] + 1
                if neighbor not in self.cost_so_far or new_cost < self.cost_so_far[neighbor]:
                    self.cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(self.target, neighbor)
                    self.queue.put(neighbor, priority)
                    self.parent[neighbor] = current
                    yield (neighbor, new_cost)
        yield
