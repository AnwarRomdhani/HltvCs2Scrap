import csv



def initialize():
    data = []
    with open('links_matches.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data