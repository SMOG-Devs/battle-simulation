from abc import ABC
from enum import Enum
from math import sqrt
from typing import Tuple, Dict, List

import agentpy as ap
import random

class Team(Enum):
    RED = 0
    BLUE = 1

class Orders(Enum):
    MoveAndAttack = 1
    Wait = 2


class Status(Enum):
    Fighting = 1
    Dead = 0
    Surrender = 2


class Unit(ap.Agent):
    """
    Grid abstract class for pygame visualization
    :argument cell_count: size of grid (horizontal and vertical)
    """

    def __init__(self, model, *args, **kwargs):
        """
        Initialize variables
        """
        super().__init__(model, *args, **kwargs)
        self.battle_front: ap.Grid
        self.speed: float
        self.pos: int
        self.regiment_order: Orders
        self.overflow_y = 0
        self.overflow_x = 0
        self.team: Team
        self.health = 100
        self.damage = 20
        self.status = 2
        self.range = 1

    def setup(self, **kwargs):
        """
        Loads parameters from self.p e.x:  self.speed = self.p['infantry_speed']
        """
        print("setup have no override")

    def setup_map_binding(self, battle_front: ap.Grid):
        """
        Setup self positions and ap.Grid
        :argument battle_front: ap.Grid
        """
        self.battle_front = battle_front
        self.pos = self.battle_front.positions[self]

    def move(self, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        """
        Move regiment towards enemy regiment
        :argument enemy_position: (int, int) target regiment
        :argument regiment_position: (int, int) own regiment
        """
        print("move have no override")

    def attack(self, enemy_regiment):
        """
        Attack selected regiment :argument enemy_regiment: Regiment - it is optional, e.x: melee units don't need a
        target, they will just attack nearby enemy
        """
        print("attack have no override")
