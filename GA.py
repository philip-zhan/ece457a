from enum import Enum


class Crossover(Enum):
    SINGLE_ARITHMETIC = 1
    SIMPLE_ARITHMETIC = 2
    WHOLE_ARITHMETIC = 3
    PMX = 4
    ORDER1 = 5
    CYCLE = 6

    def single_arithmetic(self, parent1, parent2):
        pass

    def simple_arithmetic(self, parent1, parent2):
        pass

    def whole_arithmetic(self, parent1, parent2):
        pass

    def pmx(self, parent1, parent2):
        pass

    def order1(self, parent1, parent2):
        pass

    def cycle(self, parent1, parent2):
        pass


def crossover(parent1, parent2, method):
    if method == Crossover.SINGLE_ARITHMETIC:
        method.single_arithmetic(parent1, parent2)
    elif method == Crossover.SIMPLE_ARITHMETIC:
        method.simple_arithmetic(parent1, parent2)
    elif method == Crossover.WHOLE_ARITHMETIC:
        method.whole_arithmetic(parent1, parent2)
    elif method == Crossover.PMX:
        method.pmx(parent1, parent2)
    elif method == Crossover.ORDER1:
        method.order1(parent1, parent2)
    elif method == Crossover.CYCLE:
        method.cycle(parent1, parent2)

