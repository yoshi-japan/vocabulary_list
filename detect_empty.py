import csv


file_name = input('Enter file name; new_svl8_2.csv : ')

with open(file_name, 'r', encoding='utf-8') as detect_file:
    csv_reader = csv.reader(detect_file)
    for row in csv_reader:
        if not row[1]:
            print(row)
