import agentpy as ap
import random


class Soldier(ap.Agent):

    def setup_map_binding(self, battle_front: ap.Grid):
        self.battle_front = battle_front


    def setup(self):
        # team:
        # 'blue' -> 0
        # 'red' -> 1
        self.team = 0
        # Initialize an attribute with a parameter
        self.health = 100
        self.damage = 200  # To kill enemy in one step for easier debugging

        # status:
        #   2 - alive and fighting (default)
        #   1 - surrendered and running away
        #   0 - dead
        self.status = 2

        # view range
        self.view_range = 2

        # self.endurance = 100
        # self.strength = 100
        # self.speed = 100
        # self.itd = 123
        # self.itp = 321


    def attack(self, enemy):
        enemy.health -= self.damage
        # if soldier killed enemy
        if enemy.health <= 0:
            enemy.status = 0

    # TODO: One soldiers shouldn't be on top of another
    def move(self, x_axis: int, y_axis: int):
        pos = self.battle_front.positions[self]
        destination = (pos[0] + x_axis, pos[1] + y_axis)
        if destination in self.battle_front.empty:  # check if target position is empty
            self.battle_front.move_by(self, (x_axis, y_axis))
        else:
            pass

