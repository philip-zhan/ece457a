from Crossover import Crossover
from Mutation import Mutation
from Util import *
import numpy as np
import random


crossover = Crossover(alpha=0.7)
mutation = Mutation(mutation_rate=0.1)
number_of_dest = 8
max_generation = 2000
population_size = 100


def main():
    nodes = get_nodes('../map_uwaterloo.osm.xml', number_of_dest)
    population = []
    lowest_cost = get_solution_cost(nodes)
    best_solution = nodes
    print("initial solution: ", nodes)
    print("initial cost: ", lowest_cost)
    for i in range(population_size):
        copy = list.copy(nodes)
        random.shuffle(copy)
        population.append(copy)
    print('running GA......')
    print('======================================================================')
    for generation in range(max_generation):
        # print("generation: ", generation)
        parents = select_parents(population)
        children = apply_crossover(parents)
        children = mutate_offspring(children)
        population, cost = select_offspring(population + children)
        if cost < lowest_cost:
            lowest_cost = cost
            best_solution = population[0]
        # print("lowest cost: ", lowest_cost)
    print('======================================================================')
    print("finished GA")
    print("solution: ", best_solution, "cost: ", lowest_cost)
    plot(best_solution)


def select_parents(population):
    random.shuffle(population)
    return population


def get_solution_cost(solution):
    cost = 0
    for i in range(len(solution)):
        cost += get_cost(solution[i - 1], solution[i])
    return cost


def evaluate(population):
    solution_cost = []
    for solution in population:
        solution_cost.append((solution, get_solution_cost(solution)))
    return solution_cost


def apply_crossover(parents):
    children = []
    for i in range(len(parents)):
        child1, child2 = crossover.pmx(parents[i-1], parents[i])
        children.append(child1)
        children.append(child2)
    return children


def mutate_offspring(children):
    for i in range(len(children)):
        children[i] = mutation.swap(children[i])
    return children


def select_offspring(children):
    solution_cost = evaluate(children)
    sorted(solution_cost, key=lambda child_cost: child_cost[1])
    lowest_cost = solution_cost[0][1]
    offspring = [item[0] for item in solution_cost[:population_size]]
    return offspring, lowest_cost


if __name__ == '__main__':
    main()
