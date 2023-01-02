from enum import Enum
from math import sqrt
from typing import Tuple, Dict, List

import agentpy as ap
import random
from src.Agent.unit import Unit
from src.Agent.unit import Orders
from src.Agent.unit import Status
import random


class Soldier(ap.Agent):

    def setup_map_binding(self, battle_front: ap.Grid):
        self.battle_front = battle_front

    def setup(self):
        # team:
        # 'blue' -> 0
        # 'red' -> 1
        self.team = 0
        # Initialize an attribute with a parameter
        self.health = 100
        self.damage = 200  # To kill enemy in one step for easier debugging

        # status:
        #   2 - alive and fighting (default)
        #   1 - surrendered and running away
        #   0 - dead
        self.status = 2

        # view range
        self.view_range = 2

        # self.endurance = 100
        # self.strength = 100
        # self.speed = 100
        # self.itd = 123
        # self.itp = 321

        self.battle_front = None
        self.speed = None
        self.battle_front: ap.Grid
        self.speed: float = 1
        self.pos: int
        self.regiment_order: Orders
        self.regiment_order = Orders.MoveEnemyLongRange
        self.overflow_y = 0
        self.overflow_x = 0
        self.vector = (0, 0)
        # self.team = 0

    def attack(self, enemy):
        enemy.health -= self.damage
        # if soldier killed enemy
        if enemy.health <= 0:
            enemy.status = 0

    # TODO: One soldiers shouldn't be on top of another
    # def move(self, x_axis: int, y_axis: int):
    #     pos = self.battle_front.positions[self]
    #     destination = (pos[0] + x_axis, pos[1] + y_axis)
    #     if destination in self.battle_front.empty:  # check if target position is empty
    #         self.battle_front.move_by(self, (x_axis, y_axis))
    #     else:
    #         pass

    #########################

    def move(self, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        match self.regiment_order:
            case Orders.MoveEnemyLongRange:
                self.__calculateVector(enemy_position, regiment_position)
                self.battle_front.move_by(self, self.vector)
                self.pos = self.battle_front.positions[self]

    def __calculateVector(self, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        x, y = (0, 0)
        if enemy_position[1] != regiment_position[1] and enemy_position[0] != regiment_position[0]:
            a = (enemy_position[1] - regiment_position[1]) / (enemy_position[0] - regiment_position[0])
            sign = (enemy_position[0] > regiment_position[0]) * 2 - 1
            x = sign * sqrt(self.speed ** 2 / (1 + a ** 2))
            y = a * x
            x += self.overflow_x
            y += self.overflow_y
            self.overflow_y = y - int(y)
            self.overflow_x = x - int(x)
        elif enemy_position[0] == regiment_position[0]:
            y = self.speed * ((enemy_position[1] > regiment_position[1]) * 2 - 1)
            y += self.overflow_y
            self.overflow_y = y - int(y)
        else:
            x = self.speed * ((enemy_position[0] > regiment_position[0]) * 2 - 1)
            x += self.overflow_x
            self.overflow_x = x - int(x)
        self.vector = (int(x), int(y))

    def correct_move(self, agent_positions: Dict[Tuple[int, int], List[ap.Agent]]):
        if len(agent_positions[self.pos]) > 1:
            correction_vector = (0, 0)
            corrected_position = self.pos
            vectors = self.__correct_vector()
            depleted_vector = vectors.pop(len(vectors) - 1)
            while len(vectors) > 0 and corrected_position in agent_positions:
                correction_vector = (self.vector[0] - depleted_vector[0], self.vector[1] - depleted_vector[1])
                corrected_position = (self.pos[0] - correction_vector[0], self.pos[1] - correction_vector[1])
                depleted_vector = vectors.pop(len(vectors) - 1)
            self.battle_front.move_by(self, ((corrected_position not in agent_positions) * correction_vector[0],
                                             (corrected_position not in agent_positions) * correction_vector[1]))

    def __correct_vector(self) -> List[Tuple[int, int]]:
        vectors = []
        x_sign = (self.vector[0] > 0) * 2 - 1
        y_sign = (self.vector[1] > 0) * 2 - 1
        for x in range(abs(self.vector[0]) + 1):
            for y in range(abs(self.vector[1]) + 1):
                vectors.append((x_sign * x, y_sign * y))

        random.shuffle(vectors)
        return vectors


class Infantry(Unit):

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

    def setup(self, **kwargs):  # remember: attributes are inherited from Unit superclass
        self.speed = self.p['infantry_speed']
        self.regiment_order = Orders.MoveAndAttack
        # self.tema has to be set outside, by regiment
        self.health = 100
        self.damage = 0  # Somehow that doesn't work, it takes damage value  from superclass...
        self.status = Status.Fighting
        self.range = 1

    def __attack(self, enemy_regiment):
        def inside_of_grid(troop: Infantry):
            return 0 < self.battle_front.grid.positions[troop][0] < self.battle_front.grid.shape[0] and \
                0 < self.battle_front.grid.positions[troop][1] < self.battle_front.grid.shape[0]

        if not inside_of_grid(self):
            return

        for neighbor in self.battle_front.grid.neighbors(self, distance=self.range).to_list():
            if neighbor.team != self.team:
                # attack the first found neighbour from opposite team
                # break to not attack all neighbours but only the first one
                neighbor.health -= self.damage
                # if soldier killed enemy
                if neighbor.health <= 0:
                    neighbor.status = Status.Dead
                break

    # TODO: One soldiers shouldn't be on top of another
    # def move(self, x_axis: int, y_axis: int):
    #     pos = self.battle_front.positions[self]
    #     destination = (pos[0] + x_axis, pos[1] + y_axis)
    #     if destination in self.battle_front.empty:  # check if target position is empty
    #         self.battle_front.move_by(self, (x_axis, y_axis))
    #     else:
    #         pass

    #########################

    def take_action(self, enemy_regiment, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        match self.regiment_order:
            case Orders.MoveAndAttack:
                self.__attack(enemy_regiment)
                self.__calculatePath(enemy_position)
                start = (len(self.path) > self.speed) * self.speed + (len(self.path) <= self.speed) * (
                            len(self.path) - 1)
                for i in range(start, -1, -1):
                    if self.path[i] in self.battle_front.grid.empty:
                        vector = (self.path[i][0] - self.pos[0], self.path[i][1] - self.pos[1])
                        self.battle_front.grid.move_by(self, vector)
                        break
                self.pos = self.battle_front.grid.positions[self]

    def __calculatePath(self, enemy_position: Tuple[int, int]):
        self.path = self.battle_front.shortest_path(self.pos, enemy_position)


class HorseArcher(Unit):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.speed: int
        self.accuracy: int
        self.last_target: Unit
        self.damage: int

    def setup(self, **kwargs):  # remember: attributes are inherited from Unit superclass
        self.speed = 6
        self.regiment_order = Orders.MoveAndAttack
        # self.tema has to be set outside, by regiment
        self.health = 90
        self.damage = 10  # Somehow that doesn't work, it takes damage value  from superclass...
        self.status = Status.Fighting
        self.range = 80
        self.accuracy = 0.65

    def __attack(self, enemy_regiment):
        def inside_of_grid(troop: Unit):
            return 0 < self.battle_front.grid.positions[troop][0] < self.battle_front.grid.shape[0] and \
                0 < self.battle_front.grid.positions[troop][1] < self.battle_front.grid.shape[0]

        if not inside_of_grid(self):
            return

        for neighbor in self.battle_front.grid.neighbors(self, distance=self.range).to_list():
            if neighbor.team != self.team:
                self.last_target = neighbor
                # attack the first found neighbour from opposite team
                # break to not attack all neighbours but only the first one
                neighbor.health -= (random.random < self.accuracy) * self.damage
                # if soldier killed enemy
                if neighbor.health <= 0:
                    neighbor.status = Status.Dead
                break

    def take_action(self, enemy_regiment, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        match self.regiment_order:
            case Orders.MoveAndAttack:
                self.__attack(enemy_regiment)
                self.__calculatePath(enemy_position)
                start = (len(self.path) > self.speed) * self.speed + (len(self.path) <= self.speed) * (
                            len(self.path) - 1)
                for i in range(start, -1, -1):
                    if self.path[i] in self.battle_front.grid.empty:
                        vector = (self.path[i][0] - self.pos[0], self.path[i][1] - self.pos[1])
                        self.battle_front.grid.move_by(self, vector)
                        break
                self.pos = self.battle_front.grid.positions[self]

