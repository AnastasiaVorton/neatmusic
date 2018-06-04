import os
import configparser
from neat import *
from neat.nn import MLRecurrentNetwork

from fitness import *
from multipleworld_neat import *

def main():
    num_of_octaves = int(input("Please enter the number of octaves you want your music to be generated: "))
    num_of_instruments = int(input("Please enter the number of instruments you want to generate: "))

    config = create_config(num_of_octaves, num_of_instruments)
    instruments = [i for i in range(num_of_instruments)]

    p = Multipleworld(config, instruments)

    p.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(Checkpointer(50))

    winner = p.run(eval_genomes, 100)
    
    print(winner)


def create_config(num_of_octaves: int, num_of_instruments: int) -> Config:
    """Sets ANN's parameters based on the number of octaves and instruments the user wants to generate"""
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)

    num_inputs = num_of_octaves * 12 * (num_of_instruments + 1)
    num_outputs = num_of_octaves * 12
    config.genome_config.num_inputs = num_inputs
    config.genome_config.num_outputs = num_outputs

    return config


def build_generator_function(genome, config: Config):
    return MLRecurrentNetwork.create(genome, config)


def eval_genomes(populations, config):
    for name, genomes in populations.items():
        for genome_id, genome in genomes:
            func = build_generator_function(genome, config)
            genome.fitness = eval_function(func)


if __name__ == "__main__":
    main()
