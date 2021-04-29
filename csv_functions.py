import csv
def insert_row_csv(csv_file, row):
    with open(csv_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(someiterable)