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
        self.graph = graph
        self.start = start
        self.target = target
        self.queue = PriorityQueue()
        self.visited = []
        self.target_not_found = True

    @staticmethod
    def heuristic(start, target):
        (x1, y1) = start
        (x2, y2) = target
        return abs(x1 - x2) + abs(y1 - y2)

    def step(self):
        self.queue.put(self.start, 0)
        cost_so_far = {self.start: 0}

        while not self.queue.empty():
            current = self.queue.get()

            if current == self.target:
                break

            for neighbor in self.graph.get_connected_nodes(current):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(self.target, neighbor)
                    self.queue.put(neighbor, priority)
                    yield neighbor

    def can_execute(self):
        return self.start is not None and self.target is not None
