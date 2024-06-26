import argparse
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import networkx as nx
from cdlib import algorithms, viz
from scipy.stats import norm
import statistics
import numpy as np
import math

def intersections(file):

    df = pd.read_csv(file, sep='\t')
    df.drop(df[df['total'] == 1].index, inplace=True) #removing rows with no connections between tracks

    name_columns = df.columns.tolist()
    name_columns = name_columns[2:len(name_columns)-1] #to get only the tracks
    df = df[name_columns]

    list_columns= []

    for column in name_columns:
        list_columns.append(df[column].tolist())
    
    # dictionary with track as key and a list of numbers (the frequency of words calculated in the previous script) (example {track: [n1, n2, ..., n-n]})
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

    # dictionary with track as key and 0 as value (example {track: 0}). this will be a dictionary with track as key and her number of intersection as value
    h_dict = {a: b for a, b in zip(name_columns, zero_list)}
    
    # dictionary with a tupla of two tracks as key and the number of intersection between this two tracks (example {(track1, track2): number of intersection})
    track_intersection_dict = {a: b for a, b in zip(track_pairs, intersection_without_zero)}

    for key in track_intersection_dict.keys():

        h_dict[key[0]] = h_dict[key[0]] + track_intersection_dict.get(key)
        h_dict[key[1]] = h_dict[key[1]] + track_intersection_dict.get(key)
    
    for key in h_dict.keys():
        
        # average of intersections
        h_dict[key] = round(h_dict.get(key)/len(h_dict))

    return h_dict

def h_index_expert(h_dict):
    
    value_list = list(h_dict.values())

    value_list = np.array(value_list)
    n = value_list.shape[0]
    array = np.arange(1, n+1)
    
    # reverse sorting
    value_list = np.sort(value_list)[::-1]
    
    # intersection of citations and k
    h_idx = np.max(np.minimum(value_list, array))

    return h_idx, array, value_list

def createImage(h_idx, array, value_list):

    plt.hist(array, bins=45, weights=value_list, ec="black", fc="orange")

    plt.plot(array,value_list, color="green", linestyle="solid")

    plt.plot([0, h_idx], [h_idx, h_idx], color='b', linestyle='--')
    plt.plot([h_idx, h_idx], [0, h_idx], color='b', linestyle='--')


    plt.plot(h_idx, h_idx, color="red", marker="o")

    plt.text(h_idx + 0.5, h_idx + 0.5, h_idx)

    plt.xlabel('Number of tracks')
    plt.ylabel('Intersections')
    plt.savefig('h_index.png')
    plt.clf()
    
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='matrix')
    args = parser.parse_args()

    h_dict = intersections(args.file)

    h_idx, array, value_list = h_index_expert(h_dict)

    createImage(h_idx, array, value_list)
    
if __name__ == '__main__':
    main()
