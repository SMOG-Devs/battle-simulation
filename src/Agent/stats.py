from abc import ABC
from dataclasses import dataclass


@dataclass
class Stats(ABC):
    pass

@dataclass
class HorseArcherStats(Stats):
    targetInRange: bool