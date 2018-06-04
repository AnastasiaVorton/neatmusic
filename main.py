import os
from neat import *
from neat.nn import MLRecurrentNetwork

from fitness import *
from multipleworld_neat import *


def main():
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)

    instruments = [1]

    p = Multipleworld(config, instruments)

    p.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(Checkpointer(50))

    winner = p.run(eval_genomes, 100)
    print(winner)
    for test in valid_tests:
        net = build_generator_function(winner, config)
        print(eval_function(net, test))


def build_generator_function(genome, config: Config):
    return MLRecurrentNetwork.create(genome, config)


def eval_genomes(genomes, config):
    genomes = genomes[0][1]
    for genome_id, genome in genomes:
        func = build_generator_function(genome, config)
        genome.fitness = eval_tests(func)


if __name__ == "__main__":
    main()
