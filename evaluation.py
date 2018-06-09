import random

from neat import *
from neat.nn import MLRecurrentNetwork

from fitness import fitness_function, music_parser


class Evaluator:
    def __init__(self, octaves: int, dataset: list):
        """
        :param octaves: sounding ranges of generated instruments, in octaves
        :param dataset: list of melodies to measure fitnesses of the genomes upon
        """
        self.octaves = octaves
        self.dataset = dataset

    def evaluate_genomes(self, populations: dict, config: Config):
        """
        Evaluates the genomes by combining them into worlds and evaluating the worlds
        :param populations: dictionary of populations for each instrument
        :param config: NEAT configuration object
        """
        instruments = list(populations.keys())
        pop_size = len(populations[instruments[0]])
        for pop in populations.values():
            assert len(pop) == pop_size

        # Create a neural network from each genome
        nns = {name: [MLRecurrentNetwork.create(genome, config) for _, genome in genomes]
               for name, genomes in populations.items()}

        # Combine a neural network with other neural networks
        shuffled = {a: list(range(pop_size)) for a in nns.keys()}
        for i in shuffled.values():
            random.shuffle(i)
        worlds = [{a: nns[a][shuffled[a][i]] for a in instruments} for i in range(pop_size)]

        # Evaluate the worlds and calculate genome ratings
        world_ratings = [self.evaluate_world(w) for w in worlds]
        for world_index, rating in enumerate(world_ratings):
            for instrument in instruments:
                genome_index = shuffled[instrument][world_index]
                populations[instrument][genome_index][1].fitness = rating

    def evaluate_world(self, world: dict) -> float:
        """
        Evaluates the world and returns its fitness
        :param world: dictionary of instruments
        :return: world's fitness
        """
        out = 0.0
        for melody in self.dataset:
            tracks = self.generate_tracks(world, melody)
            tracks[0] = melody
            cleaned = music_parser(tracks)
            fitness = fitness_function(self.octaves, cleaned)
            out += sum(fitness.values()) / len(fitness)
        return out

    @staticmethod
    def generate_tracks(world: dict, melody) -> dict:
        """
        Runs the world with a melody
        :param world: dictionary of instruments
        :param melody: list of ticks, used as inputs to neural networks
        :return: dictionary of generated tracks
        """
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
