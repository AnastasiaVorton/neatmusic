import os

from neat import *
from neat.nn import MLRecurrentNetwork

from evaluation import *
from multipleworld import *
from midi_reader import read_all_dataset


def main():
    # Config and data initialization
    num_of_octaves = int(input("Please enter the number of octaves you want your music to be generated: "))
    num_of_instruments = int(input("Please enter the number of instruments you want to generate: "))
    config = create_config(num_of_octaves, num_of_instruments)
    instruments = [i for i in range(num_of_instruments)]
    data = read_all_dataset(num_of_octaves)

    # Multiple world initialization
    p = Multipleworld(config, instruments)
    p.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(Checkpointer(50))

    # Running and result handling
    winner = p.run(lambda x, y: evaluate_genomes(x, y, data), 3)
    print(winner)


def create_config(num_of_octaves: int, num_of_instruments: int) -> Config:
    """
    Sets ANN's parameters based on the number of octaves and instruments the user wants to generate
    :param num_of_octaves:
    :param num_of_instruments:
    :return: config with provided parameters
    """
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)

    num_inputs = num_of_octaves * 12 * (num_of_instruments + 1)
    num_outputs = num_of_octaves * 12
    config.set_num_inputs_outputs(num_inputs, num_outputs)

    return config


if __name__ == "__main__":
    main()
