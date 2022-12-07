import agentpy as ap
from .model_constants import FIELD_WIDTH, FIELD_HEIGHT, Agent_type, Team
from typing import List, Tuple, Dict
import numpy as np
from .MeasureSystem import closestRegiment, centroidOfRegiment


class BattleModel(ap.Model):

    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id)
        self.battle_field = None
        self.army_blue = dict()
        self.army_red = dict()

    def setup(self):
        """ Initiate a list of new agents. """
        self.battle_field = ap.Grid(self, (FIELD_WIDTH, FIELD_HEIGHT), track_empty=True, check_border=True)

        for key, values in self.p['army_dist'].items():
            self._setup_army(key, values['quantity'], values['position'])

    def _setup_army(self, agent_type: Agent_type, quantities: List[int], positions: List[Tuple[int, int]]):
        if agent_type.value[1] == Team.RED:
            self.army_red[agent_type] = []
        else:
            self.army_blue[agent_type] = []

        for quantity, position in zip(quantities, positions):
            regiment = ap.AgentList(self, quantity, agent_type.value[0])
            regiment.speed = 1 #dummy trzeba to później poprawić
            positions_for_soldiers = self._generate_positions(quantity, position)
            self.battle_field.add_agents(regiment, positions=positions_for_soldiers)
            if agent_type.value[1] == Team.RED:
                self.army_red[agent_type].append(regiment)
                regiment.team = Team.RED.value
            else:
                self.army_blue[agent_type].append(regiment)
                regiment.team = Team.BLUE.value
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
        for red,blue in zip(self.army_red.values(),self.army_blue.values()):
            for regiment in red:
                closest = closestRegiment(regiment,self.army_blue)
                regiment.move(closest[1], closest[0], centroidOfRegiment(regiment))
            for regiment in blue:
                closest = closestRegiment(regiment,self.army_red)
                regiment.move(closest[1], closest[0], centroidOfRegiment(regiment))

        #correction
        inv_pos = self.__inverse_position()
        for red,blue in zip(self.army_red.values(),self.army_blue.values()):
            for regiment in red:
                regiment.correct_move(inv_pos)
            for regiment in blue:
                regiment.correct_move(inv_pos)

        print(all(len(node) == 1 for node in inv_pos.values()))

        print(f'{self.t}/150')
        if self.t == 150:
            self.stop()

    def __inverse_position(self) -> Dict[Tuple[int,int],List[ap.Agent]]:
        inv_pos = {}
        for k, v in self.battle_field.positions.items():
            inv_pos[v] = inv_pos.get(v, []) + [k]

        return inv_pos
    def update(self):
        """ Record a dynamic variable. """

    def end(self):
        """ Repord an evaluation measure. """

    def return_soldiers_colors(self):
        colors = {1:'b', 2:'r'}
        written_colors = []

        for key in self.battle_field.positions:
            if key.team == Team.RED.value:
                written_colors.append(colors[2])
            else:
                written_colors.append(colors[1])

        return written_colors