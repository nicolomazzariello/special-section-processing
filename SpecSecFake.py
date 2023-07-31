import argparse
import csv
import pandas as pd
import re
import random
import os
from pathlib import Path

# Lettura del csv contenente gli articoli postprocessati di tutte le Special Section
def read_csv(file):

    papers = []

    with open(file, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        for item in reader:
            papers.append(item)

    return papers

# Creazione csv Special Section fake
def csv_specsec_fake(papers, ind):

        keys = papers[0].keys()

        Path(f'SpecSecFake\SpecSecFake{ind}').mkdir(parents=True)

        with open(f'SpecSecFake/SpecSecFake{ind}/SpecSecFake{ind}_postproc.csv', 'w', newline='', encoding='utf-8') as csv_output:
            dict_writer = csv.DictWriter(csv_output, keys, delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(papers)

# Creazione Special Section fake con articoli postprocessati presi in maniera casuale dalle Special Section
def create_fake(postproc_file, ind):

    random_papers = []

    random_num = random.sample(list(range(0, len(postproc_file))), random.randint(9, 12))

    for i in random_num:
        random_papers.append(postproc_file[i])

    csv_specsec_fake(random_papers, ind)

# Creazione di Special Section fake con articoli postprocessati tutti provenienti da Special Section diverse
def create_all_different_fake(dir, ind):

    random_papers = []
    fake_specsec = []

    random_specsec = random.sample(list(range(0, len(dir))), random.randint(9, 12))

    for i in random_specsec:
        random_papers.append(random.randint(0, len(dir[i])-1))

    for specsec, paper in zip(random_specsec, random_papers):
        fake_specsec.append(dir[specsec][paper])

    csv_specsec_fake(fake_specsec, ind)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directories_special_section', nargs='*', help='directories contenenti tutti i papers divisi per Special Section')
    parser.add_argument('postprocess_file', type=str, help='file postprocessato')
    parser.add_argument('-fake', type=int, help='numero di Special Section fake che si vogliono creare')
    args = parser.parse_args()

    postproc_by_specsec = []
    ind_specsec = 1

    if args.fake is None:
        args.fake = 200

    postproc_file = read_csv(args.postprocess_file)

    for i in range(0, int(args.fake/2)):
        create_fake(postproc_file, ind_specsec)
        ind_specsec += 1

    for item in args.directories_special_section:
        postproc_by_specsec.append(read_csv(os.path.join(item, item.split('\\')[-1] + '_postproc.csv')))

    for i in range(0, args.fake - ind_specsec + 1):
        create_all_different_fake(postproc_by_specsec, ind_specsec)
        ind_specsec += 1

if __name__ == '__main__':
    main()