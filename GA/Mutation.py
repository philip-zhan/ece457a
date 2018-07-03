import random


class Mutation:
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate

    def simple(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome

    def uniform(self, chromosome):
        lb = min(chromosome)
        ub = max(chromosome)
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                chromosome[i] = random.uniform(lb, ub)
        return chromosome
