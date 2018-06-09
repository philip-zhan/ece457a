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
        neighbourhood = build_neighbourhood(destinations)


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
