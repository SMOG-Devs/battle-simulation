from __future__ import annotations

from math import sqrt
from typing import Tuple, List

import agentpy as ap
from .model_constants import Agent_type
import numpy as np
from src.Agent.unit import Team, Orders
from .World.World import World
import src.Agent.order_decider as general
import src.Agent.units as u


class Regiment:
    regiments: List = []  # static variable, contains all regiments
    model: ap.Model = None
    battlefield: World = None
    type: Agent_type

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
        positions_for_soldiers = Regiment._generate_positions(quantity, position)
        Regiment.battlefield.grid.add_agents(self.units, positions=positions_for_soldiers)
        Regiment._add_regiment(self)
        self.units.setup_map_binding(self.battlefield)
        self.units.team = team
        self.team = team
        self.type = agent_type

    def units_count(self) -> int:
        return len(self.units)

    def __establish_order(self):
        match self.type:
            case u.HorseArcher | u.HorseArcher:
                self.units.regiment_order = general.generate_order_horse_archers(self.units)

    def take_action(self):

        target: ((int, int), Regiment) = self.__closest_regiment()  # Remember: it contains ((int, int), Regiment)
        if target is None:
            return
        if len(target[1].units) <= 0:
            return  # This shouldn't happen, where there is no enemy, battle is won

        # direction = direction_to(target[1]) we don't pass direction, we pass enemy and self centroid tuples instead
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
