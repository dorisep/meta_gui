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
from playlist_app import get_week_num
from credentials.config import scrape_path, clean_path
from dedup_csv import dedup_meta_scrape


#set instance of tk
window = tk.Tk()
#set title
window.title('Create Playlist from meta_scrape')
#set window size
window.geometry('800x800')
# window.state('zoomed')
# set week_num variable to current week
week_num = IntVar(window, value = get_week_num())
print(f'GUI week_num {week_num}')
# import meta_scrape data for plot
def data_list():
    scrape_dict = {
        'datalst': [],
        'albumlst': [],
        'artistlst': []
    }
    file_path = os.path.join('..', 'data', 'clean_meta_scrape.csv')
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if int(row['week_num']) == week_num.get():
                scrape_dict['datalst'].append(row['meta_score'])
                scrape_dict['albumlst'].append(row['album'])
                scrape_dict['artistlst'].append(row['artist']) 
    return scrape_dict
# import scrape module and set to week_num variable to value in week field
def scrape():
    meta_scrape(week_field.get())
    # print(week_num)
# dedup csv file for db
def dedup():
    dedup_meta_scrape(scrape_path, clean_path)
# set plotting function
def plot():
    meta_dict = data_list()
    datalst = meta_dict['datalst']
    albumlst = meta_dict['albumlst']
    fig = Figure(figsize=(6,6), dpi=100)
    chart = fig.add_subplot(111)
    ind = np.arange(len(datalst))
    chart.bar(ind, datalst, 0.8)
    chart.set_ylabel('meta_score')
    chart.set_xlabel('albums')
    chart.set_xticklabels(albumlst, rotation=45)
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

