import random
from multiprocessing import Pool

from neat import *
from neat.nn import MLRecurrentNetwork

from fitness import fitness_function, music_parser


class Evaluator:
    def __init__(self, octaves: int, dataset: list, workers: int = 5):
        """
        :param octaves: sounding ranges of generated instruments, in octaves
        :param dataset: list of melodies to measure fitnesses of the genomes upon
        :param workers: number of parallel evaluation workers
        """
        self.octaves = octaves
        self.dataset = dataset
        self.workers = workers
        self.pool = Pool(workers)

    def __del__(self):
        self.pool.close()
        self.pool.join()

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
        jobs = [self.run_world_evaluation(w) for w in worlds]
        world_ratings = [self.combine_world_fitness(js) for js in jobs]
        for world_index, rating in enumerate(world_ratings):
            for instrument in instruments:
                genome_index = shuffled[instrument][world_index]
                populations[instrument][genome_index][1].fitness = rating

    def run_world_evaluation(self, world):
        """
        Uses the pool to run the world evaluation
        :param world: dictionary of instruments
        :return: list of jobs for each track in the dataset
        """

        jobs = []
        for melody in self.dataset:
            jobs.append(self.pool.apply_async(Evaluator.evaluate, (world, melody, self.octaves)))
        return jobs

    @staticmethod
    def combine_world_fitness(jobs):
        out = 0.0
        for j in jobs:
            out += j.get()
        return out / len(jobs)

    @staticmethod
    def evaluate(world, melody, octaves):
        tracks = Evaluator.generate_tracks(world, melody)
        tracks[0] = melody
        cleaned = music_parser(tracks)
        fitness = fitness_function(octaves, cleaned)
        return sum(fitness.values()) / len(fitness)


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
