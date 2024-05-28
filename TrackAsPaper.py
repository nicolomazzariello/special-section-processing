import argparse
import pandas as pd
from pathlib import Path
import os
import csv


# Tutti gli articoli presenti in una track vengono fusi in un solo "big paper"
def track_as_paper(file):

    df = pd.read_csv(file, sep='\t')
    df = df[['final_track', 'abstract_filtered']]

    concateneted_filtered_abstract = ''

    track = df.iloc[0, 0]

    for abstract in df['abstract_filtered']:
        concateneted_filtered_abstract = concateneted_filtered_abstract + abstract + ' '

    #removing the last space
    concateneted_filtered_abstract = concateneted_filtered_abstract[:-1]

    trackPaper = [track, concateneted_filtered_abstract]
    write_biggestPaper(trackPaper)

""" 
    bigPaper = pd.DataFrame({'id': [track], 'abstract_filtered':[concateneted_filtered_abstract]})
    write_csv(bigPaper, track)

# Un file csv contenente il "big paper" per ogni track
def write_csv(bigPaper, track):

    bigPaper.to_csv('Tracks/' + track + '.csv', sep='\t')
 """

def write_biggestPaper(trackPaper):

    with open('Biggest_Paper.csv', 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t')
        csv_writer.writerow(trackPaper)

def create_csv():

    keys = ['id', 'abstract_filtered']

    with open('Biggest_Paper.csv', 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys, delimiter='\t')
        writer.writeheader()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('directories_special_section', nargs='*', help='elenco di directory delle Special Section')
    args = parser.parse_args()

    create_csv()

    #Path('Tracks').mkdir(parents=True)

    for dir in args.directories_special_section:
        track_as_paper(os.path.join(dir, dir.split('/')[-1] + '_postproc.csv'))
        
if __name__ == '__main__':
    main()