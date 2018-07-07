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

    def random_noise(self, chromosome, sigma):
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                chromosome[i] += random.gauss(0, sigma)
        return chromosome

    def insert(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                first = random.randrange(len(chromosome)-1)
                second = random.randrange(first+1, len(chromosome))
                chromosome.insert(first+1, chromosome.pop(second))
        return chromosome

    def swap(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                first = random.randrange(len(chromosome)-1)
                second = random.randrange(first+1, len(chromosome))
                temp = chromosome[first]
                chromosome[first] = chromosome[second]
                chromosome[second] = temp
        return chromosome
