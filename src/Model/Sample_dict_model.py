from .model_constants import Agent_type

sample_model = {
    'army_dist': {
        Agent_type.INFANTRY_BLUE: {
            'quantity': [10],
            'position': [(20, 20)]},
        Agent_type.INFANTRY_RED: {
            'quantity': [100],
            'position': [(270, 20)]}},
    'infantry_speed': 1
}
# TODO: it doesn't work with multiple regiments with same unit types ans team
# there should be possibility to create e.g. two blue infantry regiments
# maybe change dict to list

sample_model2 = {
    'army_dist': {
        Agent_type.SOLDIER_BLUE: {
            'quantity': [10],
            'position': [(20, 20)]},
        Agent_type.SOLDIER_RED: {
            'quantity': [100],
            'position': [(40, 20)]},
        Agent_type.SOLDIER_DUMMY3: {
            'quantity': [10],
            'position': [(70, 100)]},
        Agent_type.SOLDIER_DUMMY4: {
            'quantity': [10],
            'position': [(140, 120)]}},
    'infantry_speed': 2
}
