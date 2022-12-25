import pickle
from abc import ABC
from itertools import product
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Tuple

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

    def shortest_path(self, start: (int, int), end: (int, int)) -> [(int, int)]:
        """
        Calculates the shortest path from start to end
        :param start: start position
        :param end: end position
        :return: list of positions
        """
        # nodes = self.__get_nodes()
        # neighbors = self.__get_neighbors
        # dist = {node: float('inf') for node in nodes}
        # dist[start] = 0
        # prev = {node: None for node in nodes}
        # while nodes:
        #     u = min(nodes, key=lambda node: dist[node])
        #     nodes.remove(u)
        #     if dist[u] == float('inf'):
        #         break
        #     for v in neighbors(u):
        #         alt = dist[u] + self.grid[v[0]][v[1]]
        #         if alt < dist[v]:
        #             dist[v] = alt
        #             prev[v] = u
        #     if u == end:
        #         break
        # path, u = [], end
        # while prev[u]:
        #     path.append(u)
        #     u = prev[u]
        # path.append(start)
        # path.reverse()
        # return path

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            item: Tuple[int,int] = field(compare=False)

        open = PriorityQueue()
        open.put(PrioritizedItem(0,start))
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


if __name__ == '__main__':
    g = Terrain(70, 70)
    print(g.shortest_path((4, 10), (18, 29)))
# [(4, 10), (3, 9), (2, 8), (1, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (1, 25), (2, 26), (2, 27), (3, 28), (4, 29), (5, 30), (6, 31), (7, 32), (8, 33), (9, 32), (10, 31), (11, 30), (12, 30), (13, 30), (14, 30), (15, 29), (16, 28), (17, 28), (18, 29)]

# tests
# cur_path = os.path.dirname(__file__)
# print(cur_path)
# new_path = cur_path.replace('src\\Visualization', 'logs.plk')
# print(new_path)

# g = GridPickle(300, 'logs.plk')
