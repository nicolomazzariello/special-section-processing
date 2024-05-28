import csv
import re
import pandas as pd
from pathlib import Path
import argparse

# Divisione degli articoli delle Special Section in base alla Special Section di appartenenza
def titles_partition(spec_sec_file):
    titles = []

    csv_file = pd.read_csv(spec_sec_file, sep='\t')
    grouped_spec_sec = csv_file.groupby('final_track')
    for _, group in grouped_spec_sec:
        titles.append([re.sub('[^a-zA-Z]', '', title.strip().lower()) for title in group['title'].values.tolist()])

    return titles

# Divisione degli articoli preprocessati con slrkit in base alla Special Section di appartenenza
def preproc_partition(titles, preproc_file):
    preproc_titles_partition = []

    for i in titles:
        preproc_titles_partition.append([])

    with open(preproc_file, 'r', encoding='utf-8') as csv_preproc:
        csv_reader = csv.DictReader(csv_preproc, delimiter='\t')

        for item in csv_reader:
            for i in range(0, len(titles)):
                if re.sub('[^a-zA-Z]', '', item['title'].strip().lower()) in titles[i]:
                    preproc_titles_partition[i].append(item)
                    break

    return preproc_titles_partition

# Creazione di sottocartelle per ogni Special Section e divisione degli articoli preprocessati nelle sottocartelle
def create_subdir(preproc_titles):

    keys = preproc_titles[0][0].keys()
    ind = 0

    for item in preproc_titles:

        p_specsec = Path('SpecSec')
        p_specsec_child = Path(f'SpecSec{ind+1}')

        p = Path(p_specsec/p_specsec_child)
        p.mkdir(parents=True)

        with open(p/f'SpecSec{ind+1}_postproc.csv', 'w', newline='', encoding='utf-8') as csv_output:
            dict_writer = csv.DictWriter(csv_output, keys, delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(preproc_titles[ind])

        ind += 1

""" # Creazione di un eseguibile .bat per l'esecuzione del postprocessamento degli abstract e di LDA per ogni Special Section
def create_bat(dim):

   slrkitpath = r'set SLRKITPATH=Inserire il percorso di slr-kit presente sul proprio pc' + '\n\n'
    command = slrkitpath
    postproc = ''
    lda = ''

    for i in range(0, dim):
        postproc += f'python %SLRKITPATH%\postprocess.py SpecSec\SpecSec{i+1}\SpecSec{i+1}_preproc.csv SpecSec-TII_terms.csv SpecSec\SpecSec{i+1} --output SpecSec{i+1}_postproc.csv\n'
        lda += f'python %SLRKITPATH%\lda_ga.py SpecSec\SpecSec{i+1}\SpecSec{i+1}_postproc.csv %SLRKITPATH%\ga_param.toml SpecSec\SpecSec{i+1}\n'

    command += postproc + '\n' + lda

    with open('run_all_process.bat', 'w', encoding='utf-8') as bat_file:
        bat_file.write(command) """

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('spec_sec_csv', type=str, help='file csv contenente articoli e nomi delle Special Section')
#    parser.add_argument('preproc_file', type=str, help='file csv contenente gli articoli preprocessati di tutte le Special Section')
    args = parser.parse_args()

    titles = titles_partition(args.spec_sec_csv)
    preproc_titles_partition = preproc_partition(titles, args.spec_sec_csv)
    create_subdir(preproc_titles_partition)
#    create_bat(len(preproc_titles_partition))

if __name__ == '__main__':
    main()