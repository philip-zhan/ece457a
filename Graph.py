import networkx as nx
import xml.etree.ElementTree as ET
import random
import matplotlib.pyplot as plt


class Graph:

    def main(self):
        map_name = 'map_uwaterloo.osm.xml'
        # generate graph from map
        graph, source, destination = self.get_graph(map_name)
        # draw_graph(graph, source, destination)
        self.breadth_first_search(graph, source, destination)
        for beam_width in range(2, 7):
            self.beam_search(graph, source, destination, beam_width)

    def get_graph(self, map_name):
        # parse the map file
        osm = ET.parse(map_name)
        root = osm.getroot()
        # max height of the drone in meters
        max_height = 120

        # get the boundary of the map
        bounds = root.find('bounds').attrib

        building_ways = self.get_building_ways(root)
        node_dict = self.get_node_dictionary(root)
        building_coords = self.get_building_coords(building_ways, node_dict, bounds)
        exclude_ranges = self.get_exclude_ranges(building_coords)
        edges = self.get_edges(bounds, max_height, exclude_ranges)
        source, destination = self.get_src_dest(edges)
        graph = self.build_graph(edges)
        return graph, source, destination
    
    def lon_to_x(self, lon, minlon):
        return int((float(lon) - float(minlon)) * 5000)

    def lat_to_y(self, lat, minlat):
        return int((float(lat) - float(minlat)) * 5000)

    def get_building_ways(self, root):
        building_ways = []
        for way in root.findall('./way/tag[@k="building:levels"]/..'):
            height = int(way.find('tag[@k="building:levels"]').attrib.get('v')) * 5
            nd_refs = []
            for nd in way.findall('nd'):
                nd_refs.append(nd.attrib.get('ref'))
            building_ways.append((nd_refs, height))
        # print 'building_ways[0]:', building_ways[0]
        # print 'len(building_ways):', len(building_ways)
        return building_ways

    def get_node_dictionary(self, root):
        node_dict = {}
        for node in root.findall('./node'):
            node_dict[node.attrib.get('id')] = (node.attrib.get('lat'), node.attrib.get('lon'))
        # print 'node_dict.items()[0]:', node_dict.items()[0]
        # print 'len(node_dict):', len(node_dict)
        return node_dict

    def get_building_coords(self, building_ways, node_dict, bounds):
        building_coords = []
        for way in building_ways:
            nd_coords = []
            height = way[1]
            for ref in way[0]:
                nd_coords.append((
                    self.lon_to_x(node_dict[ref][1], bounds['minlon']),
                    self.lat_to_y(node_dict[ref][0], bounds['minlat'])
                ))
            building_coords.append((height, nd_coords))
        # print 'building_coords[0]:', building_coords[0]
        # print 'len(building_coords):', len(building_coords)
        return building_coords

    def get_exclude_ranges(self, building_coords):
        exclude_ranges = []
        for building_nodes in building_coords:
            max_x = 0
            min_x = 99999
            max_y = 0
            min_y = 99999
            for building_node in building_nodes[1]:
                if building_node[0] < min_x:
                    min_x = building_node[0]
                elif building_node[0] > max_x:
                    max_x = building_node[0]
                if building_node[1] < min_y:
                    min_y = building_node[1]
                elif building_node[1] > max_y:
                    max_y = building_node[1]
            range_dict = {'min_x': min_x, 'max_x': max_x, 'min_y': min_y, 'max_y': max_y, 'z': building_nodes[0]}
            exclude_ranges.append(range_dict)
        # print 'exclude_ranges[0]:', exclude_ranges[0]
        # print 'len(exclude_ranges):', len(exclude_ranges)
        return exclude_ranges

    def get_edges(self, bounds, max_height, exclude_ranges):
        edges = []
        for x in range(self.lon_to_x(bounds['maxlon'], bounds['minlon'])):
            for y in range(self.lat_to_y(bounds['maxlat'], bounds['minlat'])):
                for z in range(max_height):
                    do_add = True
                    for exclude_range in exclude_ranges:
                        if(
                                z <= exclude_range['z'] and
                                exclude_range['min_x'] <= x <= exclude_range['max_x'] and
                                exclude_range['min_y'] <= y <= exclude_range['max_y']
                        ):
                            do_add = False
                            break
                    if do_add:
                        edges.append(((x, y, z), (x + 1, y, z)))
                        edges.append(((x, y, z), (x, y + 1, z)))
                        edges.append(((x, y, z), (x, y, z + 1)))
        # print 'edges[0]:', edges[0]
        # print 'len(edges):', len(edges)
        return edges

    def get_src_dest(self, edges):
        source = edges[random.randint(1, len(edges) - 1)][0]
        destination = edges[random.randint(1, len(edges) - 1)][0]
        print(f'source: {source}')
        print(f'destination: {destination}')
        return source, destination

    def build_graph(self, edges):
        graph = nx.Graph()
        graph.add_edges_from(edges)
        print('graph has been built')
        return graph

    def draw_graph(self, graph, source, destination):
        nodes_near_source = []
        for x in range(source[0] - 5, source[0] + 5):
            for y in range(source[1] - 5, source[1] + 5):
                for z in range(source[2] - 5, source[2] + 5):
                    nodes_near_source.append((x, y, z))
        nx.draw(graph.subgraph(nodes_near_source))
        plt.show()

    def breadth_first_search(self, graph, source, destination):
        path = []
        for edge in nx.bfs_edges(graph, source):
            if edge[1] != destination:
                path.append(edge[1])
            else:
                break
        print(f'breadth first search cost: {len(path)}')

    def beam_search(self, graph, source, destination, beam_width):
        print(f'doing beam search with beam width: {beam_width}')
        path = []
        for edge in nx.bfs_beam_edges(graph, source, lambda _: 1, beam_width):
            if edge[1] != destination:
                path.append(edge[1])
            else:
                break
        print(f'beam search cost: {len(path)}')


if __name__ == '__main__':
    Graph().main()
