import csv

with open('..//data//meta_scrape.csv') as file:
    reader = csv.reader(file)
    header = next(reader)
    
    genre_lst = []
    for row in reader:
        print(row)
# clear