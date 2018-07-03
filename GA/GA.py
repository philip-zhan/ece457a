from Crossover import Crossover

crossover = Crossover(alpha=0.5)

# SGA
parent1 = [0, 0, 0, 0, 0]
parent2 = [1, 1, 1, 1, 1]
print('ONE_POINT', crossover.one_point(parent1, parent2))
print('N_POINT', crossover.n_point(parent1, parent2))
print('UNIFORM', crossover.uniform(parent1, parent2))

# RGA
parent1 = [0, 0, 0, 0, 0]
parent2 = [0.1, 0.2, 0.3, 0.4, 0.5]
print('SINGLE_ARITHMETIC', crossover.single_arithmetic(parent1, parent2))
print('SIMPLE_ARITHMETIC', crossover.simple_arithmetic(parent1, parent2))
print('WHOLE_ARITHMETIC', crossover.whole_arithmetic(parent1, parent2))

# PGA
parent1 = [1, 2, 3, 4, 5]
parent2 = [5, 4, 1, 3, 2]
print('PMX', crossover.pmx(parent1, parent2))
print('ORDER1', crossover.order1(parent1, parent2))
