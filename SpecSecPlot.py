import argparse
import statistics
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

# Lettura del file csv con i valori di coerenza
def read_csv(file):

    values_by_row = []
    prefix = 'coherence_th'

    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        headers = next(reader)

        col_ind = [i for i, col in enumerate(headers) if col.startswith(prefix)]

        for row in reader:
            columns = [float(row[i]) for i in col_ind]
            values_by_row.append(columns)

        return list(zip(*values_by_row))

# Calcolo del valore medio di coerenza di una Special Section o Special Section fake
def mean_calc(values):

    mean = []

    for value in values:
        mean.append(statistics.mean(value))

    return mean

# Creazione del grafico
def create_plot(x, y):

    graph_name = ['Special Section', 'Special Section Fake']

    colors = ['red', 'blue']
    plt.figure(figsize=(30, 15))

    for i,item in enumerate(y):

        x_plot = np.linspace(min(x), max(x), 100)
        y_plot = np.interp(x_plot, x, item)

        plt.plot(x, item, 'o', color='black')
        plt.plot(x_plot, y_plot, label=graph_name[i], color=colors[i])

    plt.xlabel('Threshold', fontsize=20)
    plt.ylabel('Mean', fontsize=20)
    plt.legend(fontsize=20)


    plt.savefig('Plot.png')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('spec_sec_metrics', type=str, help='file con le metriche delle Special Section')
    parser.add_argument('spec_sec_fake_metrics', type=str, help='file con le metriche delle Special Section')
    args = parser.parse_args()

    mean = []

    for item in sys.argv[1:]:
        values = read_csv(item)
        mean.append(mean_calc(values))

    create_plot(list(range(1, len(mean[0]) + 1, 1)), mean)

if __name__ == '__main__':
    main()