import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials (replace these!)
SPOTIPY_CLIENT_ID = '64f1a3c92c884372a01bab5f8d4d6cd5'
SPOTIPY_CLIENT_SECRET = '5ee43cec0e56468fb1134caf9ffa10e2'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

def play_on_spotify(query):
    results = sp.search(q=query, type='track', limit=1)
    tracks = results['tracks']['items']
    if tracks:
        sp.start_playback(uris=[tracks[0]['uri']])
        return f"🎵 Playing on Spotify: {tracks[0]['name']}"
    return "❌ Song not found on Spotify."

def pause_spotify():
    sp.pause_playback()
    return "⏸️ Spotify paused."

def resume_spotify():
    sp.start_playback()
    return "▶️ Spotify resumed."

def next_spotify():
    sp.next_track()
    return "⏭️ Skipped to next track."

def play_on_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    return f"📺 Searching on YouTube: {query}"
