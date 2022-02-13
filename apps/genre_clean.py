import csv

with open('..//data//meta_scrape.csv') as file:
    reader = csv.reader(file)
    header = next(reader)
    
    genre_lst = []
    for row in reader:
        print(row)
#         if len(row) > 0:
#             print(row[10])
#             # for genres in row[10]:
#             #     if genres not in genre_lst:
#             #         genre_lst.append(genres)
# print(genre_lst)