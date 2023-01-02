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

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            item: Tuple[int, int] = field(compare=False)

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open = PriorityQueue()
        open.put(PrioritizedItem(0, start))
        search_area = self.__calculate_search_neighbourghood(start, foot_range)
        new_end = self.__project_end(start, end, search_area)
        dist = dict()
        dist[start] = 0  # f cost
        g = dict()  # g cost
        g[start] = abs(start[0] - end[0]) + abs(start[1] - end[1])  # heuristic
        prev = dict()
        prev[start] = None
        while not open.empty():
            current = open.get().item
            if current == new_end:
                path, u = [], current
                while prev[u]:
                    path.append(u)
                    u = prev[u]
                path.append(start)
                path.reverse()
                return path
            for node in self.__get_neighbors(current, search_area):
                node = tuple(node)
                new_g = g[current] + self.terrain.grid[node[0]][node[1]]
                new_dist = new_g + heuristic(node, end)  # f cost
                if node not in dist or dist[node] > new_dist:
                    dist[node] = new_dist  # self.grid[x][y] have weight of the move
                    g[node] = new_g
                    prev[node] = current
                    open.put(PrioritizedItem(new_dist, node))

        raise Exception("No path found")  # shouldn't happen

    def __get_neighbors(self, node, search_area):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x = node[0] + i
                new_y = node[1] + j
                if (i == 0 and j == 0) or (new_y not in search_area[1] and new_x not in search_area[0]):
                    continue
                if 0 <= new_x < self.grid.shape[0] and 0 <= new_y < self.grid.shape[1]:
                    neighbours.append((new_x, new_y))
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
