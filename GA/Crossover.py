from enum import Enum, auto
import random


# parameters
alpha = 0.5


class Crossover(Enum):
    ONE_POINT = auto()
    N_POINT = auto()
    UNIFORM = auto()
    SINGLE_ARITHMETIC = auto()
    SIMPLE_ARITHMETIC = auto()
    WHOLE_ARITHMETIC = auto()
    PMX = auto()
    ORDER1 = auto()
    CYCLE = auto()

    def run(self, parent1, parent2):
        if len(parent1) != len(parent2):
            return None
        if self is self.ONE_POINT:
            return self.one_point(parent1, parent2)
        if self is self.N_POINT:
            return self.n_point(parent1, parent2)
        if self is self.UNIFORM:
            return self.uniform(parent1, parent2)
        if self is self.SINGLE_ARITHMETIC:
            return self.single_arithmetic(parent1, parent2)
        if self is self.SIMPLE_ARITHMETIC:
            return self.simple_arithmetic(parent1, parent2)
        if self is self.WHOLE_ARITHMETIC:
            return self.whole_arithmetic(parent1, parent2)
        if self is self.PMX:
            return self.pmx(parent1, parent2)
        if self is self.ORDER1:
            return self.order1(parent1, parent2)
        if self is self.CYCLE:
            return self.cycle(parent1, parent2)

    def one_point(self, parent1, parent2):
        k = random.randrange(len(parent1))
        child1 = parent1[:k] + parent2[k:]
        child2 = parent2[:k] + parent1[k:]
        return child1, child2

    def n_point(self, parent1, parent2):
        n = random.randrange(len(parent1))
        child1 = parent1.copy()
        child2 = parent2.copy()
        for i in range(n):
            child1, child2 = self.one_point(child1, child2)
        return child1, child2

    def uniform(self, parent1, parent2):
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1[-1] = parent2[-1]
        child2[-1] = parent1[-1]
        # print(parent1, parent2, child1, child2)
        parents = [parent1, parent2]
        for i in range(1, len(parent1)-1):
            coin = random.getrandbits(1)
            # print(coin, child1, child2)
            child1[i] = parents[coin][i]
            child2[i] = parents[1-coin][i]
        return child1, child2

    def single_arithmetic(self, parent1, parent2):
        k = random.randrange(len(parent1))
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1[k] = alpha * parent2[k] + (1 - alpha) * parent1[k]
        child2[k] = alpha * parent1[k] + (1 - alpha) * parent2[k]
        return child1, child2

    def simple_arithmetic(self, parent1, parent2):
        k = random.randrange(len(parent1))
        child1 = parent1.copy()
        child2 = parent2.copy()
        for i in range(k+1, len(parent1)):
            child1[i] = alpha * parent2[i] + (1 - alpha) * parent1[i]
            child2[i] = alpha * parent1[i] + (1 - alpha) * parent2[i]
        return child1, child2

    def whole_arithmetic(self, parent1, parent2):
        child1 = parent1.copy()
        child2 = parent2.copy()
        for i in range(len(parent1)):
            child1[i] = alpha * parent1[i] + (1 - alpha) * parent2[i]
            child2[i] = alpha * parent2[i] + (1 - alpha) * parent1[i]
        return child1, child2

    def pmx(self, parent1, parent2):
        length = len(parent1)
        start = random.randrange(length)
        stop = random.randrange(start, length)
        # print(start, stop)
        child1 = [None] * start + parent1[start:stop] + \
            [None] * (length - stop)
        child2 = [None] * start + parent2[start:stop] + \
            [None] * (length - stop)
        # print(child1, child2)
        for i in range(start, stop):
            if parent2[i] not in child1:
                j = i
                k = parent2.index(parent1[j])
                while child1[k] is not None:
                    j = k
                    k = parent2.index(parent1[j])
                child1[k] = parent2[i]
            if parent1[i] not in child2:
                j = i
                k = parent1.index(parent2[j])
                while child2[k] is not None:
                    j = k
                    k = parent1.index(parent2[j])
                child2[k] = parent1[i]
        for i in range(length):
            if child1[i] is None:
                child1[i] = parent2[i]
            if child2[i] is None:
                child2[i] = parent1[i]
        return child1, child2

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
