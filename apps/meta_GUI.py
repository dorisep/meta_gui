import os 
from tkinter import *
import csv
import numpy as np
# from more_itertools import unique_everseen
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
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
# import meta_scrape data for plot
def data_list():
    scrape_dict = {
        'scores': [],
        'albumlst': [],
        'artistlst': []
    }
    file_path = os.path.join('..', 'data', 'clean_meta_scrape.csv')
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if int(row['week_num']) == week_num.get():
                scrape_dict['scores'].append(row['meta_score'])
                scrape_dict['albumlst'].append(row['album'])
                scrape_dict['artistlst'].append(row['artist']) 
    return scrape_dict
# import scrape module and set to week_num variable to value in week field
def scrape():
    week_num = int(week_field.get())
    meta_scrape(week_num, year=date_info[0])
# dedup csv file for db
def dedup():
    dedup_meta_scrape(scrape_path, clean_path)
# set plotting function
def plot():
    fig = None
    meta_dict = data_list()
    # print(meta_dict.keys)
    scores = meta_dict['scores']
    # print(datalst)
    albumlst = meta_dict['albumlst']
    # print(albumlst)
    fig = Figure(figsize=(10,10), dpi=100)
    chart = fig.add_subplot(111)
    ind = np.arange(len(datalst))
    chart.bar(ind, scores, 0.8)
    chart.set_ylabel('meta_score')
    chart.set_xlabel('albums')
    chart.set_xticklabels(len(albumlst), rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT)
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

window.mainloop()


