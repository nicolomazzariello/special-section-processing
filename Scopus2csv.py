import csv
import argparse

# Lettura del csv scaricato da Scopus e conversione nel csv compatibile con slr-kit
def scopus2csv(input_file):
        with open(input_file, 'r', encoding='utf-8') as bibliography_file:
            csv_reader = csv.DictReader(bibliography_file, delimiter=',')
            id = 0
            conv_list = []
            for item in csv_reader:
                conv_list.append({'id':id, 'title':item['Title'], 'abstract':item['Abstract'], 'year':item['Year'], 'journal':item['Source title'], 'citations':item['Cited by']})
                id += 1

            keys = conv_list[0].keys()

            with open('slr-kit_abstracts.csv', 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, keys, delimiter='\t')
                dict_writer.writeheader()
                dict_writer.writerows(conv_list)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', type=str, help='file csv scaricato da Scopus')
    args = parser.parse_args()

    scopus2csv(args.input_file)

if __name__ == '__main__':
    main()