import os
import random
import re

from neat import *
from neat.nn import MLRecurrentNetwork

from evaluation import *
from multipleworld import *
from midi_reader import read_all_dataset


def main():
    # Config and data initialization
    instruments_input = input("Please enter the instruments' ids as a comma-separated list (e.g.: 1, 33): ")
    instruments = [int(i) for i in re.split('[^0-9]+', instruments_input)]
    config = create_config(instruments)
    data = read_all_dataset(1)
    training_set = random.sample(data, 5)

    # Multiple world initialization
    p = Multipleworld(config, instruments)
    p.add_reporter(StdOutReporter(True))
    p.add_reporter(StatisticsReporter())
    p.add_reporter(Checkpointer(generation_interval=10, filename_prefix='checkpoint-'))

    # Running and result handling
    evaluator = Evaluator(training_set)
    winner = p.run(evaluator.evaluate_genomes, 100)
    print(winner)


def create_config(instruments: list) -> Config:
    """
    Sets ANN's parameters based on the number of octaves and instruments the user wants to generate
    :return: config with provided parameters
    """
    drum_outputs = 5
    outputs = {0: 12, 1: 24, 25: 36, 33: 24}
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)
    num_inputs = 12  # default is 12 for main melody only
    num_outputs = 0
    for instrument in instruments:
        num_inputs += outputs.get(instrument)
    config.set_num_inputs_outputs(num_inputs, num_outputs)

    return config


if __name__ == "__main__":
    main()
