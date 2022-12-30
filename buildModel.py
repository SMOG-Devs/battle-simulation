import src.Model.model as battle_model


def build(steps: int, parameters: dict, output_filename: str, **kwargs):
    model = battle_model.BattleModel(steps=steps, parameters=parameters, logs_filename=output_filename)
    results = model.run()


