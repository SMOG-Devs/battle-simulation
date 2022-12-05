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

    def __init__(self, quantity: int, agent_type: Agent_type, position: (int, int)):
        self.units = ap.AgentList(Regiment.model, quantity, agent_type.value[0])
        positions_for_soldiers = Regiment._generate_positions(quantity, position)
        self.battlefield.add_agents(self.units, positions=positions_for_soldiers)
