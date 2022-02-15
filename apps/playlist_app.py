import requests
import os
import base64
import csv
import json
import re
import datetime
from spotify_client import *
from credentials.config import *



def refresh_accesss_token():
    client_creds = f'{client_id}:{client_secret}'
    client_creds_b64 = base64.b64encode(client_creds.encode())
    refresh_token_header = {
        'Authorization' : f'Basic {client_creds_b64.decode()}'
    }
    # def refresh_playlist_token():
    refresh_url =  'https://accounts.spotify.com/api/token'
    refresh_params = {
        'grant_type': 'refresh_token',
        'refresh_token': f'{refresh_token}'    
    }
    r_token = requests.post(refresh_url, data=refresh_params, headers=refresh_token_header)
    refresh_response = r_token.json()
    access_token = refresh_response['access_token']
    return access_token


playlist_token = refresh_accesss_token()
csv_path = os.path.join('..', 'data', 'meta_scrape.csv')
###
# imported get_date_info into tkinter as a default entry in for the scrape button
# left here in case using the scrape without the gui
###
def get_date_info():    
    my_date = datetime.date.today() 
    year, week_num, day_of_week = my_date.isocalendar()
    date_info = (year, week_num)
    return date_info

def get_track_features(track_uris):

    playlist_token = refresh_accesss_token()
    track_ids = [track[14:] for track in track_uris]
    track_limit = 100 
    # using list comprehension 
    batched_tracks = [track_ids[i * track_limit:(i + 1) * track_limit] for i in range((len(track_ids) + track_limit - 1) // track_limit)]  
#     url = f'https://api.spotify.com/v1/audio-features?ids='
#     =7ouMYWpwJ422jRcDASZB7P%2C4VqPOruhp5EdPBeR92t6lQ%2C2takcwOaAZWiXQijPHIx7B'
    for batch in batched_tracks:
        request_data =  "%2C".join(batch)
        
        url = f'https://api.spotify.com/v1/audio-features?ids={request_data}'
        response = requests.get(
            url,
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {playlist_token}'
            })
 
        b = response.json()


def get_album_tracks(album_ids):
    track_uris = []
#     request_data = json.dumps(uris)
    for album_id in album_ids:
        query = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
        response = requests.get(
            query,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {playlist_token}'
            })
        response_json = response.json()
        tracks = response_json['items']
        for track in tracks:
            track_uris.append(track['uri'])
    return track_uris

def search_for_albums(week_num, csv_path):

    artists=[]
    albums=[]
    meta_score=[]
    user_score=[]

    albums_not_found = {'artist': [], 'album': []}
    album_ids = set()
    

#     read in weekly metaScrape csv 

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            
#         filter for artists and albums from current week
            if int(row['week_num'])== week_num:

                artists.append(row['artist'])
                albums.append(row['album'])
                meta_score.append(row['meta_score'])
                user_score.append(row['user_score'])
#   initialize spotify client
 
    spotify = SpotifyAPI(client_id, client_secret)
    for al, ar in zip(albums, artists):
#       trim album names of suffixes (e.g. .vol 1, [ep] etc.)
        al_trim = re.split(',|\[', al)
#       search for album ids 
        temp = spotify.search({"album":al_trim[0]}, search_type="album")
        try:
            parse_album_ids = (temp["albums"]["items"][0]["id"])
#   create dicitonary for albums not found
        except:
            albums_not_found['artist'].append(ar)
            albums_not_found['album'].append(al) 
        album_ids.add(parse_album_ids)
#   create log of albums_not_found
    return(get_album_tracks(album_ids))

def add_tracks_to_playlist(week_num, playlist_id):
    track_uris = [track for track in search_for_albums(week_num, csv_path)]
 
    track_limit = 100 
    # using list comprehension 
    batched_tracks = [track_uris[i * track_limit:(i + 1) * track_limit] for i in range((len(track_uris) + track_limit - 1) // track_limit)]  
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    for batch in batched_tracks:
        request_data = json.dumps(batch)

        requests.post(
            url,
            data=request_data,
            headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {playlist_token}'
            })
    return

def create_playlist(week_num):
    date_info =  get_date_info()
    year = date_info[0]
    
    request_body = json.dumps({
        'name': f'{year}-week {week_num} scrape',
        'description': f'metacritic rated albums for the {week_num}th of the year',
        'public': True
    })
    url = f'https://api.spotify.com/v1/users/{spotify_user_id}/playlists'


    response = requests.post(
        url,
        data = request_body,
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {playlist_token}'

    })
    response_json = response.json()
    playlist_id = (response_json['id'])
    # code here for traking playlists by writing playlist ids to file
    add_tracks_to_playlist(week_num, playlist_id)
