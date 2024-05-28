import argparse
import pandas as pd

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='ETFA.csv')
    args = parser.parse_args()

    #reading the csv file and put it in a dataframe
    df = pd.read_csv(args.file, sep='\t')


    #now I have to drop all rows which contain "no" in the accepted column
    accepted_column = df['accepted']
    indexNames = df[accepted_column == "no"].index
    df.drop(indexNames, inplace=True)

    df.to_csv("onlyAcceptedETFA.csv", sep='\t')
        
if __name__ == '__main__':
    main()