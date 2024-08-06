import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import API_KEY, CLIENT_ID

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=API_KEY)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_album_id(album_name):
    results = sp.search(q='album:' + album_name, type='album')
    items = results['albums']['items']
    if items:
        return items[0]['id']  # Return the first album's ID
    else:
        return None


def get_track_release_date(artist_name, track_name):
    query = f'artist:{artist_name} track:{track_name}'
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        album_id = track['album']['id']
        album = sp.album(album_id)
        release_date = album['release_date']
        return release_date
    else:
        return None

