from abc import ABC, abstractmethod


class Graph(ABC):
    @abstractmethod
    def add_edge_to_neighbors(self, node):
        pass

    @abstractmethod
    def remove_edge(self, node1, node2):
        pass

    @abstractmethod
    def mark_as_obstacle(self, node):
        pass

    @abstractmethod
    def is_obstacle(self, node):
        return False

    @abstractmethod
    def get_connected_nodes(self, node):
        return []
