import agentpy as ap
from .model_constants import FIELD_WIDTH, FIELD_HEIGHT, Agent_type, Team
from typing import List, Tuple
import numpy as np


class BattleModel(ap.Model):

    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id)
        self.battle_field = None
        self.army = dict()

    def setup(self):
        """ Initiate a list of new agents. """
        self.battle_field = ap.Grid(self, (FIELD_WIDTH, FIELD_HEIGHT), track_empty=True, check_border=False)

        for key, values in self.p['army_dist'].items():
            self._setup_army(key, values['quantity'], values['position'])

    def _setup_army(self, agent_type: Agent_type, quantities: List[int], positions: List[Tuple[int, int]]):
        self.army[agent_type] = []

        for quantity, position in zip(quantities, positions):
            regiment = ap.AgentList(self, quantity, agent_type.value[0])
            positions_for_soldiers = self._generate_positions(quantity, position)
            self.battle_field.add_agents(regiment, positions=positions_for_soldiers)
            self.army[agent_type].append(regiment)
            regiment.setup_map_binding(self.battle_field)

            # TODO:
            # Dodać zabezpieczenie przed nakładaniem się wojsk

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

    def step(self):
        """ Call a method for every agent. """
        for key, value in self.army.items():
            for regiment in value:
                if key.value[1] == Team.RED:
                    regiment.move(-1, 0)
                else:
                    regiment.move(1, 0)

        if self.t == 150:
            self.stop()

    def update(self):
        """ Record a dynamic variable. """

    def end(self):
        """ Repord an evaluation measure. """

    def return_soldiers_colors(self):
        colors = {1:'b', 2:'r'}
        written_colors = []

        for key,value in self.army.items():
            if key.value[1] == Team.BLUE:
                for regiment in value:
                    for agent in regiment:
                        written_colors.append(colors[1])
            else:
                for regiment in value:
                    for agent in regiment:
                        written_colors.append(colors[2])

        return written_colors