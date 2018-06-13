from evaluation import Evaluator
from fitness import music_parser
from midi_reader import read_file, get_original_track
from midi_writer import generate_and_save_midi
from neat import Checkpointer
from neat.nn import MLRecurrentNetwork


def generate_composition(checkpoint_file_name, midi_file_name, new_midi_file_name):
    """
    generates composition from populations and a melody
    :param checkpoint_file_name: file with a serialized population
    :param midi_file_name:
    :param new_midi_file_name:
    :return:
    """
    configs, populations = Checkpointer.retrieve_populations(checkpoint_file_name)
    world = create_fittest_world(populations)
    nns = create_nns_from_world(world, configs)
    initial_melody = read_file(midi_file_name)
    tracks = Evaluator.generate_tracks(nns, initial_melody)
    cleaned = music_parser(tracks)
    generate_and_save_midi(new_midi_file_name, cleaned, get_original_track(midi_file_name))


def create_fittest_world(populations):
    """
    chooses the fittest species, one for each instrument, and creates a world out of them
    :param populations:
    :return:
    """
    world = {}
    for instrument, population in populations.items():
        best_individual = None
        best_fitness = 0
        for individual in population.values():
            if individual.fitness is not None and individual.fitness > best_fitness:
                best_fitness = individual.fitness
                best_individual = individual

        world[instrument] = best_individual
    return world


def create_nns_from_world(world, configs):
    nns = {instrument: MLRecurrentNetwork.create(individual, configs[instrument])
           for instrument, individual in world.items()}
    return nns
