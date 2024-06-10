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

    # dictionary with track as key and her relative abstract as value (example {track: "text"})
    track_dictionary = {a: b for a, b in zip(track, text)}

    # after the loop the dictionary will be with track as key and a list of words as value (example {track: [word1, word2, ..., word-n]})
    for key in track_dictionary.keys():

        words = []

        words = track_dictionary.get(key).split(" ")

        track_dictionary[key] = words
 
    cnt_list = [] # will be a list of counter

    for key in track_dictionary.keys():

        cnt = Counter()
    
        for word in track_dictionary.get(key):
            cnt[word] += 1

        cnt_list.append(cnt)

    # dictionary with track as key and her relative counter as value (example {track: counter})
    track_counter_dictionary = {a: b for a, b in zip(track, cnt_list)}

    # will be an hash dictionary with number as key and word as value (example {1: word1})
    hash_big_cnt = {}
    c = 0

    # big_cnt is a dictionary with every word of every paper as key and her frequency as value (example {word: frequency})
    for key in big_cnt.keys():
        hash_big_cnt[c] = key
        c+=1

    for key in track_counter_dictionary.keys():

        counter_dict = {}
        counter_dict = track_counter_dictionary.get(key) #to get the counter of a track (a counter is a dictionary)

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
