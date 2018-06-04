import os
import configparser
from neat import *
from neat.checkpoint import Checkpointer
from neat.config import Config
from neat.genome import DefaultGenome
from neat.nn import RecurrentNetwork
from neat.population import Population
from neat.reporting import StdOutReporter
from neat.reproduction import DefaultReproduction
from neat.species import DefaultSpeciesSet
from neat.stagnation import DefaultStagnation
from neat.statistics import StatisticsReporter

from fitness import *


def main():
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)
    num_of_octaves = int(input("Please enter the number of octaves you want your music to be generated: "))
    num_of_instruments = int(input("Please enter the number of instruments you want to generate: "))

    p = Population(config)

    p.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(Checkpointer(5))

    set_network_parameters(num_of_octaves, num_of_instruments, config, conf_path)

    winner = p.run(eval_genomes, 300)
    print(winner)


def set_network_parameters(num_of_octaves, num_of_instruments, cnf, cnf_path):
    """Sets ANN's parameters based on the number of octaves and instruments the user wants to generate"""
    num_inputs = (12 * num_of_octaves * num_of_instruments) + (num_of_octaves * 12)
    num_outputs = num_of_octaves * 12
    temp_conf = configparser.ConfigParser()
    temp_conf.read(cnf_path)
    cnf.genome_config.num_inputs = str(num_inputs)
    cnf.genome_config.num_outputs = str(num_outputs)
    print(cnf.genome_config.num_inputs)
    print(cnf.genome_config.num_outputs)


def build_generator_function(genome, config: Config):
    nn = RecurrentNetwork.create(genome, config)
    return lambda input: nn.activate(input)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        func = build_generator_function(genome, config)
        genome.fitness = eval_function(func)


if __name__ == "__main__":
    main()
