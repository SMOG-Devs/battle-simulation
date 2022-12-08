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
            'quantity': [10, 10],
            'position': [(20, 20), (20, 100)]},
        Agent_type.SOLDIER_RED: {
            'quantity': [10, 10, 20],
            'position': [(60, 20), (60, 100), (40, 50)]}
    },
    'infantry_speed': 2
}
sample_model3 = {
    'army_dist': {
        Agent_type.SOLDIER_BLUE: {
            'quantity': [1],
            'position': [(20, 20)]},
        Agent_type.SOLDIER_RED: {
            'quantity': [1],
            'position': [(20, 40)]}
    },
    'infantry_speed': 2
}
