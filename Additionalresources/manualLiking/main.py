import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pynput import keyboard

# Load secrets from .env
load_dotenv()

# Setup Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-modify user-read-playback-state",
    cache_path=".cache"  # Store token locally
))

def like_current_song():
    current = sp.current_playback()
    if current and current.get("is_playing"):
        track = current["item"]
        track_id = track["id"]
        track_name = track["name"]
        artists = ", ".join([a["name"] for a in track["artists"]])
        sp.current_user_saved_tracks_add([track_id])
        print(f"❤️ Liked: {track_name} by {artists}")
    else:
        print("No song is currently playing.")

# Listen for Ctrl+Alt+L
def on_press(key):
    if key == keyboard.KeyCode.from_char('l') and any([ctrl_pressed, alt_pressed]):
        like_current_song()

ctrl_pressed = False
alt_pressed = False

def on_key_down(key):
    global ctrl_pressed, alt_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True
    elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = True
    elif key == keyboard.KeyCode.from_char('l'):
        if ctrl_pressed and alt_pressed:
            like_current_song()

def on_key_up(key):
    global ctrl_pressed, alt_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False
    elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = False

# Start listening
print("🎵 Spotify Auto-Liker running. Press Ctrl+Alt+L to like the current song.")
with keyboard.Listener(on_press=on_key_down, on_release=on_key_up) as listener:
    listener.join()
