import csv
def next_batch():
    with open('next_pages.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        
        if rows:  # Check if the file is not empty
            last_row = rows[-1]  # Get the last row
            print(last_row)
        else:
            print("The CSV file is empty.")
    return(last_row)