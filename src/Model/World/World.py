import agentpy as ap
from .Terrain import Terrain

from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Tuple

class World:

    grid: ap.Grid
    terrain: Terrain

    def __init__(self, grid, terrain):
        self.grid = grid
        self.terrain = terrain

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
                new_g = g[current] + self.terrain.grid[node[0]][node[1]]
                new_dist = new_g + heuristic(node, end)  # f cost
                if node not in dist or dist[node] > new_dist:
                    dist[node] = new_dist  # self.grid[x][y] have weight of the move
                    g[node] = new_g
                    prev[node] = current
                    open.put(PrioritizedItem(new_dist, node))

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
