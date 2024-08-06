import requests
import json
from config import API_KEY, CLIENT_ID
import datetime
import time


def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    auth_response_data = auth_response.json()
    return auth_response_data['access_token']


def search_track(access_token, artist_name, track_name):
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q': f'artist:{artist_name} track:{track_name}',
        'type': 'track',
        'limit': 1,
    }

    search_response = requests.get(search_url, headers=headers, params=params)
    if search_response.status_code == 200:
        search_results = search_response.json()
        if search_results['tracks']['items']:
            return search_results['tracks']['items'][0]
        else:
            return None
    elif search_response.status_code == 429:
        retry_after = search_response.headers['retry-after']
        print(f'''Rate limited. Retrying after {retry_after} seconds. 
                    Estimated retry time: {datetime.datetime.now() + datetime.timedelta(seconds=int(retry_after))}''')
        time.sleep(int(retry_after))
    else:
        print(f'Error: {search_response.status_code}')
        return None


def get_track_details(access_token, track_id):
    track_url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    track_response = requests.get(track_url, headers=headers)
    if track_response.status_code == 200:
        return track_response.json()
    elif track_response.status_code == 429:
        retry_after = track_response.headers['retry-after']
        print(
            f'''Rate limited. Retrying after {retry_after} seconds. 
            Estimated retry time: {datetime.datetime.now() + datetime.timedelta(seconds=int(retry_after))}''')
        time.sleep(int(retry_after))

