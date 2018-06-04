import os
import configparser
from neat import *
from neat.nn import MLRecurrentNetwork

from fitness import *
from multipleworld_neat import *


def main():
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)
    num_of_octaves = int(input("Please enter the number of octaves you want your music to be generated: "))
    num_of_instruments = int(input("Please enter the number of instruments you want to generate: "))

    instruments = [1]

    p = Multipleworld(config, instruments)

    p.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(Checkpointer(50))

    set_network_parameters(num_of_octaves, num_of_instruments, config, conf_path)

    winner = p.run(eval_genomes, 100)
    
    print(winner)
    for test in valid_tests:
        net = build_generator_function(winner, config)
        print(eval_function(net, test))


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
    return MLRecurrentNetwork.create(genome, config)


def eval_genomes(genomes, config):
    genomes = genomes[0][1]
    for genome_id, genome in genomes:
        func = build_generator_function(genome, config)
        genome.fitness = eval_tests(func)


if __name__ == "__main__":
    main()
