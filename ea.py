import os
import operator
import random


class EA:

    def __init__(self, clauses, num_literals):
        self.clauses = clauses
        self.num_clauses = len(self.clauses)
        self.num_literals = num_literals

        """
        Parameters were selected experimentally
        """
        self.max_iterations = 1000
        self.generation_size = 100
        self.mutation_rate = 0.01
        self.selection_size = 10
        self.current_iteration = 0
        self.crossover_p = 0.5
        # self.tournament_k = 20
        self.top_chromosome = None


    def is_clause_satisfied(self, valuation_list, clause):
        """
        Returns True if clause is true (satisfied) or False if not satisfied.
        """
        for literal in clause:
            if literal < 0:
                v = 1 - valuation_list[-literal - 1]
            else:
                v = valuation_list[literal - 1]
            if v == 1:
                return True
        return False


    def goal_function(self, fitness, chromosome):
        """
        In case we find optimal solution, we remember gene as optimal and stop the
        algorithm (stop condition will be archieved).
        """

        if fitness == self.num_clauses:
            self.top_chromosome = chromosome


    def fitness(self, chromosome):
        """
        Number of satisfied clauses with given valuation
        """
        num_true_clauses = 0
        for c in self.clauses:
            num_true_clauses += self.is_clause_satisfied(chromosome, c)

        self.goal_function(num_true_clauses, chromosome)

        return num_true_clauses


    def initial_population(self):
        """
        Initialize population using random approach
        """
        solutions = [[random.randint(0,1) for x in range(self.num_literals)] for y in range(self.generation_size)]
        init_pop = [Chromosome(solution, self.fitness(solution)) for solution in solutions]

        return init_pop


    def stop_condition(self):
        return self.current_iteration > self.max_iterations or self.top_chromosome != None


    def selection(self, chromosomes):
        """
        Perform selection using top 10 best fitness chromosome approach
        """

        #TODO add tournament or rullete approach!
        sorted_chromos = sorted(chromosomes, key = lambda chromo: chromo.fitness)
        selected_chromos = sorted_chromos[:10]

        return selected_chromos


    def crossover(self, a, b):
        """
        Perform uniform crossover with given probability crossover_p
        """
        ab = a
        ba = b

        for i in range(len(a)):
            p = random.random()
            if p < self.crossover_p:
                ab[i] = a[i]
                ba[i] = b[i]
            else:
                ab[i] = b[i]
                ba[i] = a[i]

        return (ab,ba)


    def mutation(self, chromosome):
        """
        Performing mutation over chromosome with given probability mutation_rate
        """
        t = random.random()
        if t < self.mutation_rate:
            #We do mutation
            i = random.randint(0, len(chromosome)-1)
            chromosome[i] = 1 if chromosome[i] == 0 else 0

        return chromosome


    def create_generation(self, for_reproduction):
        """
        With individuals obtained in for_reproduction array we generate new generation
        using genetic operators crossover and mutation. The new generation is the same
        length as at the starting point.
        """
        new_generation = []

        #While we don't fill up new_generation
        while len(new_generation) < self.generation_size:
            #Pick 2 randomly and do crossover
            parents = random.sample(for_reproduction, 2)
            child1, child2 = self.crossover(parents[0].solution, parents[1].solution)

            #Perform mutation after crossover
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            #Add new chromosomes into new generation
            new_generation.append(Chromosome(child1, self.fitness(child1)))
            new_generation.append(Chromosome(child2, self.fitness(child2)))

        return new_generation


    def run(self):
        #Generate initial population and calculate fitness of each chromosome
        chromosomes = self.initial_population()

        #While stop condition is not archieved
        while not self.stop_condition():
            print('Iteration %d:' % self.current_iteration)

            #From population choose chromosomes for reproduction
            for_reproduction = self.selection(chromosomes)

            #Show current state of algorithm
            print('Top solution fitness = %d' % max(chromosomes, key = lambda chromo: chromo.fitness).fitness)

            #Using genetic operators crossover and mutation create new chromosomes
            chromosomes = self.create_generation(for_reproduction)

            self.current_iteration += 1

        #Return best chromosome in the last population
        if self.top_chromosome:
            return Chromosome(self.top_chromosome, self.fitness(self.top_chromosome))
        else:
            max(chromosomes, key = lambda chromo: chromo.fitness)



class Chromosome:
    """
    Class chromosome represents one chromosome that has one solution
    and it fitness value
    """
    def __init__(self, solution, fitness):
        self.solution = solution
        self.fitness = fitness

    def __str__(self):
        return ('f = ' + str(self.fitness) + ' %s') % [x for x in self.solution]


def clauses_from_file(filename):
    """
    Returns array of clauses [[1,2,3], [-1,2], ...] and number of literals(variables)
        """
    with open(filename, "r") as fin:
        #remove comments from beginning
        line = fin.readline()
        while(line.lstrip()[0] == 'c'):
            line = fin.readline()

        header = line.split(" ")
        num_literals = int(header[2].rstrip())

        lines = fin.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].split(" ")[:-1]
            lines[i] = [int(x) for x in lines[i]]

        return (lines, num_literals)


def main():
    clauses, num_literals = clauses_from_file(os.path.abspath("examples/aim-50-2_0-yes.cnf"))
    ea = EA(clauses, num_literals)
    solution = ea.run()
    print(solution)

if __name__ == "__main__":
    main()
