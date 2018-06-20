import os
import re
import random

from composition_generator import generate_composition
from evaluation import *
from multipleworld import *
from midi_reader import read_all_dataset
from neat.gru import GRUGenome

instrument_outputs = {0: 12, 1: 24, 25: 36, 33: 24}
input_melody_octaves = 1


def main() -> None:
    # Config and data initialization
    data = read_all_dataset(input_melody_octaves)
    training_set = random.sample(data, 30)

    # Multiple world initialization
    settings = read_settings()
    if settings[0]:
        p = Checkpointer.restore_checkpoint('checkpoints' + os.sep + settings[1])
    else:
        instruments = settings[1]
        configs = create_config(instruments)
        p = Multipleworld(configs, instruments)
    p.add_reporter(StdOutReporter(True))
    p.add_reporter(StatisticsReporter())
    p.add_reporter(
        Checkpointer(instruments=p.outputs, generation_interval=1, filename_prefix='checkpoints' + os.sep + 'cp-'))

    # Running and result handling
    evaluator = Evaluator(training_set)
    winner = p.run(evaluator.evaluate_genomes)
    print(winner)


def read_settings():
    """
    Reads whether a user wants to restore training or start a new one
    :return:
    """
    continue_or_new = input("Do you want to restore previous generation or start new? [res/new] ")
    if continue_or_new == 'res':
        checkpoint_name = find_last_checkpoint()
        return True, checkpoint_name
    elif continue_or_new == 'new':
        instruments = read_instruments()
        return False, instruments


def find_last_checkpoint():
    """
    finds the name of last check point
    :return: the name of last check point
    """
    file_list = [f for f in os.listdir('checkpoints') if f.startswith('cp-')]
    file_list.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
    return file_list[len(file_list) - 1]


def read_instruments() -> Dict[int, int]:
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
        config = Config(GRUGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)
        config.set_num_inputs(num_inputs)
        config.set_num_outputs(num_outputs)
        configs[instrument] = config
    return configs


if __name__ == "__main__":
    main()
