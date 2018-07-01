from enum import Enum, auto
import random


# parameters
alpha = 0.5


class Crossover(Enum):
    ONE_POINT = auto()
    N_POINT = auto()
    SINGLE_ARITHMETIC = auto()
    SIMPLE_ARITHMETIC = auto()
    WHOLE_ARITHMETIC = auto()
    PMX = auto()
    ORDER1 = auto()
    CYCLE = auto()

    def one_point(self, parent1, parent2):
        k = random.randint(len(parent1))
        child1 = parent1[:k] + parent2[k:]
        child2 = parent1[k:] + parent2[:k]
        return child1, child2

    def n_point(self, parent1, parent2):
        n = random.randint(len(parent1))
        child1 = parent1
        child2 = parent2
        for i in range(n):
            child1, child2 = self.one_point(child1, child2)
        return child1, child2

    def single_arithmetic(self, parent1, parent2):
        k = random.randint(len(parent1))
        child1 = parent1
        child1[k] = alpha * parent2[k] + (1 - alpha) * parent1[k]
        child2 = parent2
        child2[k] = alpha * parent1[k] + (1 - alpha) * parent2[k]
        return child1, child2

    def simple_arithmetic(self, parent1, parent2):
        k = random.randint(len(parent1))
        child1 = parent1[:k]
        child2 = parent2[:k]
        for i in range(k, len(parent1)):
            child1.append(alpha * parent2[i] + (1 - alpha) * parent1[i])
            child2.append(alpha * parent1[i] + (1 - alpha) * parent2[i])
        return child1, child2

    def whole_arithmetic(self, parent1, parent2):
        child1 = []
        child2 = []
        for i in range(len(parent1)):
            child1.append(alpha * parent1[i] + (1 - alpha) * parent2[i])
            child2.append(alpha * parent2[i] + (1 - alpha) * parent1[i])
        return child1, child2

    def pmx(self, parent1, parent2):
        pass

    def order1(self, parent1, parent2):
        pass

    def cycle(self, parent1, parent2):
        pass


def crossover(parent1, parent2, method):
    if len(parent1) != len(parent2):
        return None
    if method == Crossover.ONE_POINT:
        return method.one_point(parent1, parent2)
    if method == Crossover.SINGLE_ARITHMETIC:
        return method.single_arithmetic(parent1, parent2)
    if method == Crossover.SIMPLE_ARITHMETIC:
        return method.simple_arithmetic(parent1, parent2)
    if method == Crossover.WHOLE_ARITHMETIC:
        return method.whole_arithmetic(parent1, parent2)
    if method == Crossover.PMX:
        return method.pmx(parent1, parent2)
    if method == Crossover.ORDER1:
        return method.order1(parent1, parent2)
    if method == Crossover.CYCLE:
        return method.cycle(parent1, parent2)

