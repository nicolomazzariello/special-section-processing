import argparse
import pandas as pd

def checkMismatch(checked_file, file_to_check):

    df_checked_file = pd.read_csv(checked_file, sep='\t')
    df_file_to_check = pd.read_csv(file_to_check, sep='\t')

    df_file_to_check['Profs_classification'] = None

    dict_checked_file = {a: b for a, b in zip(df_checked_file['term'],df_checked_file['label'])}
    dict_file_to_check = {a: b for a, b in zip(df_file_to_check['term'],df_file_to_check['label'])}

    i = 0

    for key in dict_file_to_check.keys():

        if key in dict_checked_file.keys():
            df_file_to_check.at[i, 'Profs_classification'] = dict_checked_file.get(key)

        i+=1

    df_file_to_check.to_csv('file_to_check.csv', sep='\t')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('checked_file', type=str, help='file with the classification checked by the expert')
    parser.add_argument('file_to_check', type=str, help='file to check with the file with a good classification')
    args = parser.parse_args()

    checkMismatch(args.checked_file, args.file_to_check)
    
if __name__ == '__main__':
    main()
