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
sample_model4 = {
    'army_dist': {
        Agent_type.INFANTRY2_RED: {
            'quantity': [100, 100],
            'position': [(20, 20), (20, 40)]},
        Agent_type.INFANTRY2_BLUE: {
            'quantity': [100, 100],
            'position': [(140, 20), (40, 140)]}
    },
    'infantry_speed': 1
}

sample_model5 = {
    'army_dist': {
        Agent_type.INFANTRY2_RED: {
            'quantity': [20, 30],
            'position': [(0, 0), (20, 0)]},
        Agent_type.INFANTRY2_BLUE: {
            'quantity': [20, 30],
            'position': [(40, 20), (20, 20)]}
    },
    'infantry_speed': 1
}

sample_model6 = {
    'army_dist': {
        Agent_type.CANNON_RED: {
            'quantity': [5, 2],
            'position': [(50, 10), (30, 200)]},
        Agent_type.INFANTRY2_BLUE: {
            'quantity': [20, 30],
            'position': [(140, 20), (40, 140)]}
    },
    'infantry_speed': 1
}

sample_model7 = {
    'army_dist': {
        Agent_type.HUSSAR_BLUE: {
            'quantity': [7, 5],
            'position': [(150, 100), (150,120)]},
        Agent_type.HUSSAR_RED: {
            'quantity': [6, 6],
            'position': [(200, 100), (200, 120)]},
    },
    'infantry_speed': 1
}