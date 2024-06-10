import csv
import argparse
import itertools
import matplotlib.pyplot as plt
import networkx as nx
from cdlib import algorithms, viz

# Lettura del file csv con i Track paper
def read_csv(file):

    with open(file, 'r', encoding='utf-8') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter='\t')

        doc = []

        for item in csv_reader:
            doc.append(item)

    return doc

# Calcolo dei lati e del loro peso (numero di parole in comune tra gli abstract_filtered di due Track paper)
def edges_calc(doc):
    graph_edges = []
    edges_weights = []
    intersection_values = []

    for paper1, paper2 in itertools.combinations(doc, 2):
        intersection = len(set(paper1['abstract_filtered'].lower().split()).intersection(set(paper2['abstract_filtered'].lower().split())))
        intersection_values.append(intersection)
        if intersection > 35:
            graph_edges.append((paper1['id'], paper2['id']))
            edges_weights.append(intersection)

    return graph_edges, edges_weights, intersection_values

# Inserimento dei nodi all'interno del grafo
def nodes_calc(doc):
    nodes = []

    for d in doc:
        nodes.append(d['id'])

    return nodes

# Creazione del grafo
def create_graph(nodes, edges, weights):
    plt.figure(figsize = (15, 10))
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    coms = algorithms.leiden(g, weights=weights)

    pos = nx.spring_layout(g, k=1)

    viz.plot_network_clusters(g, coms, pos, plot_labels=True, node_size=900)

    """ communities = nx.community.greedy_modularity_communities(g)

    supergraph = nx.cycle_graph(len(communities))
    superpos = nx.spring_layout(g, scale=50, seed=429)

    # Use the "supernode" positions as the center of each node cluster
    centers = list(superpos.values())
    pos = {}
    for center, comm in zip(centers, communities):
        pos.update(nx.spring_layout(nx.subgraph(g, comm), k=40, center=center, seed=1430, weight='weight'))

    nx.draw(g, pos, with_labels=True, node_color='orange', node_size=900, edge_color=['red' if weight > 6 else 'blue' for weight in weights])
    a_dict = {a: b for a, b in zip(edges, weights)}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=a_dict)

    #pos = nx.spring_layout(g, weight='weight', k=1) """
        
    """ nx.draw(g, pos, with_labels=True, node_size=900)
    a_dict = {a: b for a, b in zip(edges, weights)}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=a_dict) """

    plt.savefig('BiggestPaper_graph.png')
    plt.clf()

#istogramma delle intersezioni (parole comuni tra paper) (asse x il numero di parole comuni, asse y la ricorrenza di tale numero)
def create_intersectionHistogram(intersection_values):
    plt.hist(intersection_values, bins=len(intersection_values))
    plt.xlabel('intersections')
    plt.savefig('intersection_histogram.png')
    plt.clf()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='big paper')
    args = parser.parse_args()

    doc = read_csv(args.file)
    graph_edges, edges_weights, intersection_values = edges_calc(doc)
    intersection_values.sort()
    create_intersectionHistogram(intersection_values)
    nodes = nodes_calc(doc)
    create_graph(nodes, graph_edges, edges_weights)

    #print(intersection_values)
    #print(len(intersection_values))

if __name__ == '__main__':
    main()
