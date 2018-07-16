import random


class Crossover:
    def __init__(self, alpha):
        self.alpha = alpha

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
        for i in range(1, len(parent1) - 1):
            coin = random.getrandbits(1)
            # print(coin, child1, child2)
            child1[i] = parents[coin][i]
            child2[i] = parents[1 - coin][i]
        return child1, child2

    def single_arithmetic(self, parent1, parent2):
        k = random.randrange(len(parent1))
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1[k] = self.alpha * parent2[k] + (1 - self.alpha) * parent1[k]
        child2[k] = self.alpha * parent1[k] + (1 - self.alpha) * parent2[k]
        return child1, child2

    def simple_arithmetic(self, parent1, parent2):
        k = random.randrange(len(parent1))
        child1 = parent1.copy()
        child2 = parent2.copy()
        for i in range(k + 1, len(parent1)):
            child1[i] = self.alpha * parent2[i] + (1 - self.alpha) * parent1[i]
            child2[i] = self.alpha * parent1[i] + (1 - self.alpha) * parent2[i]
        return child1, child2

    def whole_arithmetic(self, parent1, parent2):
        child1 = parent1.copy()
        child2 = parent2.copy()
        for i in range(len(parent1)):
            child1[i] = self.alpha * parent1[i] + (1 - self.alpha) * parent2[i]
            child2[i] = self.alpha * parent2[i] + (1 - self.alpha) * parent1[i]
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
        children = []
        print("parent is "+str(parent1)+" and "+str(parent2))
        for j in range(2):
            parent = parent1 if j == 0 else parent2
            otherParent = parent2 if parent == parent1 else parent1
            k = random.randrange(len(parent))
            length = random.randrange(len(parent))
            child = [None] * len(parent)
            for offset in range(length):
                child[(k+offset) % len(parent)] = parent[(k+offset) % len(parent)]
            print("k is "+str(k)+" length is "+str(length)+" child is "+str(child))
            start = (k+length) % (len(parent))
            parentIndex = start
            for j in range(len(otherParent)):
                parentElement = otherParent[parentIndex]
                parentIndex = (parentIndex + 1) % len(otherParent)
                if parentElement not in child:
                    child[start] = parentElement
                    start = (start + 1) % len(child)
            children.append(child)
        return children

    def cycle(self, parent1, parent2):
        pass
