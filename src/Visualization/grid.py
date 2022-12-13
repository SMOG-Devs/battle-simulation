import pickle
from abc import ABC
import os
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

# tests
# cur_path = os.path.dirname(__file__)
# print(cur_path)
# new_path = cur_path.replace('src\\Visualization', 'logs.plk')
# print(new_path)

# g = GridPickle(300, 'logs.plk')
