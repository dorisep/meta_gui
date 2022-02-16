import os 
from tkinter import *
import csv
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from scrape import meta_scrape
from playlist_app import get_date_info
from credentials.config import scrape_path, clean_path
from dedup_csv import dedup_meta_scrape


#set instance of tk
window = tk.Tk()
#set title
window.title('Create Playlist from meta_scrape')
#set window size
window.geometry('1000x1000')
# window.state('zoomed')
# set week_num variable to current week
date_info = get_date_info()
week_num = IntVar(window, value = date_info[1])
# import scrape module and set to week_num variable to value in week field
def scrape():
    week_num = int(week_field.get())
    meta_scrape(week_num, year=date_info[0])
# dedup csv file for db
def dedup():
    dedup_meta_scrape(scrape_path, clean_path)
# set plotting function


# import meta_scrape data for plot
def scraped_data():
    week_num = int(week_field.get())
    print(week_num)
    scrape_dict = {
        'scores': [],
        'albumlst': [],
        'artistlst': [],
        'num_review_lst': []
    }
    
    file_path = os.path.join('..', 'data', 'meta_scrape.csv')
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if int(row['week_num']) == week_num:
                scrape_dict['scores_lst'].append(row['meta_score'])
                scrape_dict['album_lst'].append(row['album'])
                scrape_dict['artist_lst'].append(row['artist'])
                scrape_dict['num_review_lst'].append(row['crit_num'])

    return scrape_dict

def scrape_bar_scores(scrape_dict):
    scores = [float(x) for x in scrape_dict['scores']]

    albums = scrape_dict['albumlst']

    fig = plt.figure(figsize = (5, 2.5))
    plt.xticks(rotation = 90)
    plt.bar(albums, scores, color='cornflowerblue')

    plt.xlabel('album names')
    plt.ylabel('metascores')
    plt.title('Current Week Scores')
    plt.show()

def scrape_scatter(scrape_dict):
    pass

def plot():
    scrape_bar_scores(scraped_data())


# create button for scrape
scraper = tk.Button(window,text='Run Scrape for week number:',command=scrape, height=1,width=25,state='normal')
scraper.place(x=12, y=20)
# create field for week num variable
week_field = Entry(window, textvariable=week_num, width=2)
week_field.place(x=270, y=22)
# create_depuped_csv
cleaner = tk.Button(window,text='create deduped csv',command=dedup, height=1,width=25,state='normal')
cleaner.place(x=12, y=45)
# create button for plot
plotter = tk.Button(window,text='plot',command=plot, height=1,width=25,state='normal')
plotter.place(x=12, y=70)
# button to disply scrape results for QA
plotter = tk.Button(window,text='scrape results',command=plot, height=1,width=25,state='normal')
plotter.place(x=12, y=70)

window.mainloop()


