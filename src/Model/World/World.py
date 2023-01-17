import agentpy as ap
import numpy as np

from .Terrain import Terrain

from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Tuple, List
from itertools import product

class World:

    grid: ap.Grid
    terrain: Terrain

    def __init__(self, grid, terrain):
        self.grid = grid
        self.terrain = terrain

    def shortest_path(self, start: (int, int), end: (int, int), foot_range: int = 10) -> [(int, int)]:
        """
        Calculates the shortest path from start to end
        :param start: start position
        :param end: end position
        :param foot_range: area to search
        :return: list of positions
        """

        #if target is in straight line, move only in x or y direction
        x_diff = abs(start[0] - end[0])
        y_diff = abs(start[1] - end[1])
        if x_diff > y_diff * 4:
            if start[0] - end[0] > 0:
                return [(start[0] - i, start[1]) for i in range(foot_range)]
            else:
                return [(start[0] + i, start[1]) for i in range(foot_range)]
        if 4 * x_diff < y_diff:
            if start[1] - end[1] > 0:
                return [(start[0], start[1] - i) for i in range(foot_range)]
            else:
                return [(start[0], start[1] + i) for i in range(foot_range)]

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            item: Tuple[int, int] = field(compare=False)

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open = PriorityQueue()
        open.put(PrioritizedItem(0, start))
        #search_area = self.__calculate_search_neighbourghood(start, foot_range)
        new_end = end
        g = dict()  # g cost -> distance from starting node
        g[start] = 0
        prev = dict()
        prev[start] = None
        while not open.empty():
            current = open.get().item
            if current == new_end or g[current] > 20:
                path, u = [], current
                while prev[u]:
                    path.append(u)
                    u = prev[u]
                path.append(start)
                path.reverse()
                return path
            for node in self.__get_neighbors(current):
                if node not in self.grid.empty:
                    continue
                node = tuple(node)
                new_g = g[current] + self.terrain.grid[node[0]][node[1]]
                new_dist = new_g + heuristic(node, end)  # f cost
                if node not in g or g[node] > new_g:  # self.grid[x][y] have weight of the move
                    g[node] = new_g
                    prev[node] = current
                    open.put(PrioritizedItem(new_dist, node))
        return []
        raise Exception("No path found")  # shouldn't happen

    def __get_neighbors(self, node):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= node[0] + i < self.grid.shape[0] and 0 <= node[1] + j < self.grid.shape[1]:
                    neighbours.append((node[0] + i, node[1] + j))
        return neighbours

    def __calculate_search_neighbourghood(self, start: Tuple[int,int], foot_range: int) -> List[np.ndarray]:
        upper_limit_x = self.grid.shape[0] - foot_range - 1
        upper_limit_y = self.grid.shape[1] - foot_range - 1
        x_min = (foot_range < start[0]) * (start[0] - foot_range)
        x_max = (start[0] > upper_limit_x) * (self.grid.shape[0] - 1) + (
                    start[0] <= upper_limit_x) * (start[0] + foot_range)
        y_min = (foot_range < start[1]) * (start[1] - foot_range)
        y_max = (start[1] > upper_limit_y) * (self.grid.shape[1] - 1) + (
                    start[1] <= upper_limit_y) * (start[1] + foot_range)

        neighbourhood_list = [np.arange(x_min, x_max + 1), np.arange(y_min, y_max + 1)]

        return neighbourhood_list

    def __project_end(self, start: Tuple[int,int], end: Tuple[int,int], search_area: List[np.ndarray]) -> Tuple[int,int]:
        if end[0] in search_area[0] and end[1] in search_area[1]:
            return end

        corner = np.array(max(search_area[0]), max(search_area[1]))
        np_start = np.array(start)
        np_stop = np.array(end)

        dist_vector = np_stop - np_start
        dist = np.linalg.norm(dist_vector)
        direction_vector = dist_vector / dist

        multiplier = np.min(abs((corner-start)/(direction_vector + 1e-10)))

        return tuple(np.round(start + direction_vector * multiplier))
