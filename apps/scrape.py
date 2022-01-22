import requests
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime
import playlist_app
import re

def meta_scrape(week_num):
    print(f'meta_scrap called, week num =  {week_num}')
    week_num = week_num
    url_for_scrape = 'https://www.metacritic.com/browse/albums/release-date/new-releases/date'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    # send response
    response_score = requests.get(url_for_scrape, headers = user_agent)
    # scrape website into variable to parse
    soup_score = BeautifulSoup(response_score.text, 'html.parser')
    # create/initialize dictionary 
    albums_dict = {'artist':[], 'album':[], 'date':[], 'week_num':[], 'meta_score': [], 'user_score':[]}
    # create soup 
    for _ in soup_score.find_all('td', class_='clamp-summary-wrap'):
        # scrape album name
        albums_dict['album'].append(_.find('a', class_= 'title').text)
        # scrape artist name and strip white space and extra characters
        albums_dict['artist'].append(_.find('div', class_='artist').text.strip().lstrip('by '))
        # scrape date
        ###
        #sqlite doesn't support datetime objects date column will be string
        #make an objec of date to extract week num
        ###
        date_string = (_.find('div', class_='clamp-details').find('span').text)
        date_obj = datetime.strptime(date_string, '%B %d, %Y')
        albums_dict['date'].append(date_string)
        albums_dict['week_num'].append(int(date_obj.isocalendar()[1]))
        # Handle for varaitions in classes for critic name by pattern matching with regular expression.
        # then scrape critic and user scores
        meta_critic_pattern = re.compile('^metascore_w large')
        meta_user_pattern = re.compile('^metascore_w user')
        albums_dict['meta_score'].append(int(_.find('div', class_= meta_critic_pattern).text))
        user_string = (_.find('div', class_= meta_user_pattern).text)
        # Handle for variations in classes for user by filtering out scores from strings to ints
        if user_string == 'tbd':
            albums_dict['user_score'].append(user_string)
        else:
            user_score = int(float(user_string)*10)
            albums_dict['user_score'].append(user_score)

    # create fields for csv
    fields = ['artist', 'album', 'date', 'week_num', 'meta_score', 'user_score'] 
    # create variable for data to be written
    data = zip(albums_dict['artist'], albums_dict['album'], albums_dict['date'], albums_dict['week_num'], albums_dict['meta_score'], albums_dict['user_score'])
    print('meta_scrape complete')
    return write_csv(albums_dict, week_num)

def scrape_reviews(albums_dict, week_num):
    print('scrape_reviews called')
    artists = albums_dict['artist']
    for artist in artists:
        url_for_reviews = f'https://www.metacritic.com/music/the-myth-of-the-happily-ever-after/{artist}'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        # send response
        response_reviews = requests.get(url_for_reviews, headers = user_agent)
        # scrape website into variable to parse
        soup_reviews = BeautifulSoup(response_reviews.text, 'html.parser')
        # print(soup_reviews)
    playlist_app.create_playlist(week_num)
    return albums_dict


def write_csv(albums_dict, week_num):
    print('write_csv called')
    # write dictionary to csv
    # csv variables
    output_path = os.path.join('..', 'data', 'meta_scrape.csv')
    # create header
    fields = ['artist', 'album', 'date', 'week_num', 'meta_score', 'user_score'] 
    # create variable for data to be written
    data = zip(
            albums_dict['artist'], 
            albums_dict['album'], 
            albums_dict['date'], 
            albums_dict['week_num'], 
            albums_dict['meta_score'], 
            albums_dict['user_score']
            )
    # output to csv
    with open(output_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for d in data:
            writer.writerow(d)
    # call create playlist script      
    return playlist_app.create_playlist(week_num)
