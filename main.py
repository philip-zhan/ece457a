import networkx as nx
import xml.etree.ElementTree as ET
import random


def main():
    map_name = 'map_uwaterloo.osm.xml'
    osm = ET.parse(map_name)
    root = osm.getroot()
    max_height = 120

    bounds = root.find('bounds').attrib
    # print(float(bounds['minlon']))

    building_ways = []
    for way in root.findall('./way/tag[@k="building:levels"]/..'):
        height = int(way.find('tag[@k="building:levels"]').attrib.get('v')) * 5
        nd_refs = []
        for nd in way.findall('nd'):
            nd_refs.append(nd.attrib.get('ref'))
        building_ways.append((nd_refs, height))

    nodes = {}
    for node in root.findall('./node'):
        nodes[node.attrib.get('id')] = (node.attrib.get('lat'), node.attrib.get('lon'))

    # print(nodes)
    # print(len(nodes))

    building_coords = []
    for way in building_ways:
        nd_coords = []
        height = way[1]
        for ref in way[0]:
            nd_coords.append((
                lon_to_x(nodes[ref][1], bounds['minlon']),
                lat_to_y(nodes[ref][0], bounds['minlat'])
            ))
        building_coords.append((height, nd_coords))
    # print(building_coords)
    # print(len(building_coords))

    exclude_ranges = []
    for building_nodes in building_coords:
        max_x = 0
        min_x = 10000
        max_y = 0
        min_y = 10000
        for building_node in building_nodes[1]:
            if building_node[0] < min_x:
                min_x = building_node[0]
            elif building_node[0] > max_x:
                max_x = building_node[0]

            if building_node[1] < min_y:
                min_y = building_node[1]
            elif building_node[1] > max_y:
                max_y = building_node[1]

        dict = {'min_x': min_x, 'max_x': max_x, 'min_y': min_y, 'max_y': max_y, 'z': building_nodes[0]}
        exclude_ranges.append(dict)

    # print(exclude_ranges)
    # print(len(exclude_ranges))

    edges = []
    for x in range(lon_to_x(bounds['maxlon'], bounds['minlon'])):
        for y in range(lat_to_y(bounds['maxlat'], bounds['minlat'])):
            for z in range(max_height):
                do_add = True
                for exclude_range in exclude_ranges:
                    if(
                            z <= exclude_range['z'] and
                            x >= exclude_range['min_x'] and x <= exclude_range['max_x'] and
                            y >= exclude_range['min_y'] and y <= exclude_range['max_y']
                    ):
                        do_add = False
                        break
                if do_add:
                    edges.append(((x, y, z), (x, y, z + 1)))
                    edges.append(((x, y, z), (x, y + 1, z)))
                    edges.append(((x, y, z), (x + 1, y, z)))

    # print(edges)
    # print(len(edges))

    warehouse = edges[random.randint(1, len(edges) - 1)][0]
    destination = edges[random.randint(1, len(edges) - 1)][0]

    print('warehose: ', warehouse)
    print('destination: ', destination)

    G = nx.Graph()
    G.add_edges_from(edges)
    print('graph is built')
    # print(G.nodes)

    path = []
    for edge in nx.bfs_edges(G, warehouse):
        if edge[1] != destination:
            path.append(edge)
        else:
            break
    print(len(path))

    # for way in root.iter('way'):
    #     for tag in way.iter('tag'):
    #         # print(tag.attrib)
    #         k = tag.attrib.get('k')
    #         v = tag.attrib.get('v')
    #         if k == 'building:levels':
    #             print(k, v)


def lon_to_x(lon, minlon):
    return int((float(lon) - float(minlon)) * 5000)


def lat_to_y(lat, minlat):
    return int((float(lat) - float(minlat)) * 5000)


if __name__ == '__main__':
    main()
