from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
API_KEY = os.getenv('SPOTIFY_CLIENT_SECRET')