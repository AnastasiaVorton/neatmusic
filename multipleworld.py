"""Implements the core evolution algorithm."""
from __future__ import print_function

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

    def __init__(self, config, instruments, initial_state=None):
        self.instruments_map = dict.fromkeys(instruments)
        self.species = {}
        self.best_genomes = {}
        self.reporters = ReporterSet()
        self.config = config
        stagnation = config.stagnation_type(config.stagnation_config, self.reporters)
        self.reproduction = config.reproduction_type(config.reproduction_config,
                                                     self.reporters,
                                                     stagnation)
        if config.fitness_criterion == 'max':
            self.fitness_criterion = max
        elif config.fitness_criterion == 'min':
            self.fitness_criterion = min
        elif config.fitness_criterion == 'mean':
            self.fitness_criterion = mean
        elif not config.no_fitness_termination:
            raise RuntimeError(
                "Unexpected fitness_criterion: {0!r}".format(config.fitness_criterion))

        if initial_state is None:
            # Create a population from scratch, then partition into species.
            self.generation = 0
            i = 0
            for instrument in instruments:
                population = self.reproduction.create_new(config.genome_type,
                                                          config.genome_config,
                                                          config.pop_size)
                self.instruments_map[instrument] = population
                self.species[instrument] = config.species_set_type(config.species_set_config, self.reporters)
                self.species[instrument].speciate(config, self.instruments_map[instrument], self.generation)
                i = i + 1
        else:
            self.population, self.species, self.generation = initial_state

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

        if self.config.no_fitness_termination and (n is None):
            raise RuntimeError("Cannot have no generational limit with no fitness termination")

        k = 0
        while n is None or k < n:
            k += 1

            self.reporters.start_generation(self.generation)

            # Evaluate all genomes using the user-provided function.
            # x = list(((item[0], list(iteritems(item[1]))) for item in self.instruments_map.items()))
            fitness_function(dict(((item[0], list(iteritems(item[1]))) for item in self.instruments_map.items())), self.config)

            for (instrument, population) in self.instruments_map.items():
                # Gather and report statistics.
                best = None
                for g in itervalues(population):
                    if best is None or g.fitness > best.fitness:
                        best = g
                self.reporters.post_evaluate(self.config, population, self.species[instrument], best)

                # Track the best genome ever seen.
                if not (instrument in self.best_genomes) or best.fitness > self.best_genomes[instrument].fitness:
                    self.best_genomes[instrument] = best

                if not self.config.no_fitness_termination:
                    # End if the fitness threshold is reached.
                    fv = self.fitness_criterion(g.fitness for g in itervalues(population))
                    if fv >= self.config.fitness_threshold:
                        self.reporters.found_solution(self.config, self.generation, self.best_genomes[instrument])
                        break

                # Create the next generation from the current generation.
                self.instruments_map[instrument] = self.reproduction.reproduce(self.config, self.species[instrument],
                                                                               self.config.pop_size, self.generation)

                # Check for complete extinction.
                if not self.species[instrument].species:
                    self.reporters.complete_extinction()

                    # If requested by the user, create a completely new population,
                    # otherwise raise an exception.
                    if self.config.reset_on_extinction:
                        self.instruments_map[instrument] = self.reproduction.create_new(self.config.genome_type,
                                                                                        self.config.genome_config,
                                                                                        self.config.pop_size)
                    else:
                        raise CompleteExtinctionException()

                # Divide the new population into species.
                self.species[instrument].speciate(self.config, self.instruments_map[instrument], self.generation)
                self.reporters.end_generation(self.config, self.instruments_map[instrument], self.species[instrument])

            self.generation += 1

        # if self.config.no_fitness_termination:
        #     self.reporters.found_solution(self.config, self.generation, self.best_genome)

        return self.best_genomes
