import sys
import pygame
import pygcurse
from pygame.locals import *
from win32api import GetSystemMetrics


def test_cell_size():
    test = pygcurse.PygcurseWindow(1, 1)
    width = test.cellwidth
    height = test.cellheight
    pygame.quit()

    return width, height


# calculate window size
cell_width, cell_height = test_cell_size()
size_x, size_y = int(GetSystemMetrics(0) / cell_width), int(GetSystemMetrics(1) / cell_height)

# create window
win = pygcurse.PygcurseWindow(size_x, size_y, fullscreen=True)

win.pygprint('What is your name?')
name = win.input()
win.write('Hello, ')
win.fgcolor = 'red'
win.write(name + '!\n')
win.colors = ('red', 'green')
win.pygprint('It is good to meet you!')

while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
