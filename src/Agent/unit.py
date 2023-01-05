from abc import ABC
from enum import Enum
from math import sqrt
from typing import Tuple, Dict, List
from src.Model.World.World import World
from .stats import Stats

import agentpy as ap
import random

class Team(Enum):
    RED = 0
    BLUE = 1

class Orders(Enum):
    MoveAndAttack = 1
    Wait = 2
    Move = 3
    MoveAndReload = 4


class Status(Enum):
    Fighting = 1
    Dead = 0
    Surrender = 2


class Unit(ap.Agent):
    """
    Grid abstract class for pygame visualization
    :argument cell_count: size of grid (horizontal and vertical)
    """
    battle_front: World
    speed: int
    pos: Tuple[int,int]
    path: List[Tuple[int,int]]
    regiment_order: Orders
    health: float
    damage: float
    status: int
    range: int

    def __init__(self, model, *args, **kwargs):
        """
        Initialize variables
        """
        super().__init__(model, *args, **kwargs)
        self.last_target: Unit

    def setup(self, **kwargs):
        """
        Loads parameters from self.p e.x:  self.speed = self.p['infantry_speed']
        """
        print("setup have no override")

    def setup_map_binding(self, battle_front: World):
        """
        Setup self positions and ap.Grid
        :argument battle_front: ap.Grid
        """
        self.battle_front = battle_front
        self.pos = self.battle_front.grid.positions[self]

    def take_action(self, enemy_regiment, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        """
        Move regiment towards enemy regiment
        :argument enemy_position: (int, int) target regiment
        :argument enemy_regiment: (Regiment) enemy regiment
        :argument regiment_position: (int, int) own regiment
        """
        print("move have no override")

    def evaluate_situation(self) -> Stats:
        """
        Gives information on which basis order will be formed
        """
        print("evaluate_situation has no override")

    def find_target(self, enemy_regiment):
        found = False
        for neighbor in self.battle_front.grid.neighbors(self, distance=self.range).to_list():
            if neighbor.team != self.team and neighbor in enemy_regiment.units:
                self.last_target = neighbor
                found = True
                break
        if not found:
            self.last_target = None

