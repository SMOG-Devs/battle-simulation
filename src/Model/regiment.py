from __future__ import annotations

from math import sqrt
from typing import Tuple, List, Set

import agentpy as ap
from .model_constants import Agent_type
import numpy as np
from src.Agent.unit import Team, Orders
from .World.World import World
import src.Agent.order_decider as general
import src.Agent.units as u
from math import atan2
import random

class Regiment:
    regiments: List = []  # static variable, contains all regiments
    model: ap.Model = None
    battlefield: World = None
    type: Agent_type
    positions = set()
    degree: float
    attacking_row: int
    rows: int

    @staticmethod  # call it first before creating any object Regiment
    def setup(model: ap.Model, grid: World):
        Regiment.model = model
        Regiment.battlefield = grid

    @staticmethod
    def _add_regiment(regiment):
        Regiment.regiments.append(regiment)

    @staticmethod
    def _generate_positions(quantity: int, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        positions = []
        x, y = position
        units_per_line = round(np.sqrt(quantity))
        square = quantity & units_per_line != 0

        x_range = x + units_per_line * 2
        y_range = y + (units_per_line + square) * 2

        assert not any(x <= curr_x <= x_range and y <= curr_y <= y_range for curr_x, curr_y in
                        Regiment.battlefield.grid.positions.values()), 'Two regiments are intercepting'

        for i in range(1, quantity + 1):
            positions.append((x, y))
            x += 2
            if i % units_per_line == 0:
                x = position[0]
                y += 2

        return positions

    def __init__(self, quantity: int, agent_type: Agent_type, team: Team, position: (int, int)):
        self.units = ap.AgentList(Regiment.model, quantity, agent_type)
        self.positions = Regiment._generate_positions(quantity, position)
        Regiment.battlefield.grid.add_agents(self.units, positions=self.positions)
        Regiment._add_regiment(self)
        self.units.setup_map_binding(self.battlefield)
        self.units.team = team
        self.team = team
        self.type = agent_type
        match agent_type:
            case u.Reiter:
                self.__establish_rows()
                self.degree = 0
                self.attacking_row = 1

    def __establish_rows(self):
        curr_y = -1
        row_number = 0
        for unit in self.units:
            if curr_y != unit.pos[1]:
                curr_y = unit.pos[1]
                row_number += 1
            unit.row_number = row_number
        self.rows = row_number


    def units_count(self) -> int:
        return len(self.units)

    def __establish_order(self):
        match self.type:
            case u.HorseArcher:
                self.units.regiment_order = general.generate_order_horse_archers(self.units)
            case u.Reiter:
                row_number = 1
                units = self.units.select(self.units.row_number == row_number)
                while len(units) != 0:
                    order = general.generate_order_reiters(units, self.attacking_row)
                    if order is not Orders.MoveAndAttack and self.attacking_row == row_number:
                        self.attacking_row = (self.attacking_row + 1) % self.rows + 1
                    units.regiment_order = order
                    row_number += 1
                    units = self.units.select(self.units.row_number == row_number)


    def take_action(self):

        target: ((int, int), Regiment) = self.__closest_regiment()  # Remember: it contains ((int, int), Regiment)
        if target is None:
            return
        if len(target[1].units) <= 0:
            return  # This shouldn't happen, where there is no enemy, battle is won
        # direction = direction_to(target[1]) we don't pass direction, we pass enemy and self centroid tuples instead
        position = self.__centroid_of_regiment()
        direction = -1 + (np.linalg.norm([position[0] - target[0][0],position[1] - target[0][1]]) >= self.units[0].range - random.random()*20) * 2
        match self.type:
            case u.Reiter:
                position_of_regiment = self.__centroid_of_regiment()
                reiter_path = self.battlefield.shortest_path(position_of_regiment, target[0])
                reiter_speed = (len(reiter_path) >= self.units[0].speed) * self.units[0].speed + (len(reiter_path) < self.units[0].speed) * (len(reiter_path) - 1)
                self.units.find_target(target[1])
                self.__establish_order()
                x_diff = target[0][0] - position_of_regiment[0]
                y_diff = target[0][1] - position_of_regiment[1]
                m = atan2(y_diff, x_diff)
                sign = 1
                if self.degree > m:
                    sign *= -1
                if abs(self.degree - m) > np.pi:
                    sign *= -1
                angle = 0
                if np.pi >= abs(self.degree - m) >= .25*np.pi or np.pi >= 2*np.pi - abs(self.degree - m) >= .25*np.pi:
                    angle = sign * .25*np.pi
                while True and reiter_speed >= 0:
                    try:
                        new_pos = reiter_path[reiter_speed]
                        move = (direction * (new_pos[0] - position[0]), direction * (new_pos[1] - position[1]))
                        self.units.check_availability(move, position_of_regiment, self.positions, angle)
                        self.units.take_action(target[1], target[0], position_of_regiment, move,angle)
                        self.positions = set(self.units.pos)
                        self.degree += angle
                        break
                    except IndexError:
                        break
                    except Exception:
                        reiter_speed -= 1




            case _:
                self.units.find_target(target[1])
                self.__establish_order()
                self.units.take_action(target[1], target[0], self.__centroid_of_regiment())

    def remove_dead(self):
        # Regiment.battlefield.remove_agents(self.units.select(self.units.health <= 0)) # doesn't work, idk why
        Regiment.battlefield.grid.remove_agents(self.units.select(self.units.health <= 0))
        self.units = self.units.select(self.units.health > 0)

    def is_alive(self) -> bool:  # check if any soldier is alive
        return len(self.units) >= 1

    # Search for closest regiment
    def __closest_regiment(self) -> Tuple[Tuple[int, int], Regiment]:  # object = Regiment
        def distance(a: Regiment, b: Regiment):  # Get distance between two regiments
            c_a = a.__centroid_of_regiment()
            c_b = b.__centroid_of_regiment()
            return sqrt((c_a[0] - c_b[0]) ** 2 + (c_a[1] - c_b[1]) ** 2)

        closest_regiment: Regiment = None
        closest_dist = float('inf')
        closest: ((int, int), Regiment)

        for reg in Regiment.regiments:
            if reg == self:
                continue
            if reg.team == self.team:
                continue
            if len(reg.units) <= 0:  # TODO: this if shouldn't be necessary, empty regiments should be removed
                continue
            if distance(self, reg) < closest_dist:
                closest_dist = distance(self, reg)
                closest_regiment = reg

        if closest_regiment is None:
            return None
        return closest_regiment.__centroid_of_regiment(), closest_regiment

    def __centroid_of_regiment(self) -> Tuple[int, int]:
        if len(self.units) == 0:
            return None
        x_sum, y_sum = (0, 0)
        for agent in self.units:
            pos = self.battlefield.grid.positions[agent]
            x_sum += pos[0]
            y_sum += pos[1]

        return x_sum // len(self.units), y_sum // len(self.units)
