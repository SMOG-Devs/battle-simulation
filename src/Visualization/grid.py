import pickle
from abc import ABC
from dataclasses import dataclass, field
from itertools import product
from queue import PriorityQueue
from typing import Tuple
import heapq
import numpy as np
from pygame import Color
import time


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

    def _shortest_path_old(self, start: (int, int), end: (int, int)) -> [(int, int)]:
        """
        Calculates the shortest path from start to end
        :param start: start position
        :param end: end position
        :return: list of positions
        """

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            item: Tuple[int, int] = field(compare=False)

        open = PriorityQueue()
        open.put(PrioritizedItem(0, start))
        dist = dict()
        dist[start] = 0
        prev = dict()
        prev[start] = None
        while not open.empty():
            current = open.get().item
            if current == end:
                path, u = [], end
                while prev[u]:
                    path.append(u)
                    u = prev[u]
                path.append(start)
                path.reverse()
                return path
            for node in self.__get_neighbors(current):
                node = tuple(node)
                new_dist = dist[current] + self.grid[node[0]][node[1]]
                if node not in dist or dist[node] > new_dist:
                    dist[node] = new_dist  # self.grid[x][y] have weight of the move
                    prev[node] = current
                    open.put(PrioritizedItem(new_dist, node))

        raise Exception("No path found")  # shouldn't happen

    def shortest_path(self, start: (int, int), end: (int, int)) -> [(int, int)]:
        """
        Calculates the shortest path from start to end
        :param start: start position
        :param end: end position
        :return: list of positions
        """

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            item: Tuple[int, int] = field(compare=False)

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open = PriorityQueue()
        open.put(PrioritizedItem(0, start))
        dist = dict()
        dist[start] = 0  # f cost
        g = dict()  # g cost
        g[start] = abs(start[0] - end[0]) + abs(start[1] - end[1])  # heuristic
        prev = dict()
        prev[start] = None
        while not open.empty():
            current = open.get().item
            if current == end:
                path, u = [], end
                while prev[u]:
                    path.append(u)
                    u = prev[u]
                path.append(start)
                path.reverse()
                return path
            for node in self.__get_neighbors(current):
                node = tuple(node)
                new_g = g[current] + self.grid[node[0]][node[1]]
                new_dist = new_g + heuristic(node, end)  # f cost
                if node not in dist or dist[node] > new_dist:
                    dist[node] = new_dist  # self.grid[x][y] have weight of the move
                    g[node] = new_g
                    prev[node] = current
                    open.put(PrioritizedItem(new_dist, node))

        raise Exception("No path found")  # shouldn't happen


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
