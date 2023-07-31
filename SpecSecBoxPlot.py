import sys
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import csv

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

# Creazione di un box plot
def create_boxplot(values, file_name):

    plt.figure(figsize=(30, 15))
    plt.boxplot(values)

    plt.xlabel('Threshold', fontsize=20)
    plt.ylabel('Values', fontsize=20)

    path = 'SpecSec'

    if 'fake' in file_name:
        path += 'Fake_BoxPlot.png'
    else:
        path += '_BoxPlot.png'

    plt.savefig(path)
    plt.clf()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('spec_sec_metrics', type=str, help='file con le metriche delle Special Section')
    parser.add_argument('spec_sec_fake_metrics', type=str, help='file con le metriche delle Special Section')
    args = parser.parse_args()

    for item in sys.argv[1:]:
        values = read_csv(item)
        create_boxplot(values, item)

if __name__ == '__main__':
    main()