import sys
import pygame
import pygcurse
from pygame.locals import *
from win32api import GetSystemMetrics
from graph.twodmap import *
from graphalgos.bfs import BFS


def test_cell_size():
    test = pygcurse.PygcurseWindow(1, 1)
    width = test.cellwidth
    height = test.cellheight
    pygame.quit()
    return width, height


def click(cell):
    global start
    global target
    global two_d_map

    if start is None:
        print("saved starting cell")
        start = cell
        win.putchar('A', cell[0], cell[1])
    elif target is None:
        print("saved target cell")
        target = cell
        win.putchar('B', cell[0], cell[1])


def place_obstacle(cell):
    global start
    global target
    global two_d_map

    if start != cell and target != cell:
        win.putchar('#', cell[0], cell[1])
        two_d_map.mark_as_obstacle(cell)


def mainloop():
    global bfs
    global bfs_step
    global two_d_map
    global mouse_down
    global start
    global target
    global cooldown
    global last

    while True:
        for event in pygame.event.get():
            # input
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_RETURN:
                if start is not None and target is not None:
                    bfs = BFS(two_d_map, start, target)
                    bfs_step = bfs.step()
            if event.type == MOUSEBUTTONDOWN:
                mouse_down = True
                click(win.getcoordinatesatpixel(event.pos))
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
            elif mouse_down:
                place_obstacle(win.getcoordinatesatpixel(event.pos))
        # bfs.step()
        now = pygame.time.get_ticks()
        if bfs is not None and now - last >= cooldown:
            last = now
            try:
                marked = next(bfs_step)
                marked_x, marked_y = marked
                if start != marked and target != marked:
                    win.write("+", marked_x, marked_y)
            except (StopIteration, TypeError):
                pass
        # win.update()


# variables
start = None
target = None
mouse_down = False
bfs = None
bfs_step = None
cooldown = 0
last = 0

# calculate window size
cell_width, cell_height = test_cell_size()
'''
size_x = int(GetSystemMetrics(0) / cell_width)
size_y = int(GetSystemMetrics(1) / cell_height)
'''
size_x = 50
size_y = 30

# create window
win = pygcurse.PygcurseWindow(size_x, size_y, fullscreen=False)
# win.autoupdate = False

# create map
two_d_map = TwoDMap(size_x, size_y)
bfs = None

mainloop()
