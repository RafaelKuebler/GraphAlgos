import pygame
import pygcurse
from pygame.locals import *
from win32api import GetSystemMetrics
from graph.twodmap import TwoDMap


class GuiState(object):
    def __init__(self, gui):
        self.gui = gui

    def update(self, events):
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit(0)


class SetStartState(GuiState):
    def __init__(self, gui):
        super(SetStartState, self).__init__(gui)

    def update(self, events):
        super(SetStartState, self).update(events)

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                cell = self.gui.getcoordinatesatpixel(event.pos)
                self.gui.mark_as_start(cell)
                return SetTargetState(self.gui)
        return self


class SetTargetState(GuiState):
    def __init__(self, gui):
        super(SetTargetState, self).__init__(gui)

    def update(self, events):
        super(SetTargetState, self).update(events)

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                cell = self.gui.getcoordinatesatpixel(event.pos)
                self.gui.mark_as_target(cell)
                return SetObstaclesState(self.gui)
        return self


class SetObstaclesState(GuiState):
    def __init__(self, gui):
        super(SetObstaclesState, self).__init__(gui)
        self.mouse_down = False

    def update(self, events):
        super(SetObstaclesState, self).update(events)

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.mouse_down = True
                cell = self.gui.getcoordinatesatpixel(event.pos)
                self.gui.place_obstacle(cell)
            elif event.type == MOUSEBUTTONUP:
                self.mouse_down = False
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return RunAlgoState(self.gui)
            elif self.mouse_down:
                cell = self.gui.getcoordinatesatpixel(event.pos)
                self.gui.place_obstacle(cell)
        return self


class RunAlgoState(GuiState):
    def __init__(self, gui):
        super(RunAlgoState, self).__init__(gui)
        self.step_gen = self.gui.step()

    def update(self, events):
        super(RunAlgoState, self).update(events)
        visited = next(self.step_gen)
        if visited is None:
            return IdleState(self.gui)

        self.gui.mark_as_visited(visited)
        return self


class IdleState(GuiState):
    def __init__(self, gui):
        super(IdleState, self).__init__(gui)

    def update(self, events):
        super(IdleState, self).update(events)

        for event in events:
            if event.type == KEYDOWN and event.key == K_RETURN or event.type == MOUSEBUTTONDOWN:
                self.gui.reset()
                return SetStartState(self.gui)
        return self


class GraphAlgoGUI:
    def __init__(self, graphalgo, size_x=50, size_y=30):
        cell_width, cell_height = self._test_cell_size()

        if size_x == "max":
            self._size_x = int(GetSystemMetrics(0) / cell_width)
        else:
            self._size_x = size_x
        if size_y == "max":
            self._size_y = int(GetSystemMetrics(1) / cell_height)
        else:
            self._size_y = size_y

        self._graph = TwoDMap(self._size_x, self._size_y)
        self._algoconstr = graphalgo
        self._graphalgo = self._algoconstr(self._graph)

        self._window = None
        self._obstacle_char = '#'
        self._start_char = 'A'
        self._target_char = 'B'
        self._visited_char = '.'
        self.state = SetStartState(self)

    def create_gui(self, fullscreen=False):
        self._window = pygcurse.PygcurseWindow(self._size_x, self._size_y, "GraphAlgo", fullscreen=fullscreen)

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

    def step(self):
        return self._graphalgo.step()

    def reset(self):
        self._window.setscreencolors(None, 'black', clear=True)
        self._graph = TwoDMap(self._size_x, self._size_y)
        self._graphalgo = self._algoconstr(self._graph)

    def getcoordinatesatpixel(self, pos):
        return self._window.getcoordinatesatpixel(pos)

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
        if cell != self._graphalgo.start and cell != self._graphalgo.target:
            self.mark_as_obstacle(cell)

    def start(self):
        self._mainloop()

    def _mainloop(self):
        while True:
            self.state = self.state.update(pygame.event.get())
