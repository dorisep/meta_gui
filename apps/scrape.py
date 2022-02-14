from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import os 
import csv
from datetime import datetime as dt
import playlist_app
import re
import time
from base64 import b64encode
from pickle import load, dump

def meta_scrape(week_num, year):
    
    url_for_scrape = 'https://www.metacritic.com/browse/albums/release-date/new-releases/date'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    # send response
    response_score = requests.get(url_for_scrape, headers = user_agent)
    # scrape website into variable to parse
    soup_score = BeautifulSoup(response_score.text, 'html.parser')
    # create list for dictionarys 
    album_dicts = []
    # create soup 
    for item in soup_score.find_all('td', class_='clamp-summary-wrap'):
        album_dict = {}
        ###        
        # scrape date
        #sqlite doesn't support datetime objects date column will be string
        #make an objec of date to extract week num and year
        ###
        date_string = (item.find('div', class_='clamp-details').find('span').text)
        date_obj = dt.strptime(date_string, '%B %d, %Y')
        album_year, album_week_num, day_of_week = date_obj.isocalendar()
        ###
        # limit scrape to previous three weeks of albums and current 
        # year of release date
        ###
        if album_week_num < (week_num - 5) or album_year < year:
            break   
        else:
            album_dict['date']=date_string
            album_dict['year'] = year
            album_dict['week_num']=album_week_num
            ###
            # scrape album name
            # regular expressions to prepare album and artist names for 
            # search in spotify DB
            ####
            album_raw = item.find('a', class_= 'title').text
            al = re.sub(r'[^-A-Za-z0-9!áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ ]+', '', album_raw)
            album_clean = re.sub(' +', ' ', al)
            album_dict['album']= album_clean
            ###
            # scrape artist name and strip white space and extra characters
            ###
            # artist_raw = item.find('div', class_='artist').text.strip().lstrip('by ')
            print(artist_raw:= item.find('div', class_='artist').text.strip()[3:])

            ar = re.sub(r'[^-A-Za-z0-9!áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ ]+', '', artist_raw)
            artist_clean= re.sub(' +', ' ', ar)
            album_dict['artist']=artist_clean
           
            ###
            # Handle for varaitions in classes for critic name by pattern matching with regular expression.
            # then scrape critic and user scores
            ###
            meta_critic_pattern = re.compile('^metascore_w large')
            meta_user_pattern = re.compile('^metascore_w user')
            album_dict['meta_score']=int(item.find('div', class_= meta_critic_pattern).text)
            user_string = (item.find('div', class_= meta_user_pattern).text)
            ###
            # Handle for variations in classes for user by filtering out strings from scores to and casting to ints
            ###
            if user_string == 'tbd':
                album_dict['user_score'] = 0
            else:
                user_score = int(float(user_string)*10)
                album_dict['user_score']=user_score
            album_dicts.append(album_dict)
    scrape_reviews(album_dicts, week_num, user_agent, al, ar)

    

def scrape_reviews(album_dicts, week_num, user_agent, al, ar):
    url_beginning ='https://www.metacritic.com/music/'
    for album_dict in album_dicts:
        # only check for the last 4 weeks of albums
        if album_dict['week_num'] < (week_num - 5):
            break
        else:
            
            url_end = f"{album_dict['album']}/{album_dict['artist']}".replace(" ", "-").lower() 
            url = url_beginning + url_end
            ###
            # creating pickles to prevent disconnect from too many pings
            # check if a pickle file exists for the current day 
            # if not run scrape for url
            ###
            picklefile = os.path.join('..', 'data', 'pickles',str(b64encode(url.encode('utf-8')),'utf-8'))
            print(picklefile)
            if os.path.exists(picklefile) and dt.fromtimestamp(os.path.getctime(picklefile)).day==dt.now().day().day:
                with open(picklefile,'rb') as pickleload:
                    print('loading a pickle')
                    content = load(pickleload)
            else:
                content = requests.get(url, headers = user_agent)
                with open(picklefile,'wb') as picklesave:
                    print('creating a pickle')
                    dump(content, picklesave)
                # scrape website into variable to parse
            soup_reviews = BeautifulSoup(content.text, 'html.parser')
            print('parsing a review')
            # scrape num of critical reviews
            try:
                num_rev=(soup_reviews.find('span', itemprop="reviewCount"))
                album_dict['crit_num'] = num_rev.text.strip()
            except:
                album_dict['crit_num'] = None
            # scrape num of user reviews
            if album_dict['user_score'] == 0:
                album_dict['user_num'] = 0
            else:
                try:
                    album_dict['user_num'] = int(soup_reviews.find_all("a", href=f"/music/{url_end}/user-reviews")[2].text.split()[0])
                except:
                    album_dict['user_num'] = 0
            # scrape record labels
            try:
                label_class = soup_reviews.find_all("span", itemprop="name")
                album_dict['label'] = label_class[2].text.strip()
            except:
                album_dict['label'] = None
            # scrape genre
            try:
                album_dict['genre'] = []
                genre_elements = soup_reviews.find_all("span", itemprop="genre")
                for genre in genre_elements:
                    album_dict['genre'].append(genre.text)
            except:
                album_dict['genre'] = 'unknown'
            time.sleep(3)
    write_csv(album_dicts, week_num)
        
def write_csv(album_dicts, week_num):

    # write dictionary to csv
    # csv variables
    output_path = os.path.join('..', 'data', 'meta_scrape.csv')
    # create header
    fields = ['artist', 'album', 'date', 'week_num', 'year', 'meta_score', 'user_score', ] 
    # create variable for data to be written
    keys = album_dicts[0].keys()
    # output to csv
    print('writing')
    with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader()
        writer.writerows(album_dicts)
    # call create playlist script
     
    return playlist_app.create_playlist(week_num)
