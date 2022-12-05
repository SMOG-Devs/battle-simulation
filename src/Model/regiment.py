from typing import Tuple, List

import agentpy as ap
from .model_constants import Agent_type, Team
import numpy as np


class Regiment:
    regiments: List = []  # static variable, contains tuples (regiment, team) of all regiments
    model: ap.Model = None
    battlefield: ap.Grid = None

    @staticmethod  # call it first before creating any object Regiment
    def setup(model: ap.Model, grid: ap.Grid):
        Regiment.model = model
        Regiment.battlefield = grid

    @staticmethod
    def _add_regiment(regiment, team):
        Regiment.regiments.append((regiment, team))

    @staticmethod
    def _generate_positions(quantity: int, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        positions = []
        x, y = position
        left = int(np.sqrt(quantity))
        for i in range(quantity):
            positions.append((x, y))
            x += 2
            if i % left == 0:
                x = position[0]
                y += 2

        return positions

    def __init__(self, quantity: int, agent_type: Agent_type, team: Team, position: (int, int)):
        self.units = ap.AgentList(Regiment.model, quantity, agent_type)
        positions_for_soldiers = Regiment._generate_positions(quantity, position)
        Regiment.battlefield.add_agents(self.units, positions=positions_for_soldiers)
        Regiment._add_regiment(self.units, team)
        self.units.setup_map_binding(self.battlefield)
        self.units.team = team
        self.team = team

    def units_count(self) -> int:
        return len(self.units)

    def move(self):
        def distance_to(regiment) -> float:
            # TODO: implement
            return 10

        def direction_to(regiment) -> (float, float):
            # Take first unit of self and regiment and normalize their difference
            # TODO: make if smarter
            first = self.units[0]
            second = regiment[0]
            x = self.battlefield.positions[second][0] - self.battlefield.positions[first][0]
            y = self.battlefield.positions[second][1] - self.battlefield.positions[first][1]
            dis = np.linalg.norm((x, y))
            # if regiments are on top of each other, return default
            if dis < 1:
                return 0, 0
            x = x / dis
            y = y / dis
            x = round(x)
            y = round(y)
            return x, y

        smallest_distance = 10000.0
        target = None
        for reg, team in Regiment.regiments:  # check every regiment for possible enemy
            if reg == self:  # ignore self
                continue
            if team != self.team:
                if smallest_distance > distance_to(reg):
                    smallest_distance = distance_to(reg)
                    target = reg

        if target is not None:
            dir = direction_to(target)
            self.units.move(dir[0], dir[1])
        else:
            if self.units[0].team == Team.RED:
                self.units.move(-1, 0)
            else:
                self.units.move(1, 0)

    def attack(self):
        def inside_of_grid(troop):
            return 0 < self.battlefield.positions[troop][0] < self.battlefield.shape[0] and \
                   0 < self.battlefield.positions[troop][1] < self.battlefield.shape[0]

        def attack(troop, attack_range=1):
            if not inside_of_grid(troop):
                return
            for neighbor in self.battlefield.neighbors(troop, distance=attack_range).to_list():
                if neighbor.team != troop.team:
                    # attack the first found neighbour from opposite team
                    # break to not attack all neighbours but only the first one
                    troop.attack(neighbor)
                    break

        for unit in self.units:
            if not inside_of_grid(unit):
                continue
            attack(unit)

    def remove_dead(self):
        # Regiment.battlefield.remove_agents(self.units.select(self.units.health <= 0)) # doesn't work, idk why
        self.units = self.units.select(self.units.health > 0)
