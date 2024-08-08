import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import CLIENT_ID, API_KEY
from api_calls import get_artist_images
import pandas as pd
import json

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=API_KEY)
sp = spotipy.Spotify(auth_manager=auth_manager)

df = pd.read_json('track_data_file0.json', lines=True)
artists = df.groupby('artistName').size().reset_index(name='count').sort_values('count', ascending=False)
artists = artists[(artists['count'] > 10)]
artists = artists.artistName.to_list()

output = []
for artist in artists:
    artist_data = sp.search(q=artist, type='artist', market='PL')['artists']['items'][0]
    id = artist_data['id']
    uri = artist_data['uri']
    url = artist_data['external_urls']['spotify']
    genres = artist_data['genres']
    images = artist_data['images']
    followers = artist_data['followers']['total']
    
    output.append({"artist_name" : artist,
                   "artist_id" : id,
                   'artist_genres' : genres,
                   'images' : images,
                   'followers' : followers,
                   'uri' : uri,
                   'url' : url})

with open('artist_db.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False)