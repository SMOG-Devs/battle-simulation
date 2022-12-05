import agentpy as ap
from .model_constants import FIELD_WIDTH, FIELD_HEIGHT, Agent_type, Team
from typing import List, Tuple
import numpy as np


class BattleModel(ap.Model):

    def __init__(self, parameters=None, _run_id=None, steps=150, **kwargs):
        super().__init__(parameters, _run_id)
        self.battle_field = None
        self.army = dict()
        self.steps = steps

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

            # This don t work for dummy_classes
            regiment.team = agent_type.value[1]

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
        # print(self.t)
        # if self.t == 41:
        #     print("Warning")
        def inside_of_grid(unit):
            return 0 < self.battle_field.positions[unit][0] < FIELD_WIDTH and \
                   0 < self.battle_field.positions[unit][1] < FIELD_HEIGHT

        def attack(unit, attack_range=1):
            # li = self.battle_field.neighbors(unit, distance=attack_range)
            # if len(li) < 0:
            #     print("Error")
            #     return
            if not inside_of_grid(unit):
                return
            for neighbor in self.battle_field.neighbors(unit, distance=attack_range).to_list():
                if neighbor.team != unit.team:
                    # attack the first found neigbour from opposite team
                    # break to not attack all neigbours but only the first one
                    unit.attack(neighbor)
                    break

        """ Call a method for every agent. """
        for key, value in self.army.items():
            for regiment in value:
                if key.value[1] == Team.RED:
                    regiment.move(-1, 0)
                else:
                    regiment.move(1, 0)

            # Perform attack
                # TODO: random unit order, currently first regiment attack fist so it always win
                # Apparently it doesn t win because dead unit ale still alive
                for u in regiment:
                    attack(u)
                    u.record(u.vars)

            # TODO: kill dead units


        if self.t == self.steps:
            self.stop()
            self.end()

    def update(self):
        """ Record a dynamic variable. """

    def end(self):
        """ Report an evaluation measure. """
        print("END")
        for key, value in self.army.items():
            for regiment in value:
                for u in regiment:
                    print(u.log)
                    print("-------------------------")

    def return_soldiers_colors(self):
        colors = {1:'b', 2:'r', 3:'black'}
        written_colors = []

        for key,value in self.army.items():
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

