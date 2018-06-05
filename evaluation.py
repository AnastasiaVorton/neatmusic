import random

from neat import *
from neat.nn import MLRecurrentNetwork


def evaluate_genomes(populations: dict, config: Config):
    instruments = list(populations.keys())
    pop_size = len(populations[instruments[0]])
    for pop in populations.values():
        assert len(pop) == pop_size

    # Create a neural network from each genome
    nns = {name: [MLRecurrentNetwork.create(genome, config) for _, genome in genomes]
           for name, genomes in populations.items()}

    # Combine a neural networks with other neural networks
    shuffled = {a: list(range(pop_size)) for a in nns.keys()}
    for i in shuffled.values():
        random.shuffle(i)
    worlds = [{a: nns[a][shuffled[a][i]] for a in instruments} for i in range(pop_size)]

    # Evaluate the worlds and calculate genome ratings
    world_ratings = [evaluate_world(w) for w in worlds]
    for world_index, rating in enumerate(world_ratings):
        for instrument in instruments:
            genome_index = shuffled[instrument][world_index]
            populations[instrument][genome_index][1].fitness = rating


def evaluate_world(world: dict) -> float:
    return 0.0
