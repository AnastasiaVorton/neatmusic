"""Implements the core evolution algorithm."""
from __future__ import print_function

from neat import Config
from neat.reporting import ReporterSet
from neat.math_util import mean
from neat.six_util import iteritems, itervalues


class CompleteExtinctionException(Exception):
    pass


class Multipleworld(object):
    """
    This class implements the core evolution algorithm:
        1. Evaluate fitness of all genomes.
        2. Check to see if the termination criterion is satisfied; exit if it is.
        3. Generate the next generation from the current population.
        4. Partition the new generation into species based on genetic similarity.
        5. Go to 1.
    """

    def __init__(self, configs, instruments, initial_state=None):
        """
        :param instruments: map of used instruments to number of outputs
        """
        self.instruments_map = {}
        self.species = {}
        self.best_genomes = {}
        self.reporters = ReporterSet()
        self.configs = configs
        self.common_config = list(configs.values())[0]
        self.outputs = instruments
        stagnation = self.common_config.stagnation_type(self.common_config.stagnation_config, self.reporters)
        self.reproduction = self.common_config.reproduction_type(self.common_config.reproduction_config,
                                                                 self.reporters,
                                                                 stagnation)
        if self.common_config.fitness_criterion == 'max':
            self.fitness_criterion = max
        elif self.common_config.fitness_criterion == 'min':
            self.fitness_criterion = min
        elif self.common_config.fitness_criterion == 'mean':
            self.fitness_criterion = mean
        elif not self.common_config.no_fitness_termination:
            raise RuntimeError(
                "Unexpected fitness_criterion: {0!r}".format(self.common_config.fitness_criterion))

        if initial_state is None:
            # Create a population from scratch, then partition into species.
            self.generation = 0
            i = 0
            for instrument in instruments:
                config = self.configs[instrument]
                population = self.reproduction.create_new(config.genome_type,
                                                          config.genome_config,
                                                          config.pop_size)
                self.instruments_map[instrument] = population
                self.species[instrument] = config.species_set_type(config.species_set_config, self.reporters)
                self.species[instrument].speciate(config, self.instruments_map[instrument], self.generation)
                i = i + 1
        else:
            self.instruments_map, self.species, self.generation = initial_state
            self.generation = self.generation + 1

    def add_reporter(self, reporter):
        self.reporters.add(reporter)

    def remove_reporter(self, reporter):
        self.reporters.remove(reporter)

    def run(self, fitness_function, n=None):
        """
        Runs NEAT's genetic algorithm for at most n generations.  If n
        is None, run until solution is found or extinction occurs.

        The user-provided fitness_function must take only two arguments:
            1. The population as a list of (genome id, genome) tuples.
            2. The current configuration object.

        The return value of the fitness function is ignored, but it must assign
        a Python float to the `fitness` member of each genome.

        The fitness function is free to maintain external state, perform
        evaluations in parallel, etc.

        It is assumed that fitness_function does not modify the list of genomes,
        the genomes themselves (apart from updating the fitness member),
        or the configuration object.
        """

        if self.common_config.no_fitness_termination and (n is None):
            raise RuntimeError("Cannot have no generational limit with no fitness termination")

        k = 0
        while n is None or k < n:
            k += 1

            self.reporters.start_generation(self.generation)

            # Evaluate all genomes using the user-provided function.
            # x = list(((item[0], list(iteritems(item[1]))) for item in self.instruments_map.items()))
            fitness_function(dict(((item[0], list(iteritems(item[1]))) for item in self.instruments_map.items())),
                             self.configs)

            for (instrument, population) in self.instruments_map.items():
                # Gather and report statistics.
                best = None
                for g in itervalues(population):
                    if best is None or g.fitness > best.fitness:
                        best = g
                self.reporters.post_evaluate(self.configs[instrument], population, self.species[instrument], best)

                # Track the best genome ever seen.
                if not (instrument in self.best_genomes) or best.fitness > self.best_genomes[instrument].fitness:
                    self.best_genomes[instrument] = best

                if not self.configs[instrument].no_fitness_termination:
                    # End if the fitness threshold is reached.
                    fv = self.fitness_criterion(g.fitness for g in itervalues(population))
                    if fv >= self.configs[instrument].fitness_threshold:
                        self.reporters.found_solution(self.configs[instrument], self.generation,
                                                      self.best_genomes[instrument])
                        break

                # Create the next generation from the current generation.
                self.instruments_map[instrument] = self.reproduction.reproduce(self.configs[instrument],
                                                                               self.species[instrument],
                                                                               self.configs[instrument].pop_size,
                                                                               self.generation)

                # Check for complete extinction.
                if not self.species[instrument].species:
                    self.reporters.complete_extinction()

                    # If requested by the user, create a completely new population,
                    # otherwise raise an exception.
                    if self.configs[instrument].reset_on_extinction:
                        self.instruments_map[instrument] = self.reproduction.create_new(
                            self.configs[instrument].genome_type,
                            self.configs[instrument].genome_config,
                            self.configs[instrument].pop_size)
                    else:
                        raise CompleteExtinctionException()

                # Divide the new population into species.
                self.species[instrument].speciate(self.configs[instrument], self.instruments_map[instrument],
                                                  self.generation)

            self.reporters.end_generation(self.configs, self.instruments_map, self.species)

            self.generation += 1

        # if self.config.no_fitness_termination:
        #     self.reporters.found_solution(self.config, self.generation, self.best_genome)

        return self.best_genomes
