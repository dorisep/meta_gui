import os
import re
import csv
import time 
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from base64 import b64encode
from pickle import load, dump
from playlist_app import create_playlist

def metaScrape(page_num, year):

    # request variables
    url_for_scrape = f'https://www.metacritic.com/browse/albums/score/metascore/year/filtered?year_selected={year}&distribution=&sort=desc&view=detailed&page={page_num}'
    # bs4 variables
    print(url_for_scrape)

    user_agent = {'User-agent': 'Mozilla/5.0'}
    # send response
    response_score = requests.get(url_for_scrape, headers = user_agent)
    # scrape website into variable to parse
    soup_score = BeautifulSoup(response_score.text, 'html.parser')
    print(soup_score)
    #     create list for dictionarys 
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

        album_dict['date']=date_string
        album_dict['year'] = album_year
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
        artist_raw = item.find('div', class_='artist').text.strip().lstrip('by ')
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
    write_csv(album_dicts, page_num, year)

def write_csv(album_dicts, page_num, year):
    # write dictionary to csv
    # csv variables
    print(len(album_dicts))
    output_path = os.path.join('..', 'data', 'hist_scrape', f'albums_{year}.csv')
    # create variable for data to be written
    keys = album_dicts[0].keys()
    # output to csv
    print(f'writing: {year}, {page_num}')
#   create output file for first page and append data from following pages
    if page_num == 0:
        with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, keys)
            writer.writeheader()
            writer.writerows(album_dicts)
    else:
        with open(output_path, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, keys)
            writer.writeheader()
            writer.writerows(album_dicts)
    time.sleep(10)

def metaScorePages():
    # find number of pages for albums 2020
    url_pages = 'https://www.metacritic.com/browse/albums/score/metascore/year/filtered?year_selected=2020&distribution=&sort=desc&view=detailed&page=0'
    # set user agent for header
    user_agent = {'User-agent': 'Mozilla/5.0'}
    # send response
    response_pages = requests.get(url_pages, headers = user_agent)
    # scrape website into variable to parse
    soup_pages = BeautifulSoup(response_pages.text, 'html.parser')
    # print(soup_pages)
    # create temporary lists for user scores

    pages = int(soup_pages.find("li", class_="page last_page").next_element.text)
    for year in range(2000, 2021):
        for page in range(pages):
            metaScrape(page, year)
        break

metaScorePages()