# Meta_GUI
A graphical interface that coordinates an app to scrape metacritic website for new music for each week, generates dynamically labelled csv files and an app that populates a playlist in my spotify account by using the Spotify API.
## Overview
---
I enjoyed working on this project as an exercise in broadening my foundation in python and app developement overall. I look forward to honing my skills through as I continue its developement.

## Background
---
As a music enthusiast, I am always exploring new music. 

While many streaming services have playlists and access to new releasses, I grew tired of feeling bound to algorithyms and coallating my own playlists. 

What I really wanted was a raw dump of albums into a list that I could listen to and select from regardless of my listening history or derived preferences. 

That led to the aformentioned applications. Which also grew as I decided to flesh out my understanding of python and development overall. 

In this project I used the spotify developer api doucmentation 

I created apps prior to developing this gui. 

Metacritic scrapping apps:
- An [app](https://github.com/dorisep/meta_gui/blob/main/apps/scrape.py) to track albums released each week.

- An [app](https://github.com/dorisep/meta_gui/blob/main/apps/historical_scrape.py) that collects the archived releases from all previous years.

Spotify playlist generation app:
- An interface for the Spoitfy [api](https://github.com/dorisep/meta_gui/blob/main/apps/playlist_app.py) that creates a playlist on my account.

Tkinter app:
- A [grahical user interface](https://github.com/dorisep/meta_gui/blob/main/apps/meta_GUI.py) that tracks the current week and runs the scaping function and playlist generation.

## Credentials
The config file requires the following credentials to run the applications in this repository

Spotify app credentials:
spotify_pass = 
spotify_user_id =

Spotify developer credentials:
client_id =
client_secret = 
redirect_uri = 
playlist_token = 
refresh_token=


 
