import sys
import glob, os
import csv
import itertools
import argparse
import re

# Lettura del file csv contenente gli articoli postprocessati
def read_csv(file):

    papers = []

    with open(file, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        for item in reader:
            papers.append(item)

    return papers

# Creazione dei file csv di output
def create_csv(file_name, th, *args):

    keys = ['id', 'papers']

    for i in range(0, th):
        keys.append(f'coherence_th{i+1}')

    if args:
        keys.append(args[0])

    with open(file_name, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys, delimiter='\t')
        writer.writeheader()

# Scrittura dei file csv di output
def write_csv(file_name, id, coherence, n_papers, *args):
    with open(file_name, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t')
        csv_row = [id, n_papers]

        for item in coherence:
            csv_row.append(round(item, 3))

        if args:
            csv_row.append(round(args[0], 3))

        csv_writer.writerow(csv_row)

# Calcolo del numero di lati del grafo una Special Section o Special Section fake in base alla soglia
def edges_calc(doc, th):
    n_edges = 0

    for paper1, paper2 in itertools.combinations(doc, 2):
        if len(set(paper1['abstract_filtered'].lower().split()).intersection(set(paper2['abstract_filtered'].lower().split()))) >= th:
            n_edges += 1

    return n_edges

# Calcolo della coerenza tra gli articoli di una stessa Special Section o Special Section fake
def metric_calc(path, th):
    coherence = []

    with open(str.format(*glob.glob(os.path.join(path, path.split('/')[-1] + '_postproc.csv'))), 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter='\t')

        doc = []

        for item in csv_reader:
            doc.append(item)

    max_edges = (len(doc)*(len(doc)-1)/2)

    for i in range(0, th):
        try:
            coherence.append(edges_calc(doc, i+1) / max_edges)
        except:
            coherence.append(0)

    return coherence, len(doc)

# Calcolo del valore sparsity per gli articoli di una Special Section fake
def sparsity_calc(papers_real, fake_spec_sec):

    num_spec_sec = []

    papers_fake = read_csv(os.path.join(fake_spec_sec, fake_spec_sec.split('/')[-1] + '_postproc.csv'))

    for item in papers_fake:
        for i in range(0, len(papers_real)):
            if re.sub('[^a-zA-Z]', '', item['title'].strip().lower()) in papers_real[i]:
                num_spec_sec.append(i)
                break

    try:
        sparsity = len(set(num_spec_sec))/len(papers_fake)
    except:
        sparsity = 'null'

    return sparsity

# Estrazione del titolo degli articoli delle Special Section
def extract_titles(spec_sec):
    titles = []

    for i in spec_sec:
        temp_titles = []
        for j in i:
            temp_titles.append(re.sub('[^a-zA-Z]', '', j['title'].strip().lower()))
        titles.append(temp_titles)

    return titles

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-th', type=int, help='threshold (soglia: numero intero)')
    parser.add_argument('--spec_sec', nargs='*', help='elenco di directory delle Special Section')
    parser.add_argument('--spec_sec_fake', nargs='*', help='elenco di directory delle Special Section Fake')
    args = parser.parse_args()

    if args.th is None:
        args.th = 10

    create_csv('Spec_Sec_metrics.csv', args.th)

    real_spec_sec = []

    for dir in args.spec_sec:
        real_spec_sec.append(read_csv(os.path.join(dir, dir.split('/')[-1] + '_postproc.csv')))
        coherence, n_papers = metric_calc(dir, args.th)
        write_csv('Spec_Sec_metrics.csv', dir.split('/')[-1], coherence, n_papers)

    real_papers_titles = extract_titles(real_spec_sec)

    create_csv('Spec_Sec_fake_metrics.csv', args.th, 'sparsity')

    for dir in args.spec_sec_fake:
        coherence, n_papers = metric_calc(dir, args.th)
        consistency = sparsity_calc(real_papers_titles, dir)
        write_csv('Spec_Sec_fake_metrics.csv', dir.split('/')[-1], coherence, n_papers, consistency)

if __name__ == '__main__':
    main()