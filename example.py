from graphalgogui import GraphAlgoGUI
from graphalgos import *

graphalgo_dict = {
    'bfs': BFS,
    'dfs': DFS,
    'astar': AStar
}

gui = GraphAlgoGUI(AStar)
gui.create_gui()

gui.start()
