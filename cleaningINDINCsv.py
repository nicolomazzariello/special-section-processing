import argparse
import pandas as pd

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='ETFA.csv')
    args = parser.parse_args()

    #reading the csv file and put it in a dataframe
    df = pd.read_csv(args.file, sep=';')

    #now I have to drop all rows which not contain "final_submitted" in the status column
    status_column = df['status']
    indexNames = df[status_column != "final_submitted"].index
    df.drop(indexNames, inplace=True)

    df.to_csv("cleanedINDIN.csv", sep='\t')
        
if __name__ == '__main__':
    main()