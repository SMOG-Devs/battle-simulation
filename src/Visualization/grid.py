import collections
import pickle
from abc import ABC
import os
from itertools import product

from pygame import Color


class Grid(ABC):
    """
    Grid abstract class for pygame visualization
    :argument cell_count: size of grid (horizontal and vertical)
    """

    def __init__(self, cell_count):
        self.cell_count = cell_count
        self.grid = []

    def step(self):
        """
        Loads next frame
        :return: nothing
        """
        pass

    def to_start(self):
        """
        Loads first frame
        :return: nothing
        """
        pass

    def get_grid(self):
        """
        Get current grid as list of lists of ints
        :return: list of lists of ints
        """
        pass

    def get_colors(self):
        """
        Get colors coded as ints
        :return: dict(int, Color)
        """
        pass


class GridPickle(Grid):

    def __init__(self, cell_count, filename):
        super().__init__(cell_count)
        self.t = 0  # current frame index
        with open(filename, 'rb') as file:
            self.logs = pickle.load(file)
        self._load_grid()
        # print(self.logs[0])
        # print("")
        # print("")
        # print("")
        # print(self.logs[1])

    def step(self):
        if self.t < len(self.logs) - 1:
            self.t += 1
        else:
            self.t = 0
        self._load_grid()

    def prev_step(self):
        if self.t >= 1:
            self.t -= 1
        else:
            self.t = len(self.logs) - 1
        self._load_grid()

    def to_start(self):
        self.t = 0
        self._load_grid()

    def get_grid(self):
        return self.grid

    def get_colors(self):
        return {0: Color(255, 255, 255), 1: Color(0, 0, 0), 2: Color(0, 0, 255), 3: Color(255, 0, 0)}

    def _load_grid(self):
        # init empty grid
        self.grid = []
        for row in range(self.cell_count):
            self.grid.append([])
            for column in range(self.cell_count):
                self.grid[row].append(0)

        # load units to their positions
        for unit_info in self.logs[self.t]:
            x = unit_info[4][0]  # pos x
            y = unit_info[4][1]  # pos y
            color = 0
            # TODO: more options for different states of units
            if unit_info[3] <= 0:  # hp
                color = 1
            else:
                if unit_info[1] == 'Team.BLUE':  # team
                    color = 2
                else:
                    color = 3
            self.grid[x][y] = color

    def get_description(self, x: int, y: int):
        descr = ""
        for unit in self.logs[self.t]:
            if unit[4] == (x, y):
                descr += str(unit[0]) + '\n' + str(unit[1]) + '\nStatus: ' + str(unit[2]) + '\nHP: ' + str(
                    unit[3]) + '\nPosition: ' + str(unit[4])
        return descr


class Terrain:
    def __init__(self, x: int, y: int):  # x y: size of the grid
        self.x = x
        self.y = y
        self.grid = []
        for i in range(self.x):
            self.grid.append([])
            for j in range(self.y):
                self.grid[i].append(0)
        for i in range(self.x):
            for j in range(self.y):
                if abs(i - j) < 3:  # river in the middle: weight 10
                    self.grid[i][j] = 10
                elif i > j + 10:  # mountains at the top/right: weight 3
                    self.grid[i][j] = 3
                else:  # grass in bot/left: weight 1
                    self.grid[i][j] = 1

                    # three obstacles in the middle of the grass
                    if (i - 10) ** 2 + (j - 20) ** 2 < 10 ** 2:
                        self.grid[i][j] = 3
                    if (i - 40) ** 2 + (j - 30) ** 2 < 10 ** 2:
                        self.grid[i][j] = 3
                    if (i - 30) ** 2 + (j - 100) ** 2 < 10 ** 2:
                        self.grid[i][j] = 3

    def get_colors(self) -> {}:  # dict with colors for each weight
        return {1: Color(0, 200, 0), 3: Color(100, 100, 100), 10: Color(0, 0, 255)}

    def get_grid(self) -> [[]]:  # grid with weights
        return self.grid

    def __get_nodes(self):
        return [(i, j) for i, j in product(range(self.x), range(self.y))]

    def __get_neighbors(self, node):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= node[0] + i < self.x and 0 <= node[1] + j < self.y:
                    neighbours.append((node[0] + i, node[1] + j))
        return neighbours


    def shortest_path(self, start: (int, int), end: (int, int)) -> []:
        """
        Calculates the shortest path from start to end
        :param start: start position
        :param end: end position
        :return: list of positions
        """
        pass


# tests
# cur_path = os.path.dirname(__file__)
# print(cur_path)
# new_path = cur_path.replace('src\\Visualization', 'logs.plk')
# print(new_path)

# g = GridPickle(300, 'logs.plk')
