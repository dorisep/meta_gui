import wikipedia
import csv
import os


csv_path = '..\\data\\meta_scrape.csv'
search = []
artist_search_results_dict = {}
with open(csv_path, newline='', encoding = "ISO-8859-1") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row)
#         filter for artists and albums from current week
        if int(row['week_num']) == 1:
            # print(row['artist'])
            ###
            # create a set for determining how artist is entered into wikkipedia
            # ampersand 
            ###
            wikki_band_variations = {row['artist'], f"{row['artist']} (band)", f"{row['artist']}pr (group)"}
            print(wikki_band_variations)
            search_results = wikipedia.search(row['artist'])  
            print(search_results)
            print(wikki_band_variations.intersection(search_results))
            # ç.sort()
            # search_artist_album=wikipedia.search(f"{row['artist']} + ' ' + {row['album']}").sort()
            # search_artist_dicography=wikipedia.search(f"{row['artist']} + discography").sort())
            ###
            #determining the type returned from wikki search
            # print(type(search))
            ###
            ###
            #checking for differences in the return using sort() and ==
            # if (search_artist==search_artist_album):
            #     print(f"{row['artist']} + search returns the same results")
            # else: print(f"{row['artist']} + search returns different results")
            ###
            ###
            # identifying differences in values returned using set()
            ###
            # search_artist=wikipedia.search(f"{row['artist']}")
            # search_artist_dicography=wikipedia.search(f"{row['artist']} + discography")
            # diff_in_search = set(search_artist)-set(search_artist_dicography)
            # print(diff_in_search not in search_artist)
            
            
            # print(search_artists_discography)



        

            #     print(f'{row["artist"]} has discography')
# for a in disc_dict.values():
#     print(a)