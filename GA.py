from enum import Enum
import random


# parameters
alpha = 0.5


class Crossover(Enum):
    SINGLE_ARITHMETIC = 1
    SIMPLE_ARITHMETIC = 2
    WHOLE_ARITHMETIC = 3
    PMX = 4
    ORDER1 = 5
    CYCLE = 6

    def single_arithmetic(self, parent1, parent2):
        k = random.randrange(len(parent1))
        child1 = parent1
        child1[k] = alpha * parent2[k] + (1 - alpha) * parent1[k]
        child2 = parent2
        child2[k] = alpha * parent1[k] + (1 - alpha) * parent2[k]
        return child1, child2

    def simple_arithmetic(self, parent1, parent2):
        k = random.randrange(len(parent1))
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
        k = random.randrange(len(parent1))
        length = random.randrange(len(parent1))
        child = parent1
        start = (k+length) % (len(parent1)-1)
        childIndex = start
        for i in range(len(parent2)):
            parentIndex = (start+i) % (len(parent2)-1)
            if parent2[parentIndex] not in child:
                child[childIndex] = parent2[parentIndex]
                childIndex = (childIndex + 1) % (len(parent1)-1)
        return child

    def cycle(self, parent1, parent2):
        pass


def crossover(parent1, parent2, method):
    if len(parent1) != len(parent2):
        return None
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

