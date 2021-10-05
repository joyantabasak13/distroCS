import os
# %matplotlib inline
import matplotlib.pyplot as plt
import networkx as nx
from entry_class import Entry


# Input Format
# #* --- paperTitle
# #@ --- Authors
# #t ---- Year
# #c  --- publication venue
# #index 00---- index id of this paper
# #% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
# #! --- Abstract


def generate_entry_list(path_data):
    in_file = open(path_data, 'r')
    lines = in_file.readlines()
    entry_count = 0
    authors = ""
    venue = ""
    title = ""
    index = 0
    year = 0
    entry_list = []

    # Strips the newline character
    for line in lines:
        if line == '\n':
            # Create Entry
            entry_list.append(Entry(title, year, authors, venue, index))
            # reinitialize variables
            authors = ""
            venue = ""
            title = ""
            index = 0
            year = 0
            # Increase Block Count
            entry_count += 1
        prefix = line.strip()[:2]
        if prefix == "#*":
            title = line.strip()[2:]
        elif prefix == "#@":
            authors = line.strip()[2:]
        elif prefix == "#t":
            year = int(line.strip()[2:])
        elif prefix == "#c":
            venue = line.strip()[2:]
        elif line.strip()[:6] == "#index":
            index = int(line.strip()[6:])
        if (entry_count > 1000):
            print("Entries Complete: {}".format(entry_count))
            break

    print("Total Entries: {}".format(entry_count))
    return entry_list


def write_graph(path_out, g_out):
    nx.write_adjlist(g_out, path_out)
    nx.write_gexf(g_out, path_out)


def read_graph(path_in):
    g_in = nx.Graph()
    nx.read_adjlist(g_in, path_in)
    return g_in


def generate_graph(entries):
    graph_gen = nx.Graph()
    for entry in entries:
        if len(entry.author_list) > 0:
            graph_gen.add_nodes_from(entry.author_list)
            if entry.title:
                graph_gen.add_node(entry.title)
                for author in entry.author_list:
                    graph_gen.add_edge(author, entry.venue)
            if entry.venue:
                graph_gen.add_node(entry.venue)
                for author in entry.author_list:
                    graph_gen.add_edge(author, entry.venue)
                graph_gen.add_edge(entry.title, entry.venue)
            if entry.year:
                graph_gen.add_node(entry.year)
                graph_gen.add_edge(entry.title, entry.year)
    return graph_gen


if __name__ == '__main__':
    path_d = os.path.abspath("./Data/outputacm.txt")
    path_graph = os.path.abspath("./Data/graph")
    entry_list = generate_entry_list(path_d)
    graph = generate_graph(entry_list)
    write_graph(path_graph, graph)
    #graph = read_graph(path_graph)
    print("#Edges: {}".format(graph.number_of_edges()))
    print("#Nodes: {}".format(graph.number_of_nodes()))
