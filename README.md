# GraphAlgos
**GraphAlgos** is a small python application that provides a framework for visualizing graph search algorithms using curses (pygcurse library).

<img alt="Recording of A*" src="https://user-images.githubusercontent.com/9216979/60671655-e01dfc80-9e73-11e9-8be7-7ac5507aef8d.gif" width="500">

## Implemented algorithms
* BFS
* DFS
* A*

## (Recommended) Setup
The dependencies are only installed in the venv folder, so once you do not need them anymore it can safely be deleted.

1. Set up a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment:
```
source venv/Scripts/activate
```

3. Install required packages:
```
pip install -r requirements.txt
```

4. Start example:
```
python example.py
```

5. The virtual environment can be deactivated with:
```
deactivate
```

## Usage
1. First left click will create a starting point.
2. Second left click will create a target point.
3. Afterwards, left clicking anywhere  will create an obstacle (positions that cannot be traversed).
Dragging while holding left click down will continuously create obstacles.
4. Press Enter to start the graph search.

## Packages
* [Pygcurse](http://inventwithpython.com/pygcurse/) - Curses emulation library.
* Pygcurse uses [Pygame](https://www.pygame.org) - Game engine written in Python.

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
