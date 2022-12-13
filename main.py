import buildModel
import pygameSim
import src.Model.Sample_dict_model as sample


def build(parameters: dict, steps: int = 100, filename: str = 'logs/b.plk'):
    buildModel.build(steps, sample.sample_model2, filename)


def run(filename: str = 'logs/b.plk'):
    pygameSim.run(filename)


def build_and_run(parameters: dict, steps: int = 100, filename: str = 'logs/b.plk'):
    buildModel.build(steps, sample.sample_model2, filename)
    pygameSim.run(filename)


if __name__ == '__main__':
    build_and_run(sample.sample_model2, 50, 'logs/b.plk')

    # Example for building only:
    # build(sample.sample_model2, 20, 'logs/b.plk')

    # Example for displaying only:
    #run('logs/b.plk')
