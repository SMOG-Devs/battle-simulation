import agentpy as ap
from typing import Dict, List, Tuple
from .model_constants import Agent_type
from numpy import sqrt


def closestRegiment(actual_regiment: ap.AgentList, enemy_regiments: Dict[Agent_type, List[ap.AgentList]]) -> Tuple[Tuple[int,int], ap.AgentList]:
    actual_pos = centroidOfRegiment(actual_regiment)
    closest_dist = float('inf')
    closest = (actual_pos, actual_regiment)
    for army in enemy_regiments.values():
        for regiment in army:
            pos = centroidOfRegiment(regiment)
            distance = sqrt((pos[0] - actual_pos[0]) ** 2 + (pos[1] - actual_pos[1]) ** 2)
            if 0 < distance < closest_dist:
                closest = (pos, regiment)
                closest_dist = distance

    return closest


def centroidOfRegiment(regiment: ap.AgentList) -> Tuple[int, int]:
    x_sum, y_sum = (0, 0)
    for agent in regiment.pos:
        x_sum += agent[0]
        y_sum += agent[1]

    return x_sum // len(regiment), y_sum // len(regiment)
