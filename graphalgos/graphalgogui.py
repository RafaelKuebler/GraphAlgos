import pygame
import pygcurse
from pygame.locals import *
from win32api import GetSystemMetrics
from graph.twodmap import TwoDMap
from graphalgos.bfs import BFS
from graphalgos.dfs import DFS


class GraphAlgoGUI:
    def __init__(self, size_x=50, size_y=30, fullscreen=False):
        cell_width, cell_height = self._test_cell_size()

        if size_x == "max":
            self._size_x = int(GetSystemMetrics(0) / cell_width)
        else:
            self._size_x = size_x
        if size_y == "max":
            self._size_y = int(GetSystemMetrics(1) / cell_height)
        else:
            self._size_y = size_y

        self._fullscreen = fullscreen
        self._window = None
        self._graph = None
        self._graphalgo = None
        self._obstacle_char = '#'
        self._start_char = 'A'
        self._target_char = 'B'
        self._visited_char = '.'

    def create_gui(self):
        self._window = pygcurse.PygcurseWindow(self._size_x, self._size_y, "GraphAlgo", fullscreen=self._fullscreen)

    def set_graph_and_algo(self, graph, graphalgo):
        self._graph = {
            'twodmap': TwoDMap(self._size_x, self._size_y)
        }[graph]

        self._graphalgo = {
            'bfs': BFS(self._graph),
            'dfs': DFS(self._graph)
        }[graphalgo]

    def set_chars(self, start, target, obstacle, visited):
        self._start_char = start
        self._target_char = target
        self._obstacle_char = obstacle
        self._visited_char = visited

    @staticmethod
    def _test_cell_size():
        test = pygcurse.PygcurseWindow(1, 1)
        width = test.cellwidth
        height = test.cellheight
        pygame.quit()
        return width, height

    def click_at(self, cell):
        if self._graphalgo.start is None:
            print("saved starting cell")
            self.mark_as_start(cell)
        elif self._graphalgo.target is None:
            print("saved target cell")
            self.mark_as_target(cell)

    def mark_as_start(self, cell):
        self._graphalgo.start = cell
        self._window.putchar(self._start_char, cell[0], cell[1])

    def mark_as_target(self, cell):
        self._graphalgo.target = cell
        self._window.putchar(self._target_char, cell[0], cell[1])

    def mark_as_obstacle(self, cell):
        self._window.putchar(self._obstacle_char, cell[0], cell[1])
        self._graph.mark_as_obstacle(cell)

    def mark_as_visited(self, cell):
        self._window.putchar(self._visited_char, cell[0], cell[1])
        self._graph.mark_as_obstacle(cell)

    def place_obstacle(self, cell):
        if self._graphalgo.start != cell and self._graphalgo.target != cell:
            self.mark_as_obstacle(cell)

    def start(self):
        self._mainloop()

    def _mainloop(self):
        mouse_down = False
        step_generator = None

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    return
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self._graphalgo.running = True
                    step_generator = self._graphalgo.step()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_down = True
                    self.click_at(self._window.getcoordinatesatpixel(event.pos))
                elif event.type == MOUSEBUTTONUP:
                    mouse_down = False
                elif mouse_down:
                    self.place_obstacle(self._window.getcoordinatesatpixel(event.pos))

            if self._graphalgo.can_execute:
                try:
                    visited = next(step_generator)
                    if self._graphalgo.start != visited and self._graphalgo.target != visited:
                        self.mark_as_visited(visited)
                except (StopIteration, TypeError):
                    pass
