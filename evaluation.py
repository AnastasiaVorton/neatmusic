import random
from multiprocessing import Pool
from typing import *

from neat import *
from neat.nn import MLRecurrentNetwork

from fitness import fitness_function, music_parser

ticks_delay = 32
tracks_per_eval = 5


class Evaluator:
    def __init__(self, dataset: list, workers: int = 5):
        """
        :param dataset: list of melodies to measure fitnesses of the genomes upon
        :param workers: number of parallel evaluation workers
        """
        self.dataset = dataset
        self.workers = workers
        self.pool = Pool(workers)

    def __del__(self):
        self.pool.close()
        self.pool.join()

    def evaluate_genomes(self, populations: dict, configs):
        """
        Evaluates the genomes by combining them into worlds and evaluating the worlds
        :param populations: dictionary of populations for each instrument
        :param configs: NEAT configuration object
        """
        instruments = list(populations.keys())
        pop_size = len(populations[instruments[0]])
        for pop in populations.values():
            assert len(pop) == pop_size

        # Create a neural network from each genome
        nns = {name: [MLRecurrentNetwork.create(genome, configs[name]) for _, genome in genomes]
               for name, genomes in populations.items()}

        # Combine a neural network with other neural networks
        shuffled = {a: list(range(pop_size)) for a in nns.keys()}
        for i in shuffled.values():
            random.shuffle(i)
        worlds = [{a: nns[a][shuffled[a][i]] for a in instruments} for i in range(pop_size)]

        # Evaluate the worlds and calculate genome ratings
        jobs = [self.run_world_evaluation(w) for w in worlds]
        world_ratings = [self.combine_world_fitness(js) for js in jobs]
        for world_index, rating in enumerate(world_ratings):
            for instrument in instruments:
                genome_index = shuffled[instrument][world_index]
                populations[instrument][genome_index][1].fitness = rating

    def run_world_evaluation(self, world: Dict[int, MLRecurrentNetwork]):
        """
        Uses the pool to run the world evaluation
        :param world: dictionary of instruments
        :return: list of jobs for each track in the dataset
        """
        return [self.pool.apply_async(Evaluator.evaluate, (world, track))
                for track in random.sample(self.dataset, tracks_per_eval)]

    @staticmethod
    def combine_world_fitness(jobs) -> float:
        out = sum([i.get() for i in jobs])
        return out / len(jobs)

    @staticmethod
    def evaluate(world: Dict[int, MLRecurrentNetwork], melody: List[List[float]]):
        tracks = Evaluator.generate_tracks(world, melody)
        tracks[0] = melody
        cleaned = {}
        for i in tracks.keys():
            cleaned[i] = music_parser(tracks[i])
        fitness = fitness_function(cleaned)
        return sum(fitness.values()) / len(fitness)

    @staticmethod
    def generate_tracks(world: Dict[int, MLRecurrentNetwork], melody: List[List[float]]) -> Dict[int, List[List[float]]]:
        """
        Runs the world with a melody
        :param world: dictionary of instruments
        :param melody: list of ticks, used as inputs to neural networks
        :return: dictionary of generated tracks
        """
        tracks = {x: [] for x in world.keys()}
        # First tick sends zeroes for inputs at generated instruments
        inputs = [0.0] + melody[0] + [0.0] * sum([len(x.output_nodes) for x in world.values()])
        for instrument, list in tracks.items():
            output = [float(round(i)) for i in world[instrument].activate(inputs)]
            list.append(output)
        # Following ticks use previous outputs
        for tick, melody_inputs in enumerate(melody[1:]):
            inputs = [0.0] + melody_inputs.copy()
            for i in tracks.values():
                inputs.extend(i[tick])
            for instrument, list in tracks.items():
                output = [float(round(i)) for i in world[instrument].activate(inputs)]
                list.append(output)
        # Add last ticks_delay NN activations
        for _ in range(ticks_delay):
            inputs = [1.0] + [0.0] * (len(melody[0]) + sum([len(x.output_nodes) for x in world.values()]))
            for instrument, list in tracks.items():
                output = [float(round(i)) for i in world[instrument].activate(inputs)]
                list.append(output)
        # Remove first ticks_delay NN activations
        for instrument in tracks.keys():
            tracks[instrument] = tracks[instrument][ticks_delay:]
        return tracks
