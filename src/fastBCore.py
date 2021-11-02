import os
import networkx as nx
import matplotlib.pyplot as plt
import main as mn
import json


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


def clear_labeling(graph):
    for (n1, n2, d) in graph.edges(data=True):
        d.clear()


def dsl_util(graph, k, root, paths, node, visited, visited_edges, metapath, val, path, counter):
    visited.add(node)
    path.append(node)

    if counter >= len(metapath):
        if root != node:
            val = val + 1
            if root in paths:
                paths[root].append(path.copy())
            else:
                paths[root] = []
                paths[root].append(path.copy())
            path.pop()
            return val, paths
        else:
            path.pop()
            return val, paths
    if val >= k:
        path.pop()
        return val, paths
    for neighbour in graph.neighbors(node):
        edge_tuple = (node, neighbour)
        if (neighbour not in visited) or (edge_tuple not in visited_edges):
            if graph.nodes[neighbour]['type'] == metapath[counter]:
                visited_edges.add(edge_tuple)
                val, paths = dsl_util(graph, k, root, paths, neighbour, visited, visited_edges, metapath, val, path, counter + 1)
    path.pop()
    return val, paths


def dsl(graph, queryNSet, metapath, k_core):
    low_k_nodes = set()
    node_paths = dict()
    for node in queryNSet:
        visited = set()
        visited_edges = set()
        paths = dict()
        val, paths = dsl_util(graph, k_core, node, paths, node, visited, visited_edges, metapath, 0, [], 1)
        if val < k_core:
            low_k_nodes.add(node)
        if node in node_paths:
            node_paths[node].append(paths)
        else:
            node_paths[node] = paths
    print("DSL Results")
    print(low_k_nodes)
    print(node_paths.keys())

    for key, value in node_paths.items():
        print(key, value)
    return low_k_nodes, node_paths


def find_new_path_util(graph, visited, root, node, metapath, path, counter, forbidden_destination, existing_paths,
                       has_found_new_path):
    if has_found_new_path:
        return has_found_new_path
    visited.add(node)
    path.append(node)
    if counter >= len(metapath):
        if (node != forbidden_destination) and (path not in existing_paths):
            has_found_new_path = True
            return has_found_new_path
        path.pop()
        return has_found_new_path

    for neighbour in graph.neighbors(node):
        if neighbour not in visited:
            if graph.nodes[neighbour]['type'] == metapath[counter]:
                has_found_new_path = find_new_path_util(graph, visited, root, neighbour, metapath, path,
                                                               counter + 1, forbidden_destination, existing_paths,
                                                               has_found_new_path)
                if has_found_new_path:
                    return has_found_new_path
    if not has_found_new_path:
        path.pop()
    return has_found_new_path


def find_new_path(graph, source, metapath, forbidden_destination, existing_paths):
    visited = set()
    path = []
    has_found_new_path = find_new_path_util(graph, visited, source, source, metapath, path, 1, forbidden_destination,
                                            existing_paths, False)
    return has_found_new_path, path


def kcore_refinement(graph, low_k_nodes, node_paths, S, metapath, k_core):
    while len(low_k_nodes) > 0:
        v = low_k_nodes.pop()
        if v in S:
            S.remove(v)
        else:
            continue
        U = []
        path_v_u = dict()

        for path in node_paths[v][v]:
            U.append(path[len(metapath) - 1])
            path_v_u[path[len(metapath) - 1]] = path

        for u in U:
            if path_v_u[u] is not None:
                if list(reversed(path_v_u[u])) in node_paths[u][u]:
                    node_paths[u][u].remove(list(reversed(path_v_u[u])))

                if len(node_paths[u][u]) < k_core:
                    has_found_new_path, new_path = find_new_path(graph, u, metapath, v, node_paths[u][u])
                    if has_found_new_path:
                        node_paths[u][u].append(new_path)
                    else:
                        low_k_nodes.add(u)

    return S


if __name__ == '__main__':
    graph, query, metapath, k_core = take_inputs()
    k_core = 3
    nx.draw(graph, with_labels=True)
    plt.savefig("sampleGraph.png")
    if query != 0:
        # initialize graph labels
        nx.set_edge_attributes(graph, values=-1, name='label')
        S = bsl(graph, query, metapath)
        print("S is {}".format(S))
        clear_labeling(graph)
        low_k_nodes, node_paths = dsl(graph, S, metapath, k_core)
        print("Low K Nodes {}".format(low_k_nodes))
        kcore_vertices = kcore_refinement(graph, low_k_nodes, node_paths, S, metapath, k_core)
        print("Final Candidates: {}".format(kcore_vertices))
