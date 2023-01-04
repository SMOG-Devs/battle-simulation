import agentpy as ap
from .stats import HorseArcherStats
from typing import List
from .unit import Orders


def generate_order_horse_archers(units: ap.AgentList) -> Orders:
    ATTACK_THRESHOLD = 0.6

    stats: List[HorseArcherStats] = []
    for unit in units:
        stats.append(unit.evaluate_situation())

    sum_of_in_range = 0
    for stat in stats:
        sum_of_in_range += stat.targetInRange

    if ATTACK_THRESHOLD > sum_of_in_range / len(stats):
        return Orders.Move
    return Orders.MoveAndAttack

def generate_order_reiters(units: ap.AgentList) -> Orders:
    return Orders.Move
