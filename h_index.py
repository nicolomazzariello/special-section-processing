import argparse
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import networkx as nx
from cdlib import algorithms, viz
from scipy.stats import norm
import statistics

def intersections(file):

    df = pd.read_csv(file, sep='\t')
    df.drop(df[df['total'] == 1].index, inplace=True) #removing rows with no connections between tracks

    name_columns = df.columns.tolist()
    name_columns = name_columns[2:len(name_columns)-1] #to get only the tracks
    df = df[name_columns]

    list_columns= []

    for column in name_columns:
        list_columns.append(df[column].tolist())
    
    dictionary_columns = {a: b for a, b in zip(name_columns, list_columns)}

    track_pairs = []
    intersection_without_zero = []
    intersection_values = []

    for track1, track2 in itertools.combinations(dictionary_columns.keys(), 2):
        
        intersection = 0

        for i, j in zip(dictionary_columns.get(track1), dictionary_columns.get(track2)):
            if i >= 2 and j >= 2:
                intersection+=1

        intersection_values.append(intersection)

        if intersection > 0:
            track_pairs.append((track1, track2))
            intersection_without_zero.append(intersection)

    zero_list = []

    for i in range(len(name_columns)):
        zero_list.append(0)

    h_dict = {a: b for a, b in zip(name_columns, zero_list)}
    
    track_intersection_dict = {a: b for a, b in zip(track_pairs, intersection_without_zero)}

    for key in track_intersection_dict.keys():

        h_dict[key[0]] = h_dict[key[0]] + track_intersection_dict.get(key)
        h_dict[key[1]] = h_dict[key[1]] + track_intersection_dict.get(key)

    return h_dict

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='matrix')
    args = parser.parse_args()

    h_dict = intersections(args.file)
    
if __name__ == '__main__':
    main()
