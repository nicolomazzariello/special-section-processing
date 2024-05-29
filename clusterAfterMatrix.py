import argparse
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import networkx as nx
from cdlib import algorithms, viz
from scipy.stats import norm
import statistics

def edges_calc(file):

    df = pd.read_csv(file, sep='\t')
    df.drop(df[df['total'] == 1].index, inplace=True) #removing rows with no connections between tracks

    name_columns = df.columns.tolist()
    name_columns = name_columns[2:len(name_columns)-1] #to get only the tracks
    df = df[name_columns]

    list_columns= []

    for column in name_columns:
        list_columns.append(df[column].tolist())
    
    dictionary_columns = {a: b for a, b in zip(name_columns, list_columns)}

    graph_edges = []
    edges_weights = []
    intersection_values = []

    for track1, track2 in itertools.combinations(dictionary_columns.keys(), 2):
        
        intersection = 0

        for i, j in zip(dictionary_columns.get(track1), dictionary_columns.get(track2)):
            if i >= 2 and j >= 2:
                intersection+=1

        intersection_values.append(intersection)

        if intersection > 5:
            graph_edges.append((track1, track2))
            edges_weights.append(intersection)

    return name_columns, graph_edges, edges_weights, intersection_values

def nodes_calc(name_columns):
    nodes = []

    for node in name_columns:
        nodes.append(node)

    return nodes

def create_graph(nodes, edges, weights):
    plt.figure(figsize = (15, 10))
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    coms = algorithms.leiden(g, weights=weights)

    pos = nx.spring_layout(g, k=1)

    viz.plot_network_clusters(g, coms, pos, plot_labels=True, node_size=900)

    plt.savefig('clusterOnMatrix.png')
    plt.clf()

""" def create_intersectionHistogram(intersection_values):

    mean = statistics.mean(intersection_values)
    sd = statistics.stdev(intersection_values)

    print(mean, sd)

    mean, sd = norm.fit(intersection_values)

    print(mean, sd)

    plt.hist(intersection_values, density=True, bins=len(intersection_values), alpha=0.5)
    plt.plot(intersection_values, norm.pdf(intersection_values, mean, sd))

    plt.xlabel('intersections')
    plt.savefig('after_matrix_intersection_histogram.png')
    plt.clf() """

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='matrix')
    args = parser.parse_args()

    name_columns, graph_edges, edges_weights, intersection_values = edges_calc(args.file)
    nodes = nodes_calc(name_columns)
    create_graph(nodes, graph_edges, edges_weights)

    #create_intersectionHistogram(intersection_values)


if __name__ == '__main__':
    main()