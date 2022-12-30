import agentpy as ap
import random
from enum import Enum
from typing import Tuple, Dict, List
from copy import deepcopy
from numpy import sqrt
import random

class Orders(Enum):
    MoveEnemyLongRange = 1

class dummy_hussar(ap.Agent):

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)



class dummy_infantry(ap.Agent):

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
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

    def setup(self, **kwargs):
        self.speed = self.p['infantry_speed']

    def setup_map_binding(self, battle_front: ap.Grid):
        self.battle_front = battle_front
        self.pos = self.battle_front.positions[self]

    def move(self, enemy_regiment: ap.AgentList, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        match self.regiment_order:
            case Orders.MoveEnemyLongRange:
                vector = self.__calculateVector(enemy_position, regiment_position)

                self.battle_front.move_by(self, self.vector)
                self.pos = self.battle_front.positions[self]

    def __calculateVector(self, enemy_position: Tuple[int, int], regiment_position: Tuple[int, int]):
        x,y = (0,0)
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
        self.vector = (int(x),int(y))

    def correct_move(self, agent_positions: Dict[Tuple[int,int],List[ap.Agent]]):
        if len(agent_positions[self.pos]) > 1:
            correction_vector = (0, 0)
            corrected_position = self.pos
            vectors = self.__correct_vector()
            depleted_vector = vectors.pop(len(vectors)-1)
            while len(vectors) > 0 and corrected_position in agent_positions:
                correction_vector = (self.vector[0] - depleted_vector[0], self.vector[1] - depleted_vector[1])
                corrected_position = (self.pos[0] - correction_vector[0], self.pos[1] - correction_vector[1])
                depleted_vector = vectors.pop(len(vectors)-1)
            self.battle_front.move_by(self, ((corrected_position not in agent_positions) * correction_vector[0], (corrected_position not in agent_positions) * correction_vector[1]))

    def __correct_vector(self) -> List[Tuple[int,int]]:
        vectors = []
        x_sign = (self.vector[0]>0)*2-1
        y_sign = (self.vector[1]>0)*2-1
        for x in range(abs(self.vector[0])+1):
            for y in range(abs(self.vector[1])+1):
                vectors.append((x_sign*x,y_sign*y))

        random.shuffle(vectors)
        return vectors


    def setup(self, **kwargs):
        self.speed = self.p['infantry_speed']

    def setup_map_binding(self, battle_front: ap.Grid):
        self.battle_front = battle_front

    def move(self, x_axis: int, y_axis: int):
        self.battle_front.move_by(self, (x_axis, y_axis))


class dummy_archer(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)


class dummy_artillery(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)




