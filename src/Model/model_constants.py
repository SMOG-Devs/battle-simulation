from enum import Enum
from . import Dummy_Classes
from src.Agent.units import Soldier, Infantry

from ..Agent.units import Soldier
from src.Agent.unit import Team

FIELD_WIDTH = 300
FIELD_HEIGHT = 300

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




