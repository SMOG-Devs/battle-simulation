from enum import Enum
from math import sqrt
from typing import Tuple, Dict, List, Optional

import agentpy as ap
import random
import math

import numpy as np

from src.Agent.unit import Unit
from src.Agent.unit import Orders
from src.Agent.unit import Status
import random
from .stats import HorseArcherStats, Stats


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
        self.damage = 5  # Somehow that doesn't work, it takes damage value  from superclass...
        self.status = Status.Fighting.value
        self.range = 1

    def __attack(self, enemy_regiment):
        def inside_of_grid(troop: Infantry):
            return 0 < self.battle_front.grid.positions[troop][0] < self.battle_front.grid.shape[0] and \
                0 < self.battle_front.grid.positions[troop][1] < self.battle_front.grid.shape[0]

        if not inside_of_grid(self):
            return

        # attack the first found neighbour from opposite team
        # break to not attack all neighbours but only the first one
        self.last_target.health -= self.damage
        # if soldier killed enemy
        if self.last_target.health <= 0:
            self.last_target.status = Status.Dead

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
                if self.last_target is not None:
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
    last_target: Optional[Unit]
    accuracy: float
    damage: int
    speed: int

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

    def setup(self, **kwargs):  # remember: attributes are inherited from Unit superclass
        self.speed = 6
        self.regiment_order = Orders.MoveAndAttack
        # self.tema has to be set outside, by regiment
        self.health = 90
        self.damage = 10  # Somehow that doesn't work, it takes damage value  from superclass...
        self.status = Status.Fighting.value
        self.range = 80
        self.accuracy = 0.65
        self.last_target = None

    def __attack(self, enemy_regiment):
        def inside_of_grid(troop: Unit):
            return 0 < self.battle_front.grid.positions[troop][0] < self.battle_front.grid.shape[0] and \
                0 < self.battle_front.grid.positions[troop][1] < self.battle_front.grid.shape[0]

        if not inside_of_grid(self):
            return

        # attack the first found neighbour from opposite team
        # break to not attack all neighbours but only the first one
        self.last_target.health -= (random.random() < self.accuracy) * self.damage
        # if soldier killed enemy
        if self.last_target.health <= 0:
            self.last_target.status = Status.Dead

    def evaluate_situation(self) -> Stats:
        return HorseArcherStats(self.last_target is not None)

    def find_target(self, enemy_regiment):
        found = False
        for neighbor in self.battle_front.grid.neighbors(self, distance=self.range).to_list():
            if neighbor.team != self.team and neighbor in enemy_regiment.units:
                self.last_target = neighbor
                found = True
                break
        if not found:
            self.last_target = None

    def __calculate_distance_to_target(self) -> float:
        if self.last_target is None:
            return float('inf')
        x_diff = self.pos[0] - self.last_target.pos[0]
        y_diff = self.pos[1] - self.last_target.pos[1]
        return np.linalg.norm([x_diff, y_diff])

    def take_action(self, enemy_regiment, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        match self.regiment_order:
            case Orders.MoveAndAttack:
                if self.last_target is None:
                    self.__calculatePath(enemy_position)
                else:
                    self.__attack(enemy_regiment)
                    if self.__calculate_distance_to_target() < self.last_target.range:
                        self.__calculatePath(self.__reverse_position())  # odwracamy współrzedne
                    else:
                        self.__calculatePath(self.last_target.pos)
            case Orders.Move:
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

    def __reverse_position(self) -> Tuple[int, int]:
        x_diff = self.last_target.pos[0] - self.pos[0]
        y_diff = self.last_target.pos[1] - self.pos[1]

        return int(np.clip(self.pos[0] - x_diff, 0, 400)), int(np.clip(self.pos[1] - y_diff, 0, 400))


class Cannon(Unit):
    reload_time: int
    reload_counter: int
    shot_radius: int

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

    # TODO: model parameters might need to be improved
    def setup(self, **kwargs):  # remember: attributes are inherited from Unit superclass
        self.speed = 1
        self.regiment_order = Orders.MoveAndAttack
        # self.team has to be set outside, by regiment
        self.health = 100
        self.damage = 15  # Somehow that doesn't work, it takes damage value  from superclass...
        self.status = Status.Fighting.value
        self.range = 30
        self.shot_radius = 3
        # how many steps skip until next attack
        self.reload_time = 7
        # increase every step, when it reaches reload_time, attack and reset
        self.reload_counter = 0

    def __attack(self, enemy_regiment):
        def inside_of_grid(troop: Cannon):
            return 0 < self.battle_front.grid.positions[troop][0] < self.battle_front.grid.shape[0] and \
                0 < self.battle_front.grid.positions[troop][1] < self.battle_front.grid.shape[0]

        if not inside_of_grid(self):
            return

        # check if cannon loaded
        if self.reload_counter < self.reload_time:
            self.reload_counter += 1
            return

        # cannon attacks the first found enemy, damage decreases with distance from the shot point
        shock_wave = {}
        for i in range(self.shot_radius + 1):
            # store list of units in shock wave per distance from shot point
            shock_wave[i] = []

        shock_wave[0].append(self.last_target)

        for shot_neighbor in self.battle_front.grid.neighbors(self.last_target, distance=self.shot_radius).to_list():
            if shot_neighbor.team != self.team and shot_neighbor in enemy_regiment.units:
                # max distance from shot point along any axis
                radius_from_shot = np.max(
                    [abs(self.battle_front.grid.positions[shot_neighbor][0]-self.battle_front.grid.positions[self.last_target][0]),
                    abs(self.battle_front.grid.positions[shot_neighbor][1] - self.battle_front.grid.positions[self.last_target][1])]
                )
                shock_wave[radius_from_shot].append(shot_neighbor)

        # attack units within shock wave
        for distance, units in shock_wave.items():
            for unit in units:
                # damage decreases with distance from shot point
                unit.health -= self.damage / (distance + 1)
                # # if cannon killed enemy
                if unit.health <= 0:
                    unit.status = Status.Dead.value

    def take_action(self, enemy_regiment, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        match self.regiment_order:
            case Orders.MoveAndAttack:
                if self.last_target is not None:
                    self.__attack(enemy_regiment)
                self.__calculatePath(enemy_position)
                start = (len(self.path) > self.speed) * self.speed + (len(self.path) <= self.speed) * (
                        len(self.path) - 1)
                # if cannon has enemies in range, it will stop moving and start attack locally
                if self.last_target is not None:
                    return
                # if no enemies in range, cannon will move to the next position
                for i in range(start, -1, -1):
                    if self.path[i] in self.battle_front.grid.empty:
                        vector = (self.path[i][0] - self.pos[0], self.path[i][1] - self.pos[1])
                        self.battle_front.grid.move_by(self, vector)
                        break
                self.pos = self.battle_front.grid.positions[self]

    def __calculatePath(self, enemy_position: Tuple[int, int]):
        self.path = self.battle_front.shortest_path(self.pos, enemy_position)

class Hussar(Unit):
    stopped: bool
    turning_time: int
    turning_counter: int
    accuracy_by_speed: float
    damage: int
    speed: int

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

    def setup(self, **kwargs):  # remember: attributes are inherited from Unit superclass
        self.speed = 8
        self.regiment_order = Orders.MoveAndAttack
        # self.tema has to be set outside, by regiment
        self.health = 60
        self.damage = 20  # Somehow that doesn't work, it takes damage value  from superclass...
        self.status = Status.Fighting.value
        self.range = 2
        # in attack it is correlated with a speed
        self.accuracy_by_speed = 0.25
        # how many steps skip until next attack, beacuse of turning 
        self.turning_time = 3
        # increase every step, when it reaches turning_time, attack and reset
        self.turning_counter = 0
        self.stopped = False

    def __attack(self, enemy_regiment):
        def inside_of_grid(troop: Unit):
            return 0 < self.battle_front.grid.positions[troop][0] < self.battle_front.grid.shape[0] and \
                0 < self.battle_front.grid.positions[troop][1] < self.battle_front.grid.shape[0]

        if not inside_of_grid(self):
            return

        # check if hussar is turned
        if self.turning_counter < self.turning_time:
            self.turning_counter += 1
            return

        # attack the first found neighbour from opposite team
        # break to not attack all neighbours but only the first one
        self.last_target.health -=  (random.random() < self.accuracy_by_speed) * self.speed * self.damage
        # if hussar killed enemy
        if self.last_target.health <= 0:
            self.last_target.status = Status.Dead

    def take_action(self, enemy_regiment, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        match self.regiment_order:
            case Orders.MoveAndAttack:
                if self.last_target is not None:
                    self.__attack(enemy_regiment)
                    self.stopped = True
                
                # self.__calculatePath(enemy_position)

                # When hussar gett stopped, 
                if self.stopped:
                    self.__fallBack(enemy_position)
                    self.stopped = False
                else:
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

    def __fallBack(self, enemy_position: Tuple[int, int]):
        turning_position = [i+math.floor(random.random()*10) for i in enemy_position]
        self.path = turning_position
