from dataclasses import dataclass, field
from itertools import product
from queue import PriorityQueue
from typing import Tuple
from PIL import Image
import numpy as np

class Terrain:
    def __init__(self, x: int, y: int):  # x y: size of the grid
        self.x = x
        self.y = y
        self.grid = []
        for i in range(self.x):
            self.grid.append([])
            for j in range(self.y):
                self.grid[i].append(0)

        image = Image.open('src//Visualization//Sprites//Map1.png')
        image = np.asarray(image)
        code = {(0, 255, 0): 1, (0, 0, 255): 10, (100, 100, 100): 3}
        for i in range(self.x):
            for j in range(self.y):
                r, g, b, a = image[i][j]
                self.grid[j][i] = code[(r, g, b)]  # TODO: i and j are swapped

        # for i in range(self.x):
        #     for j in range(self.y):
        #         # test terrain:
        #         if abs(i - j) < 3:  # river in the middle: weight 10
        #             self.grid[i][j] = 10
        #         elif i > j + 10:  # mountains at the top/right: weight 3
        #             self.grid[i][j] = 3
        #         else:  # grass in bot/left: weight 1
        #             self.grid[i][j] = 1
        #
        #             # three obstacles in the middle of the grass
        #             if (i - 10) ** 2 + (j - 20) ** 2 < 10 ** 2:
        #                 self.grid[i][j] = 3
        #             if (i - 40) ** 2 + (j - 30) ** 2 < 10 ** 2:
        #                 self.grid[i][j] = 3
        #             if (i - 30) ** 2 + (j - 100) ** 2 < 10 ** 2:
        #                 self.grid[i][j] = 3

    def get_grid(self) -> [[]]:  # grid with weights
        return self.grid

    def __get_nodes(self):
        return [(i, j) for i, j in product(range(self.x), range(self.y))]


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