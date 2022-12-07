from .model_constants import Agent_type

sample_model = {
    'army_dist': {
        Agent_type.INFANTRY_BLUE: {
            'quantity': [100,200],
            'position': [(20, 20),(50,120)]},
        Agent_type.INFANTRY_RED: {
            'quantity': [100,200],
            'position': [(270, 90),(270,190)]}},
    'infantry_speed': 2
}
