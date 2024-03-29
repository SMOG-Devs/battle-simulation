import buildModel
import pygameSim
import src.Model.Sample_dict_model as sample


def build(parameters: dict, steps: int = 100, filename: str = 'logs/b.plk'):
    buildModel.build(steps, parameters, filename)


def run(filename: str = 'logs/b.plk'):
    pygameSim.run(filename)


def build_and_run(parameters: dict, steps: int = 100, filename: str = 'logs/b.plk'):
    buildModel.build(steps, parameters, filename)
    pygameSim.run(filename)


def debug_mode(parameters: dict, steps: int = 100, filename: str = 'logs/b.plk'):
    buildModel.build(steps, parameters, filename)
    pygameSim.run(filename, True)


if __name__ == '__main__':
    build_and_run(sample.Kokenhausen_real_model_bigger, 1000, 'logs/b.plk')

    # Example for building only:
    # build(sample.sample_model2, 20, 'logs/b.plk')

    # Example for displaying only:
    # run('logs/b.plk')
