from Crossover import Crossover

# SGA tests
parent1 = [0, 0, 0, 0, 0, 0]
parent2 = [1, 1, 1, 1, 1, 1]
print('ONE_POINT', Crossover.ONE_POINT.run(parent1, parent2))
print('N_POINT', Crossover.N_POINT.run(parent1, parent2))
print('UNIFORM', Crossover.UNIFORM.run(parent1, parent2))

# RGA rests
parent1 = [0, 0, 0, 0, 0, 0]
parent2 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
print('SINGLE_ARITHMETIC', Crossover.SINGLE_ARITHMETIC.run(parent1, parent2))
print('SIMPLE_ARITHMETIC', Crossover.SIMPLE_ARITHMETIC.run(parent1, parent2))
print('WHOLE_ARITHMETIC', Crossover.WHOLE_ARITHMETIC.run(parent1, parent2))
