import pickle
from abc import ABC
import numpy as np
from pygame import Color
import time
from src.Model.World.Terrain import Terrain


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
                    if unit_info[0] == 'Reiter':  # type
                        color = 2
                    elif unit_info[0] == 'Hussar':
                        color = 3
                    elif unit_info[0] == 'Cannon':
                        color = 4
                    elif unit_info[0] == 'HorseArcher':
                        color = 5
                    elif unit_info[0] == 'Infantry':
                        color = 6
                else:
                    if unit_info[0] == 'Reiter':  # type
                        color = 7
                    elif unit_info[0] == 'Hussar':
                        color = 8
                    elif unit_info[0] == 'Cannon':
                        color = 9
                    elif unit_info[0] == 'HorseArcher':
                        color = 10
                    elif unit_info[0] == 'Infantry':
                        color = 11
            self.grid[x][y] = color

    def get_description(self, x: int, y: int):
        descr = ""
        for unit in self.logs[self.t]:
            if unit[4] == (x, y):
                descr += str(unit[0]) + '\n' + str(unit[1]) + '\nStatus: ' + str(unit[2]) + '\nHP: ' + str(
                    unit[3]) + '\nPosition: ' + str(unit[4])
        return descr





def pathfinding_benchmark(func_name):  # function name as string lmao
    def get_random_pos(min_limit, max_limit):
        return np.random.randint(min_limit, max_limit), np.random.randint(min_limit, max_limit)

    def test_pathfinding(size, num_tests):
        terrain = Terrain(size, size)
        shortest_path = getattr(terrain, func_name)
        start_time = time.time()
        biggest = 0
        for i in range(num_tests):
            start = get_random_pos(0, size)
            end = get_random_pos(0, size)
            elapsed = time.time()
            shortest_path(start, end)
            elapsed = time.time() - elapsed
            biggest = max(biggest, elapsed)
        total = time.time() - start_time
        print("Time for ", num_tests, " pathfinding tests: ", round(total, 5))
        print("Biggest time: ", round(biggest, 5))
        print("Average time: ", round(total / num_tests, 5))

    # set seed before every test for deterministic random numbers
    np.random.seed(0)
    # small 100x100 terrain, 100 tests
    test_pathfinding(100, 100)

    # medium 300x300 terrain, 30 tests
    np.random.seed(0)
    test_pathfinding(300, 30)

    # big 1000x1000 terrain, 5 tests
    np.random.seed(0)
    test_pathfinding(1000, 5)


if __name__ == '__main__':
    print("A*")
    pathfinding_benchmark("shortest_path")
    print("Djikstra")
    pathfinding_benchmark("_shortest_path_old")

    # g = Terrain(100, 100)
    # print(g.shortest_path((4, 10), (18, 29)))
