import csv

def next(index):
    data = []
    remaining_rows = []  # Initialize remaining_rows to an empty list
    with open('links_matches.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        target_element = index
        for i, row in enumerate(rows):
            if target_element in row:
                remaining_rows = rows[i+1:]  # Capture all rows after the target
                break  # Exit the loop once the target element is found
        # Ensure remaining_rows has content, otherwise the loop will not execute
        for r in remaining_rows:
            data.append(r)
    return data
