import os
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

    p = Population(config)

    p.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(Checkpointer(5))

    winner = p.run(eval_genomes, 300)
    print(winner)


def build_generator_function(genome, config: Config):
    nn = RecurrentNetwork.create(genome, config)
    return lambda input: nn.activate(input)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        func = build_generator_function(genome, config)
        genome.fitness = eval_function(func)


if __name__ == "__main__":
    main()
