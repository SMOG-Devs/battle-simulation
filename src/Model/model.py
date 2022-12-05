import agentpy as ap
from .model_constants import FIELD_WIDTH, FIELD_HEIGHT, Agent_type, Team
from typing import List, Tuple
import numpy as np
from .regiment import Regiment


class BattleModel(ap.Model):

    def __init__(self, parameters=None, _run_id=None, steps=150, **kwargs):
        super().__init__(parameters, _run_id)
        self.battle_field = None
        self.army = dict()  # required for self.return_soldiers_color but should be removed in the future
        self.steps = steps
        self.regiments: [Regiment] = []  # list of all regiments
        # model manages regiments, regiments manages units

    def setup(self):
        """ Initiate a list of new agents. """
        self.battle_field = ap.Grid(self, (FIELD_WIDTH, FIELD_HEIGHT), track_empty=True, check_border=False)
        Regiment.setup(self, self.battle_field)
        for key, values in self.p['army_dist'].items():
            self._setup_army(key, values['quantity'], values['position'])

    def _setup_army(self, agent_type: Agent_type, quantities: List[int], positions: List[Tuple[int, int]]):
        self.army[agent_type] = []

        for quantity, position in zip(quantities, positions):
            regiment = Regiment(quantity, agent_type.value[0], agent_type.value[1], position)
            self.regiments.append(regiment)

            # this is necessary for printing
            self.army[agent_type].append(regiment.units)
            # TODO:
            # Dodać zabezpieczenie przed nakładaniem się wojsk


    def step(self):
        """ Call a method for every regiment. """
        for reg in self.regiments:
            reg.move()

        for reg in self.regiments:
            reg.attack()

        if self.t == self.steps:
            self.stop()
            self.end()

    def update(self):
        """ Record a dynamic variable. """

    def end(self):
        """ Report an evaluation measure. """
        print("END")

    def return_soldiers_colors(self):
        # TODO: refactor right after Sample_dict_model fixes
        colors = {1:'b', 2:'r', 3:'black'}
        written_colors = []

        for key, value in self.army.items():
            if key.value[1] == Team.BLUE:
                for regiment in value:
                    for agent in regiment:
                        # This 'if' doesn t work with dummy classes
                        if agent.status == 0:
                            written_colors.append(colors[3])
                        else:
                            written_colors.append(colors[1])

            else:
                for regiment in value:
                    for agent in regiment:
                        # This 'if' doesn t work with dummy classes
                        if agent.status == 0:
                            written_colors.append(colors[3])
                        else:
                            written_colors.append(colors[2])
        return written_colors

