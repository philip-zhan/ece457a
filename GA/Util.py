import random
import math
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from mpl_toolkits.mplot3d import Axes3D


cost_dict = {}


def get_nodes(map_name, number_of_dest):
    osm = ET.parse(map_name)
    root = osm.getroot()
    # get the boundary of the map
    bounds = root.find('bounds').attrib
    x_max = lon_to_x(bounds['maxlon'], bounds['minlon'])
    y_max = lat_to_y(bounds['maxlat'], bounds['minlat'])
    z_max = 100
    nodes = generate_nodes(x_max, y_max, z_max, number_of_dest + 1)
    return nodes


def get_cost(a, b):
    # print("cost dict", cost_dict)
    if (a, b) in cost_dict:
        return cost_dict[(a, b)]
    else:
        cost = calculate_cost(a, b)
        cost_dict[(a, b)] = cost
        # print("new cost", cost)
        return cost


def plot(path):
    # plot the final path
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [node[0] for node in path]
    ys = [node[1] for node in path]
    zs = [node[2] for node in path]
    ax.plot(xs, ys, zs)
    plt.show()


def lon_to_x(lon, min_lon):
    return int((float(lon) - float(min_lon)) * 10000)


def lat_to_y(lat, min_lat):
    return int((float(lat) - float(min_lat)) * 10000)


def generate_nodes(x_max, y_max, z_max, number):
    destinations = []
    for i in range(number):
        node = int(x_max * random.random()), int(y_max * random.random()), int(z_max * random.random())
        destinations.append(node)
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


# def build_cost_dict(nodes):
#     cost_dict = {}
#     for node1 in nodes:
#         for node2 in nodes:
#             if node1 != node2:
#                 cost_dict[(node1, node2)] = calculate_cost(node1, node2)
#     return cost_dict
