import os
import networkx as nx
from entry_class import Entry
import main as mn


def take_inputs():
    # input 1 graph
    graph = mn.get_graph()
    print("#Edges: {}".format(graph.number_of_edges()))
    print("#Nodes: {}".format(graph.number_of_nodes()))
    # input file read
    input_file_path = os.path.abspath("../Data/query_input.txt")
    input_file = open(input_file_path, 'r')
    lines = input_file.readlines()
    for line in lines:
        prefix = line.strip()[:2].strip()
        if prefix == "#q":
            query = line.strip()[2:].strip()
        elif prefix == "#m":
            metapath_line = line.strip()[2:].strip()
        elif prefix == "#k":
            kcore = int(line.strip()[2:].strip())

    # query q
    print("QUERY: {}".format(query))
    if graph[query]:
        query_type = graph.nodes[query]['type']
        print("QUERY TYPE: {}".format(query_type))
    else:
        print("Unknown QUERY: {}".format(query))
        query = 0
    # metapath m
    metapath = [x.strip() for x in metapath_line.split(',')]
    print("Metapath: \n {}".format(metapath))
    # kcore k
    print("Kcore: {}".format(kcore))

    return graph, query, metapath, kcore


def bsl(graph, query):
    s = set()
    x = set()
    x.add(str(graph[query]))
    return s


if __name__ == '__main__':
    graph, query, metapath, kcore = take_inputs()
    if query != 0:
        s = bsl(graph, query)


