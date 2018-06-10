import xml.etree.ElementTree as ET
import random
import math


number_of_dest = 20
initial_temp = 1000
minimum_temp = 0
cooling_rate = 1
num_iterations = 10


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
    # print(f'home: {home}')
    # print(f'destinations: {destinations}')
    neighbourhood = build_neighbourhood(destinations)
    cost_dict = build_cost_dict(nodes)

    run_sa(nodes, cost_dict, neighbourhood)


def run_sa(nodes, cost_dict, neighbourhood):
    print('running SA......')
    print('======================================================================')
    # Set current temperature to an initial temperature t = t0
    current_temp = initial_temp
    # Set current solution to an initial solution s=s0
    path = nodes
    cost = 0
    for i in range(len(path)):
        cost += cost_dict[(path[i-1], path[i])]
    print(f'initial path: {path}')
    print(f'initial cost: {cost}')
    print('======================================================================')

    while current_temp > minimum_temp:
        for i in range(num_iterations):
            # Select a solution si from the neighborhood N (s)
            new_path, new_cost = select_a_solution(
                neighbourhood,
                # use the current temp and current iteration as an unique seed
                current_temp * num_iterations + i,
                path,
                cost_dict
            )
            # Calculate change in cost C according to the new solution
            cost_diff = new_cost - cost
            # If C < 0 then accept new solution (it is improving) -> s= si
            if cost_diff < 0:
                path = new_path
                cost = new_cost
            # Else generate a random number x in the range (0,1)
            else:
                x = random.random()
                # If x<e c/t then accept new solution s=si
                if x < calculate_acceptance_probability(current_temp, cost_diff):
                    path = new_path
                    cost = new_cost
        # Decrease t using alpha
        current_temp = decrement_temp(current_temp)

    print(f'final path: {path}')
    print(f'final cost: {cost}')


def select_a_solution(neighbourhood, seed, current_path, cost_dict):
    # use the current temp and current iteration as an unique seed
    random.seed(seed)
    # get a random neighbour from the neighbourhood
    neighbour = neighbourhood[random.randint(0, len(neighbourhood)-1)]
    # get the index of the first swapped node
    swap_first = current_path.index(neighbour[0])
    # get the index of the second swapped node
    swap_second = current_path.index(neighbour[1])
    # make the swap
    new_path = current_path
    temp = current_path[swap_first]
    new_path[swap_first] = current_path[swap_second]
    new_path[swap_second] = temp
    # calculate the new cost
    new_cost = 0
    for i in range(len(new_path)):
        new_cost += cost_dict[(new_path[i - 1], new_path[i])]
    return new_path, new_cost


def calculate_acceptance_probability(current_temp, cost_diff):
    return math.exp(- cost_diff / current_temp)


# Linear rule
def decrement_temp(current_temp):
    return current_temp - cooling_rate


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


if __name__ == '__main__':
    main()
