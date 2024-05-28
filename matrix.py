import argparse
import csv
import pandas as pd
from collections import Counter

def count_total_words(file):

    df = pd.read_csv(file, sep='\t')

    list = df['abstract_filtered'].values.tolist()
    words = []

    for i in list:
        words += i.split(" ")
    
    cnt = Counter()
    
    for word in words:
        cnt[word] += 1

    return cnt

def add_every_words(cnt):

    df = pd.read_csv('matrix.csv', sep='\t')

    df['unique_words'] = [key for key in cnt.keys()]

    df['total'] = [cnt.get(key) for key in cnt.keys()]

    return df

def create_csv(file):

    df = pd.read_csv(file, sep='\t')

    list = df['id'].values.tolist()

    keys = ['unique_words'] + [item for item in list] + ['total']

    with open('matrix.csv', 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys, delimiter='\t')
        writer.writeheader()

def count_words_per_track(file, big_cnt, dataFrame):

    df = pd.read_csv(file, sep='\t')

    track = df['id'].values.tolist()
    text = df['abstract_filtered'].values.tolist()

    track_dictionary = {a: b for a, b in zip(track, text)}

    for key in track_dictionary.keys():

        words = []

        words = track_dictionary.get(key).split(" ")

        track_dictionary[key] = words
 
    cnt_list = []

    for key in track_dictionary.keys():

        cnt = Counter()
    
        for word in track_dictionary.get(key):
            cnt[word] += 1

        cnt_list.append(cnt)

    track_counter_dictionary = {a: b for a, b in zip(track, cnt_list)}

    hash_big_cnt = {}
    c = 0

    for key in big_cnt.keys():
        hash_big_cnt[c] = key
        c+=1

    for key in track_counter_dictionary.keys():

        counter_dict = {}
        counter_dict = track_counter_dictionary.get(key)

        for i in hash_big_cnt.keys():

            if hash_big_cnt.get(i) not in counter_dict.keys():
                dataFrame.at[i, key] = 0

            else:
                dataFrame.at[i, key] = counter_dict.get(hash_big_cnt.get(i))
    dataFrame.to_csv('matrix.csv', sep='\t')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='big paper')
    args = parser.parse_args()

    create_csv(args.file)
    cnt = count_total_words(args.file)
    df = add_every_words(cnt)
    count_words_per_track(args.file, cnt, df)

if __name__ == '__main__':
    main()
