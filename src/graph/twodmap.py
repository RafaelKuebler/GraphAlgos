class TwoDMap(Graph):

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self._edges = {}

        for y in range(0, size_y):
            for x in range(0, size_x):
                coords = x, y
                self._edges[coords] = []
                self.add_edge_to_neighbors(coords)

    def add_edge_to_neighbors(self, node):
        edges = self._edges[node1]
        x, y = node

        if x > 0:
            edges.append((x-1, y))
        if x < self.size_x - 1:
            edges.append((x + 1, y))
        if y > 0:
            edges.append((x, y - 1))
        if y < self.size_y - 1:
            edges.append((x, y + 1))

    def remove_edge(self, node1, node2):
        pass

    def get_connected_nodes(self, node):
        return self._edges[node]
