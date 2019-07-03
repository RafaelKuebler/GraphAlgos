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
        self.gui.show_instructions()
        super(SetStartState, self).update(events)

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.gui.hide_instructions()
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
        result = next(self.step_gen)

        if result is None:
            self.gui.show_shortest_path()
            return IdleState(self.gui)

        self.gui.mark_as_visited(*result)
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
        self._path_char = '+'
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

    def mark_as_path(self, cell):
        self._graphalgo.target = cell
        self._window.putchar(self._path_char, cell[0], cell[1], fgcolor='white')

    def mark_as_obstacle(self, cell):
        self._window.putchar(self._obstacle_char, cell[0], cell[1])
        self._graph.mark_as_obstacle(cell)

    def mark_as_visited(self, cell, distance):
        r1, g1, b1 = (0, 255, 0)  # green
        r2, g2, b2 = (255, 0, 0)  # reds
        t = distance/self._size_x

        r = int(r1*(1-t)+r2*t)
        g = int(g1*(1-t)+g2*t)
        b = int(b1*(1-t)+b2*t)
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))

        self._window.putchar(self._visited_char, cell[0], cell[1], fgcolor=(r, g, b))
        self._graph.mark_as_obstacle(cell)

    def show_instructions(self):
        self._window.write('Click to set start and target.', x=2, y=5, fgcolor='white')
        self._window.write('Afterwards, click or drag to set obstacles.', x=2, y=7, fgcolor='white')
        self._window.write('When ready, press Enter to start the search!', x=2, y=9, fgcolor='white')

    def hide_instructions(self):
        self._window.fill(' ', region=(0, 0, self._size_x, 11))

    def show_not_found_message(self):
        self._window.write('Target is not reachable!', x=5, y=5, fgcolor='white')

    def place_obstacle(self, cell):
        if cell != self._graphalgo.start and cell != self._graphalgo.target:
            self.mark_as_obstacle(cell)

    def show_shortest_path(self):
        path = self._graphalgo.shortest_path()
        if path is None:
            self.show_not_found_message()
            return

        for cell in path:
            self.mark_as_path(cell)

    def start(self):
        self._mainloop()

    def _mainloop(self):
        while True:
            self.state = self.state.update(pygame.event.get())
