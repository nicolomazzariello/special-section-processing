import argparse
import glob, os
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lettura del file csv contenente gli articoli postprocessati e conteggio del numero di articoli
def read_csv(path):

    file_path = str.format(*glob.glob(os.path.join(path, path.split('\\')[-1] + '_postproc.csv')))

    dataframe = pd.read_csv(file_path, delimiter='\t')
    n_row = dataframe.shape[0]

    return path.split('\\')[-1], n_row

# Creazione di un istogramma ordinato in senso decrescente in base al numero di articoli
def create_hist(x, y, file_name):

    ordered_values = np.sort(y)[::-1]
    ordered_labels = [x[i] for i in np.argsort(y)[::-1]]

    plt.figure(figsize=(30, 15))
    plt.bar(ordered_labels, ordered_values, edgecolor='black', width=0.4, color='green')
    plt.xlabel('Special Sections')
    plt.ylabel('Number of papers')
    plt.xticks(rotation='vertical')
    plt.savefig(file_name + '_histogram.png')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('directories', nargs='*', help='elenco di directory')
    args = parser.parse_args()

    spec_sec = []
    papers = []

    for dir in args.directories:
        spec_sec.append(read_csv(dir)[0])
        papers.append(read_csv(dir)[1])

    create_hist(spec_sec, papers, args.directories[0].split('\\')[-2])

if __name__ == '__main__':
    main()