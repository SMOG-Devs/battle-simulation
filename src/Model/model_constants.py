from enum import Enum
from . import Dummy_Classes

FIELD_WIDTH = 300
FIELD_HEIGHT = 300


class Team(Enum):
    RED = 0
    BLUE = 1

class Orders(Enum):
    MoveForward = 0
    MoveEnemyLongRange = 1


class Agent_type(Enum):
    HUSSARS_RED = (Dummy_Classes.dummy_hussar, Team.RED)
    HUSSARS_BLUE = (Dummy_Classes.dummy_hussar, Team.BLUE)
    ARTILLERY_BLUE = (Dummy_Classes.dummy_artillery, Team.BLUE)
    ARTILLERY_RED = (Dummy_Classes.dummy_artillery, Team.RED)
    ARCHERS_RED = (Dummy_Classes.dummy_archer, Team.RED)
    ARCHERS_BLUE = (Dummy_Classes.dummy_archer, Team.BLUE)
    INFANTRY_BLUE = (Dummy_Classes.dummy_infantry, Team.BLUE)
    INFANTRY_RED = (Dummy_Classes.dummy_infantry, Team.RED)
