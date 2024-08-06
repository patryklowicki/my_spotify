from api_calls import get_access_token, get_track_details, search_track
import json
from pathlib import Path
import pandas as pd
from config import CLIENT_ID, API_KEY
import time

cwd = Path.cwd()
json_path = cwd.parent.parent / "spotify_data" / "StreamingHistory_music_0.json"

with open(json_path, encoding='utf-8') as f:
    data = json.load(f, )

access_token = get_access_token(client_id=CLIENT_ID, client_secret=API_KEY)

counter = 0
for row in data:
    print(row)
    if row['msPlayed'] > 30000:
        track_data = search_track(access_token=access_token,
                                artist_name=row['artistName'],
                                track_name=row['trackName'])
        try:
            row['track_id'] = track_data['id']
            row['popularity'] = track_data['popularity']
            row['duration_ms'] = track_data['duration_ms']
            row['album'] = track_data['album']['name']
            row['release_date'] = track_data['album']['release_date']
            row['album_id'] = track_data['album']['id']
        except TypeError:
            print(f"Error with {row['artistName']} - {row['trackName']}")
            pass
        counter += 1
        print(counter)
        if counter % 29 == 0:
            time.sleep(1)
    
with open('track_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)