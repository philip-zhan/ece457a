import xml.etree.ElementTree as ET
import random
import math


def main():
    map_name = 'map_uwaterloo.osm.xml'
    number_of_dest = 20
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
    run_tabu(nodes, 10, 1000)


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


def run_tabu(nodes, tenure, max_iteration):
    print('running tabu')
    # build the cost dictionary {((0, 1), 7), ((0, 2), 5), ((0, 3), 4)...}
    cost_dict = {}
    for node1 in nodes:
        for node2 in nodes:
            if node1 != node2:
                cost_dict[(node1, node2)] = calculate_cost(node1, node2)

    # calculate the initial cost
    path = nodes
    cost = 0
    for i in range(len(path)):
        cost += cost_dict[(path[i-1], path[i])]
    print(f'old path: {path}')
    print(f'old cost: {cost}')

    neighbourhood = build_neighbourhood(nodes[1:])
    # print(f'neighbourhood: {neighbourhood}')

    iteration = 0
    tabu_list = {}
    while iteration < max_iteration:
        new_cost, new_path, swap_pair = search_neighbour(cost, path, neighbourhood, cost_dict, tabu_list, iteration)
        if new_cost < cost:  # swapped
            tabu_list[swap_pair] = iteration + tenure
            cost = new_cost
            path = new_path
        iteration += 1
        # print(f'tabu list: {tabu_list}')
    print(f'new path: {path}')
    print(f'new cost: {cost}')


def build_neighbourhood(nodes):
    neighbourhood = []
    # while len(neighbourhood) <= neighbourhood_size:
    for node1 in nodes:
        for node2 in nodes:
            neighbourhood.append((node1, node2))
    return neighbourhood


def search_neighbour(prev_cost, path, neighbourhood, cost_dict, tabu_list, iteration):
    # prev_path = path
    new_path = path
    lowest_cost = prev_cost
    best_neighbour = (0, 0)
    best_neighbour_indices = (0, 0)
    # swapped_pairs = []
    for neighbour in neighbourhood:  # (1,2)
        if neighbour in tabu_list and tabu_list[neighbour] > iteration:
            continue
        swap_first = path.index(neighbour[0])
        swap_second = path.index(neighbour[1])
        # print(f'path: {path}')
        # print(f'swap_first: {swap_first}')
        # print(f'swap_second: {swap_second}')
        # print(f'cost_dict: {cost_dict}')
        # print(f'(path[swap_first], path[swap_second + 1]): {(path[swap_first], path[swap_second + 1])}')
        # do a temporary swap
        temp_path = path
        temp = path[swap_first]
        temp_path[swap_first] = path[swap_second]
        temp_path[swap_second] = temp
        new_cost = 0
        for i in range(len(temp_path)):
            new_cost += cost_dict[(temp_path[i-1], temp_path[i])]
        # new_cost = prev_cost \
        #     - cost_dict[(path[swap_first - 1], path[swap_first])] \
        #     - cost_dict[(path[swap_first], path[swap_first + 1])] \
        #     - cost_dict[(path[swap_second - 1], path[swap_second])] \
        #     - cost_dict[(path[swap_second], path[swap_second + 1])] \
        #     + cost_dict[(path[swap_first - 1], path[swap_second])] \
        #     + cost_dict[(path[swap_second], path[swap_first + 1])] \
        #     + cost_dict[(path[swap_second - 1], path[swap_first])] \
        #     + cost_dict[(path[swap_first], path[swap_second + 1])]
        # print('==================================')
        if new_cost < lowest_cost:
            # best_neighbour_indices = (swap_first, swap_second)
            lowest_cost = new_cost
            new_path = temp_path
            best_neighbour = neighbour
    # if lowest_cost < prev_cost:  # found best swap
    #     temp = path[best_neighbour_indices[0]]
    #     new_path[best_neighbour_indices[0]] = new_path[best_neighbour_indices[1]]
    #     new_path[best_neighbour_indices[1]] = temp
        # swapped_pairs = path[best_neighbour_indices[0]], path[best_neighbour_indices[1]]
        #         new_path = path
        # old_cost = cost_dict{(neighbour[0], path[path.index(neighbour[0])-1])} +
        #
        #
        # for i in range(1, len(path)):
        #     if new_path[i] == neighbour[0]:  # node is being swapped
        #         # add the cost from previous node to swapped node
        #         new_cost += cost_dict[(new_path[i-1], new_path[neighbour[1]])]
        #         new_path[i] = neighbour[1]  # make the swap
        #     elif new_path[i] == neighbour[1]:  # node is being swapped
        #         new_cost += cost_dict[(new_path[i-1], new_path[neighbour[0]])]
        #         new_path[i] = neighbour[0]
        #     else:
        #         new_cost += cost_dict[(new_path[i-1], new_path[i])]
        # new_cost += cost_dict(0, new_path[-1])  # add the cost from the last destination to home
        # if new_cost < lowest_cost:
        #     lowest_cost = new_cost
        #     best_neighbour = neighbour
    return lowest_cost, new_path, best_neighbour


if __name__ == '__main__':
    main()
