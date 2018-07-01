from Crossover import Crossover

# SGA
parent1 = [0, 0, 0, 0, 0]
parent2 = [1, 1, 1, 1, 1]
print('ONE_POINT', Crossover.ONE_POINT.run(parent1, parent2))
print('N_POINT', Crossover.N_POINT.run(parent1, parent2))
print('UNIFORM', Crossover.UNIFORM.run(parent1, parent2))

# RGA
parent1 = [0, 0, 0, 0, 0]
parent2 = [0.1, 0.2, 0.3, 0.4, 0.5]
print('SINGLE_ARITHMETIC', Crossover.SINGLE_ARITHMETIC.run(parent1, parent2))
print('SIMPLE_ARITHMETIC', Crossover.SIMPLE_ARITHMETIC.run(parent1, parent2))
print('WHOLE_ARITHMETIC', Crossover.WHOLE_ARITHMETIC.run(parent1, parent2))

# PGA
parent1 = [1, 2, 3, 4, 5]
parent2 = [5, 4, 3, 2, 1]
print('PMX', Crossover.PMX.run(parent1, parent2))
