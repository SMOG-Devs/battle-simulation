from abc import ABC
from enum import Enum
from math import sqrt
from typing import Tuple, Dict, List

import agentpy as ap
import random


# TODO: finish unit abstract class
class Unit(ABC):
    """
    Grid abstract class for pygame visualization
    :argument cell_count: size of grid (horizontal and vertical)
    """
    def __init__(self):
        self.battle_front = None
        self.speed = None
        self.battle_front: ap.Grid
        self.speed: float
        self.pos: int
        self.regiment_order: Orders
        self.regiment_order = Orders.MoveEnemyLongRange
        self.overflow_y = 0
        self.overflow_x = 0
        self.vector = (0, 0)
        self.team = 0

    def step(self):
        """
        Loads next frame
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

