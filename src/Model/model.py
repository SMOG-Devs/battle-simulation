import agentpy as ap
from .model_constants import FIELD_WIDTH, FIELD_HEIGHT, Agent_type, Team
from typing import List, Tuple, Dict
import numpy as np
from .regiment import Regiment
import pickle
from .World.World import World
from .World.Terrain import Terrain


class BattleModel(ap.Model):

    def __init__(self, parameters=None, _run_id=None, steps=150, logs_filename: str = 'logs.plk'):
        super().__init__(parameters, _run_id)
        self.battle_field: World = None
        self.army = dict()  # required for self.return_soldiers_color but should be removed in the future
        self.steps = steps
        self.regiments: [Regiment] = []  # list of all regiments
        self.logs_filename = logs_filename
        self.logs: [[(type, Team, int, int, (int,
                                             int))]] = []  # list of frames, each frame have list of tuples: type, team, status, health, (positionX, positionY)
        # model manages regiments, regiments manages units
        self.stats = {}

    def setup(self):
        """ Initiate a list of new agents. """
        self.battle_field = World(ap.Grid(self, (FIELD_WIDTH, FIELD_HEIGHT), track_empty=True, check_border=True), Terrain(FIELD_WIDTH,FIELD_HEIGHT))
        Regiment.setup(self, self.battle_field)
        for key, values in self.p['army_dist'].items():
            self._setup_army(key, values['quantity'], values['position'])

        # stats before the battle
        red_count = 0
        blue_count = 0
        for agent in self.battle_field.grid.agents:
            if agent.team == Team.RED:
                red_count += 1
            else:
                blue_count += 1
        self.stats["before battle red"] = red_count
        self.stats["before battle blue"] = blue_count

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

        reversed_positions = self.__inverse_position()
        print(any(len(agents) > 1 for agents in reversed_positions.values()))

        for reg in self.regiments:
            if reg.is_alive():  # I can't find out why that 'if' is necessary
                # all dead units are removed with .remove_dead() functions and empty
                # regiments are also removed...........
                # but it doesnt work without this 'if'
                reg.move(reversed_positions)

        for reg in self.regiments:
            reg.attack()

        for reg in self.regiments:
            reg.remove_dead()

        for reg in self.regiments:
            if reg.units_count() <= 0:
                self.regiments.remove(reg)

        self._save_frame()
        data = ""
        data += " " + str(self.t)
        for reg in self.regiments:
            data += " " + str(reg.units_count())
        print(data)

        if self.t == self.steps:
            self.stop()

    def __inverse_position(self) -> Dict[Tuple[int, int], List[ap.Agent]]:
        inv_pos = {}
        for k, v in self.battle_field.grid.positions.items():
            inv_pos[v] = inv_pos.get(v, []) + [k]

        return inv_pos

    def update(self):
        """ Record a dynamic variable. """

    def end(self):
        """ Report an evaluation measure. """

        # stats after the battle
        red_count = 0
        blue_count = 0
        for agent in self.battle_field.grid.agents:
            if agent.team == Team.RED:
                red_count += 1
            else:
                blue_count += 1
        self.stats["after battle red"] = red_count
        self.stats["after battle blue"] = blue_count
        self.stats["won"] = "red" if red_count > blue_count else "blue"
        self.stats["red died"] = self.stats["before battle red"] - red_count
        self.stats["blue died"] = self.stats["before battle blue"] - blue_count
        self.stats["red died historically"] = 100
        self.stats["blue died historically"] = 2000

        self.save_logs_as_pickle(self.logs_filename)

        print(self.stats)

    def return_soldiers_colors(self):
        colors = {1: 'b', 2: 'r', 3: 'black'}
        written_colors = []

        for key, value in self.army.items():
            if key.value[1] == Team.BLUE:
                for regiment in value:
                    for agent in regiment:
                        # This 'if' doesn't work with dummy classes
                        if agent.status == 0:
                            written_colors.append(colors[3])
                        else:
                            written_colors.append(colors[1])

            else:
                for regiment in value:
                    for agent in regiment:
                        # This 'if' doesn't work with dummy classes
                        if agent.status == 0:
                            written_colors.append(colors[3])
                        else:
                            written_colors.append(colors[2])
        return written_colors

    def _save_frame(self):
        current_frame = []
        for unit in self.battle_field.grid.agents:
            current_frame.append((str(unit.type), str(unit.team), unit.status, unit.health,
                                  self.battle_field.grid.positions[unit]))
        self.logs.append(current_frame)

    def save_logs_as_pickle(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.logs, file)

        stats = ""
        for key, val in self.stats.items():
            stats += key + ": " + str(val) + "\n"

        with open(filename + ".txt", 'w') as file:
            file.write(stats)