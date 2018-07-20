import xml.etree.ElementTree as ET
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


number_of_dest = 10
num_iterations = 500

def main():
    map_name = 'map_uwaterloo.osm.xml'
    osm = ET.parse(map_name)
    root = osm.getroot()
    # get the boundary of the map
    bounds = root.find('bounds').attrib
    x_max = lon_to_x(bounds['maxlon'], bounds['minlon'])
    y_max = lat_to_y(bounds['maxlat'], bounds['minlat'])
    z_max = 100
    nodes = generate_nodes(x_max, y_max, z_max, number_of_dest + 1)
    home = nodes[0]
    destinations = nodes[1:]
    neighbourhood = build_neighbourhood(destinations)
    cost_dict = build_cost_dict(nodes)
    # Initial pheromone value for all edges
    pheromone_dict = build_pheromone_dict(nodes)

    # print(f'nodes: {nodes}')
    # print(f'home: {home}')
    # print(f'destinations: {destinations}')
    # print(f'neighbour hood: {neighbourhood}')
    # print(f'cost: {cost_dict}')
    # print(f'phermone: {pheromone_dict}')

    run_aco(nodes, cost_dict, neighbourhood, pheromone_dict, home)


def run_aco(nodes, cost_dict, neighbourhood, pheromone_dict, home):
    print('running ACO......')
    print('======================================================================')
    # Place M ants on the graph divided among all the nodes
    M = random.randint(len(nodes), 2*len(nodes))
    print(f'Ants amount: {M}')

    # Set current solution to an initial solution s=s0
    path = nodes
    cost = 0
    for i in range(len(path)):
        cost += cost_dict[(path[i-1], path[i])]
    print(f'initial path: {path}')
    print(f'initial cost: {cost}')
    print('======================================================================')
    # plot the initial path
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [node[0] for node in path]
    ys = [node[1] for node in path]
    zs = [node[2] for node in path]
    ax.plot(xs, ys, zs)
    plt.show()

    # do SA
    iter = 0
    while iter < num_iterations:
        for i in range(M):
            # Select a solution si from the neighborhood N (s)
            new_path, new_cost = select_a_solution(
                path,
                cost_dict,
                pheromone_dict,
                home
            )
            # pheromone evaporate
            for pheromone in pheromone_dict:
                pheromone_decay_rate = random.random()
                pheromone_dict[pheromone] *= (1-pheromone_decay_rate)
            # deposit extra pheromone
            for node1 in new_path:
                for node2 in new_path:
                    if node1 != node2:
                        pheromone_dict[(node1, node2)] += 100
            # record the lowest cost solution
            if cost > new_cost:
                path = new_path
                cost = new_cost
        iter = iter + 1
    # plot the final path
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [node[0] for node in path]
    ys = [node[1] for node in path]
    zs = [node[2] for node in path]
    ax.plot(xs, ys, zs)
    plt.show()

    print(f'final path: {path}')
    print(f'final cost: {cost}')


def select_a_solution(current_path, cost_dict, pheromone_dict, home):
    # initialize the tabu list and the new_path
    remaining_nodes = [node for node in current_path]
    remaining_nodes.remove(home)
    new_path = [home]
    start_node = home
    # stop until the new_path is filled
    while len(new_path) < len(current_path):
        # calculate the selection probability
        pheromone_list, cost_list = get_pheromone_and_cost(start_node, cost_dict, pheromone_dict, remaining_nodes)
        # print(f'cost_list: {cost_list}')
        # print(f'pheromone_list: {pheromone_list}')
        node_probability = {}
        max_prob = 0
        for key in pheromone_list:
            node_probability[key] = pheromone_list[key] / cost_list[key]
            if max_prob < node_probability[key]:
                node_to_visit = key[1]
                max_prob = node_probability[key]
        # remove visited node and append it to the new path and set it to be the start node
        new_path.append(node_to_visit)
        start_node = node_to_visit
        remaining_nodes.remove(node_to_visit)
    # print(f'new path: {new_path}')
    new_cost = 0
    for i in range(len(new_path)):
        new_cost += cost_dict[(new_path[i - 1], new_path[i])]
    return new_path, new_cost


def calculate_acceptance_probability(current_temp, cost_diff):
    return math.exp(- cost_diff / current_temp)


def lon_to_x(lon, min_lon):
    return int((float(lon) - float(min_lon)) * 10000)


def lat_to_y(lat, min_lat):
    return int((float(lat) - float(min_lat)) * 10000)


def generate_nodes(x_max, y_max, z_max, number):
    destinations = []
    for i in range(number):
        destinations.append(
            (int(x_max * random.random()), int(y_max * random.random()), int(z_max * random.random())))
    return destinations


def calculate_cost(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def build_neighbourhood(destinations):
    neighbourhood = []
    # while len(neighbourhood) <= neighbourhood_size:
    for i in range(len(destinations)):
        for j in range(i+1, len(destinations)):
            neighbourhood.append((destinations[i], destinations[j]))
    return neighbourhood


def build_cost_dict(nodes):
    cost_dict = {}
    for node1 in nodes:
        for node2 in nodes:
            if node1 != node2:
                cost_dict[(node1, node2)] = calculate_cost(node1, node2)
    return cost_dict


def build_pheromone_dict(nodes):
    pheromone_dict = {}
    for node1 in nodes:
        for node2 in nodes:
            if node1 != node2:
                pheromone_dict[(node1, node2)] = 100
    return pheromone_dict


def get_pheromone_and_cost(start_node, cost_dict, pheromone_dict, remaining_nodes):
    cost_result = {}
    pheromone_result = {}
    for node in remaining_nodes:
        if start_node != node:
            node_tuple = (start_node, node)
            cost_result[node_tuple] = cost_dict[node_tuple]
            pheromone_result[node_tuple] = pheromone_dict[node_tuple]
    return pheromone_result, cost_result

if __name__ == '__main__':
    main()
