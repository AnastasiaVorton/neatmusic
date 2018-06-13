import os
import re

from composition_generator import generate_composition
from evaluation import *
from multipleworld import *
from midi_reader import read_all_dataset

instrument_outputs = {0: 12, 1: 24, 25: 36, 33: 24}
input_melody_octaves = 1


def main() -> None:
    # Config and data initialization
    generate_composition('checkpoint-287', 'jinglebells2.mid', 'result.mid')

    instruments = read_settings()
    configs = create_config(instruments)
    data = read_all_dataset(input_melody_octaves)
    training_set = random.sample(data, 5)

    # Multiple world initialization
    p = Checkpointer.restore_checkpoint('checkpoint-287')
    # p = Multipleworld(configs, instruments)
    p.add_reporter(StdOutReporter(True))
    p.add_reporter(StatisticsReporter())
    p.add_reporter(Checkpointer(instruments=instruments, generation_interval=1, filename_prefix='checkpoint-'))

    # Running and result handling
    evaluator = Evaluator(training_set)
    winner = p.run(evaluator.evaluate_genomes)
    print(winner)


def read_settings() -> Dict[int, int]:
    """
    Reads the instrument list from the standard input
    :return: a map with requested instruments and numbers of outputs for each instrument
    """
    instruments_input = input("Please enter the instruments' ids as a comma-separated list (e.g.: 1, 33) [1]: ")
    if instruments_input == '':
        instruments_input = '1'
    instruments = {int(i) for i in re.split('[^0-9]+', instruments_input)}
    return {i: instrument_outputs[i] for i in instruments}


def create_config(instruments: Dict[int, int]) -> Dict[int, Config]:
    """
    Sets ANN's parameters based on the number of octaves and instruments the user wants to generate
    :return: config with provided parameters
    """
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    num_inputs = input_melody_octaves * 12 + sum(instruments.values()) + 1
    configs = {}
    for instrument, num_outputs in instruments.items():
        config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)
        config.set_num_inputs(num_inputs)
        config.set_num_outputs(num_outputs)
        configs[instrument] = config
    return configs


if __name__ == "__main__":
    main()
