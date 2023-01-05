from enum import Enum
from . import Dummy_Classes
from src.Agent.units import Soldier, Infantry, HorseArcher, Cannon, Hussar, Reiter


from ..Agent.units import Soldier
from src.Agent.unit import Team

FIELD_WIDTH = 400
FIELD_HEIGHT = 400

#
# TEAM enum moved to src/Agent/unit.py
#

class Agent_type(Enum):
    HUSSARS_RED = (Dummy_Classes.dummy_hussar, Team.RED)
    HUSSARS_BLUE = (Dummy_Classes.dummy_hussar, Team.BLUE)
    ARTILLERY_BLUE = (Dummy_Classes.dummy_artillery, Team.BLUE)
    ARTILLERY_RED = (Dummy_Classes.dummy_artillery, Team.RED)
    ARCHERS_RED = (Dummy_Classes.dummy_archer, Team.RED)
    ARCHERS_BLUE = (Dummy_Classes.dummy_archer, Team.BLUE)
    INFANTRY_BLUE = (Dummy_Classes.dummy_infantry, Team.BLUE)
    INFANTRY_RED = (Dummy_Classes.dummy_infantry, Team.RED)
    SOLDIER_BLUE = (Soldier, Team.BLUE)
    SOLDIER_RED = (Soldier, Team.RED)

    INFANTRY2_BLUE = (Infantry, Team.BLUE)
    INFANTRY2_RED = (Infantry, Team.RED)
    HORSE_ARCHER_BLUE = (HorseArcher, Team.BLUE)
    HORSE_ARCHER_RED = (HorseArcher, Team.RED)
    REITERS_BLUE = (Reiter, Team.BLUE)
    REITERS_RED = (Reiter, Team.RED)

    CANNON_BLUE = (Cannon, Team.BLUE)
    CANNON_RED = (Cannon, Team.RED)

    HUSSAR_BLUE = (Hussar, Team.BLUE)
    HUSSAR_RED = (Hussar, Team.RED)



