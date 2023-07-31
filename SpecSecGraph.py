import csv
import argparse
import os, glob
import itertools
import matplotlib.pyplot as plt
import networkx as nx

# Lettura del file csv con gli articoli postprocessati
def read_csv(path):

    with open(str.format(*glob.glob(os.path.join(path, path.split('\\')[-1] + '_postproc.csv'))), 'r', encoding='utf-8') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter='\t')

        doc = []

        for item in csv_reader:
            doc.append(item)

    return doc

# Calcolo dei lati e del loro peso (numero di parole in comune tra gli abstract_filtered di due articoli)
def edges_calc(doc):
    graph_edges = []
    edges_weights = []

    for paper1, paper2 in itertools.combinations(doc, 2):
        intersection = len(set(paper1['abstract_filtered'].lower().split()).intersection(set(paper2['abstract_filtered'].lower().split())))
        if intersection > 0:
            graph_edges.append((paper1['id'], paper2['id']))
            edges_weights.append(intersection)

    return graph_edges, edges_weights

# Inserimento dei nodi all'interno del grafo
def nodes_calc(doc):
    nodes = []

    for d in doc:
        nodes.append(d['id'])

    return nodes

# Creazione del grafo
def create_graph(nodes, edges, weights, path):
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    pos = nx.circular_layout(g)
    nx.draw(g, pos, with_labels=True, node_color='orange', node_size=900, edge_color=['red' if weight > 6 else 'blue' for weight in weights])
    a_dict = {a: b for a, b in zip(edges, weights)}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=a_dict)
    plt.savefig(os.path.join(path, path.split('\\')[-1]+'_graph.png'))
    plt.clf()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('directories', nargs='*', help='elenco di directories con gli articoli postprocessati')
    args = parser.parse_args()

    for path in args.directories:
        doc = read_csv(path)
        graph_edges, edges_weights = edges_calc(doc)
        nodes = nodes_calc(doc)
        create_graph(nodes, graph_edges, edges_weights, path)

if __name__ == '__main__':
    main()