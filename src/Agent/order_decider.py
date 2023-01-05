import agentpy as ap
from .stats import HorseArcherStats, ReiterStats
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


def generate_order_reiters(units: ap.AgentList, attacking_row: int) -> Orders:
    ATTACK_THRESHOLD = 1

    stats: List[ReiterStats] = []
    for unit in units:
        stats.append(unit.evaluate_situation())

    sum_of_in_range = 0
    sum_of_ready = 0

    for stat in stats:
        sum_of_in_range += stat.targetInRange
        sum_of_ready += stat.readyToFire

    if sum_of_ready != len(units):
        return Orders.MoveAndReload
    elif sum_of_in_range / len(units) >= ATTACK_THRESHOLD and attacking_row == units[0].row_number:
        return Orders.MoveAndAttack
    return Orders.Move
