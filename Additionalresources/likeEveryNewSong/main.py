import os
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load .env credentials
load_dotenv()

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-modify user-read-playback-state",
    cache_path=".cache"
))

# Store last song to avoid re-liking
last_liked_id = None

def like_current_song():
    global last_liked_id

    try:
        current = sp.current_playback()
        if current and current.get("is_playing"):
            track = current["item"]
            track_id = track["id"]
            track_name = track["name"]
            artists = ", ".join([a["name"] for a in track["artists"]])

            if track_id != last_liked_id:
                sp.current_user_saved_tracks_add([track_id])
                last_liked_id = track_id
                print(f"✅ Liked: {track_name} by {artists}")
            else:
                print(f"⏩ Already liked: {track_name}")

        else:
            print("🎵 No music playing right now.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

def passive_loop(interval=15):
    print("🌀 Passive auto-like mode started.")
    print("✅ Every 15s, it will auto-like the current song (if new). Press Ctrl+C to stop.\n")

    while True:
        like_current_song()
        time.sleep(interval)

if __name__ == "__main__":
    passive_loop(interval=15)
