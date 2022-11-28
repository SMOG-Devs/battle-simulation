import agentpy as ap


class dummy_hussar(ap.Agent):

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)


class dummy_infantry(ap.Agent):

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.battle_front = None
        self.speed = None
        self.battle_front: ap.Grid
        self.speed: int

    def setup(self, **kwargs):
        self.speed = self.p['infantry_speed']

    def setup_map_binding(self, battle_front: ap.Grid):
        self.battle_front = battle_front

    def move(self, x_axis: int, y_axis: int):
        self.battle_front.move_by(self, (x_axis, y_axis))


class dummy_archer(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)


class dummy_artillery(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)




