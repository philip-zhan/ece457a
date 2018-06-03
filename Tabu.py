import xml.etree.ElementTree as ET
import random
import math


def main():
    map_name = 'map_uwaterloo.osm.xml'
    number_of_dest = 5
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
    print(f'home: {home}')
    print(f'destinations: {destinations}')


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


def run_tabu(nodes, neighbourhood_size, tenure):
    # build the cost dictionary {((0, 0), 0), ((0, 1), 7), ((0, 2), 5), ((0, 3), 4)...}
    cost_dict = {}
    for i in range(nodes):
        for j in range(nodes):
            cost_dict[(i, j)] = calculate_cost(nodes[i], nodes[j])

    # calculate the initial cost
    path = range(len(nodes))
    cost = cost_dict[(0, len(nodes))]
    for i in range(len(nodes) - 1):
        cost += cost_dict[(i, i+1)]

    neighbourhood = build_neighbourhood(neighbourhood_size, nodes)


def build_neighbourhood(neighbourhood_size, nodes):
    # build the neighbourhood list [(1, 2), (1, 3) , (1, 4)...]
    neighbourhood = []
    while len(neighbourhood) <= neighbourhood_size:
        for i in range(1, len(nodes)):
            for j in range(i+1, len(nodes)):
                neighbourhood.append(i, j)
    return neighbourhood


def find_best_neighbour(cost, neighbourhood, path, cost_dict):
    lowest_cost = cost
    best_neighbour = (0, 0)
    for neighbour in neighbourhood:
        new_cost = 0
        new_path = path
        for i in range(1, len(path)):
            if new_path[i] == neighbour[0]:  # node is being swapped
                new_cost += cost_dict[(new_path[i-1], new_path[neighbour[1]])]  # add the cost from previous node to swapped node
                new_path[i] = neighbour[1]  # make the swap
            elif new_path[i] == neighbour[1]:  # node is being swapped
                new_cost += cost_dict[(new_path[i-1], new_path[neighbour[0]])]
                new_path[i] = neighbour[0]
            else:
                new_cost += cost_dict[(new_path[i-1], new_path[i])]
        new_cost += cost_dict(0, new_path[-1])  # add the cost from the last destination to home
        if new_cost < lowest_cost:
            lowest_cost = new_cost
            best_neighbour = neighbour
    return best_neighbour


if __name__ == '__main__':
    main()
