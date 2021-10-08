import os
import networkx as nx
import matplotlib.pyplot as plt
import main as mn


def take_inputs():
    # input 1 graph
    graph = mn.get_graph()
    print("#Edges: {}".format(graph.number_of_edges()))
    print("#Nodes: {}".format(graph.number_of_nodes()))
    # input file read
    input_file_path = os.path.abspath("../DataSmol/query_input.txt")
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
    if graph.nodes[query]:
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


def bsl(graph, query, metapath):
    S = set()
    x = set()
    x.add(query)
    count = 1
    while len(x) > 0:
        print("Metapath Iter: {}".format(count))
        for i in range(len(metapath) - 1):
            y = set()
            for v in x:
                for u in graph.neighbors(v):
                    if (graph.nodes[v]['type'] == metapath[i]) and (graph.nodes[u]['type'] == metapath[i + 1]):
                        if graph[v][u]['label'] == -1:
                            y.add(str(u))
                            graph[v][u]['label'] = i
            x = y
        count += 1
        x = x.difference(S)
        S = S.union(x)

    return S


if __name__ == '__main__':
    graph, query, metapath, kcore = take_inputs()
    nx.draw(graph, with_labels = True)
    plt.savefig("sampleGraph.png")
    if query != 0:
        # initialize grap labels
        nx.set_edge_attributes(graph, values=-1, name='label')
        S = bsl(graph, query, metapath)
        print("S is {}".format(S))
