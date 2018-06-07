import random

from neat import *
from neat.nn import MLRecurrentNetwork

from fitness import fitness_function, music_parser


def evaluate_genomes(populations: dict, config: Config, dataset: list):
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
    world_ratings = [evaluate_world(w, dataset) for w in worlds]
    for world_index, rating in enumerate(world_ratings):
        for instrument in instruments:
            genome_index = shuffled[instrument][world_index]
            populations[instrument][genome_index][1].fitness = rating


def evaluate_world(world: dict, dataset: list) -> float:
    out = 0.0
    for melody in dataset:
        tracks = generate_tracks(world, melody)
        #cleaned = {x: music_parser(y) for x, y in tracks.items()}
        cleaned = music_parser(tracks)
        fitness = fitness_function(cleaned)
        out += sum(fitness.values()) / len(fitness)
    return out


def generate_tracks(world: dict, melody) -> dict:
    tracks = {x: [] for x in world.keys()}
    # First tick sends zeroes for inputs at generated instruments
    inputs = melody[0] + [0] * sum([len(x.output_nodes) for x in world.values()])
    for instrument, list in tracks.items():
        output = [float(round(i)) for i in world[instrument].activate(inputs)]
        list.append(output)
    # Following ticks use previous outputs
    for tick, melody_inputs in enumerate(melody[1:]):
        inputs = melody_inputs.copy()
        for i in tracks.values():
            inputs.extend(i[tick])
        for instrument, list in tracks.items():
            output = [float(round(i)) for i in world[instrument].activate(inputs)]
            list.append(output)
    return tracks
