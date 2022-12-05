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

sample_model2 = {
    'army_dist': {
        Agent_type.SOLDIER_BLUE: {
            'quantity': [10, 10, 20],
            'position': [(20, 20), (100, 100), (120, 120)]},
        Agent_type.SOLDIER_RED: {
            'quantity': [100, 5],
            'position': [(40, 20), (20, 100)]}
    },
    'infantry_speed': 2
}
