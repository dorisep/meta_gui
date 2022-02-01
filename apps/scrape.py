import requests
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv
from datetime import datetime
import playlist_app
import re

def meta_scrape(week_num):
    week_num = week_num
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
        artist_raw = item.find('div', class_='artist').text.strip().lstrip('by ')
        ar = re.sub(r'[^-A-Za-z0-9!áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ ]+', '', artist_raw)
        artist_clean= re.sub(' +', ' ', ar)
        album_dict['artist']=artist_clean
        
        ###        
        # scrape date
        #sqlite doesn't support datetime objects date column will be string
        #make an objec of date to extract week num and year
        ###
        date_string = (item.find('div', class_='clamp-details').find('span').text)
        date_obj = datetime.strptime(date_string, '%B %d, %Y')
        year, album_week_num, day_of_week = date_obj.isocalendar()
        album_dict['date']=date_string
        album_dict['year'] = year
        album_dict['week_num']=album_week_num
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
            album_dict['user_score']=user_string
        else:
            user_score = int(float(user_string)*10)
            album_dict['user_score']=user_score
        album_dicts.append(album_dict)
    scrape_reviews (album_dicts, week_num)
    return write_csv(album_dicts, week_num)

def scrape_reviews(album_dicts, week_num):
    img = []
    crit_num = []
    user_num = []
    label = []
    genre = []
    count = 0    
    for album_dict in album_dicts:
        print(album_dict['artist'])
        print(album_dict['album'])
        print(f"{album_dict['album']}/{album_dict['artist']}".replace(" ", "-").lower() )
        break
        
        # concat url for review scrape    
        url_beginning ='https://www.metacritic.com/music/'
        review_urls.append(url_beginning + url_end)

def write_csv(album_dicts, week_num):

    # write dictionary to csv
    # csv variables
    output_path = os.path.join('..', 'data', 'meta_scrape.csv')
    # create header
    fields = ['artist', 'album', 'date', 'week_num', 'year', 'meta_score', 'user_score'] 
    # create variable for data to be written
    keys = album_dicts[0].keys()
    # output to csv
    with open(output_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader()
        writer.writerows(album_dicts)
    # call create playlist script
     
    return playlist_app.create_playlist(week_num)
