import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import speech_recognition as sr
import traceback
import tkinter as tk
from tkinter import simpledialog, messagebox

# 👀 Ask for credentials if .env is missing
def ask_for_credentials_gui():
    root = tk.Tk()
    root.withdraw()  # hide root window

    messagebox.showinfo("SpotiBuddy Setup", "Let's set up your Spotify credentials.")
    
    client_id = simpledialog.askstring("Spotify Client ID", "Enter your SPOTIPY_CLIENT_ID")
    client_secret = simpledialog.askstring("Spotify Client Secret", "Enter your SPOTIPY_CLIENT_SECRET")
    redirect_uri = simpledialog.askstring("Redirect URI", "Enter your SPOTIPY_REDIRECT_URI", initialvalue="http://127.0.0.1:8080")

    if not (client_id and client_secret and redirect_uri):
        messagebox.showerror("Error", "All fields are required. Exiting.")
        exit()

    # Save to .env file
    with open(".env", "w") as f:
        f.write(f"SPOTIPY_CLIENT_ID={client_id}\n")
        f.write(f"SPOTIPY_CLIENT_SECRET={client_secret}\n")
        f.write(f"SPOTIPY_REDIRECT_URI={redirect_uri}\n")

    messagebox.showinfo("Success", "Credentials saved! Please restart the app.")
    exit()

# Load or ask for credentials
if not os.path.exists(".env"):
    ask_for_credentials_gui()

# Load credentials
load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-modify user-read-playback-state playlist-modify-public playlist-modify-private user-modify-playback-state streaming app-remote-control",
    cache_path=".cache"
))

# --- Your existing voice assistant functions below ---

def like_current_song():
    try:
        current = sp.current_playback()
        if current and current.get("is_playing"):
            track = current["item"]
            sp.current_user_saved_tracks_add([track["id"]])
            print(f"✅ Liked: {track['name']} by {', '.join([a['name'] for a in track['artists']])}")
        else:
            print("⚠️ No song is playing.")
    except:
        traceback.print_exc()

def skip_song():
    try:
        sp.next_track()
        print("⏭️ Skipped to next song.")
    except:
        traceback.print_exc()

def create_playlist(name):
    try:
        user_id = sp.me()["id"]
        sp.user_playlist_create(user_id, name)
        print(f"🆕 Playlist created: {name}")
    except:
        traceback.print_exc()

def add_song_to_playlist(name):
    try:
        current = sp.current_playback()
        if not current or not current.get("is_playing"):
            print("⚠️ No song is playing.")
            return

        track_id = current["item"]["id"]
        user_id = sp.me()["id"]
        playlists = sp.current_user_playlists(limit=50)
        
        playlist_id = None
        for playlist in playlists["items"]:
            if playlist["name"].lower() == name.lower():
                playlist_id = playlist["id"]
                break

        if not playlist_id:
            print(f"❌ Playlist '{name}' not found.")
            return

        sp.playlist_add_items(playlist_id, [track_id])
        print(f"🎵 Added to playlist '{name}'")

    except:
        traceback.print_exc()

def search_and_play_song(query):
    try:
        results = sp.search(q=f'track:{query}', type='track', limit=3)
        tracks = results.get('tracks', {}).get('items', [])
        if not tracks:
            print(f"❌ No track found for '{query}'")
            return

        track = tracks[0]
        track_uri = track['uri']
        track_name = track['name']
        artist = track['artists'][0]['name']

        devices = sp.devices()
        if not devices['devices']:
            print("⚠️ No active Spotify device found.")
            return

        device_id = devices['devices'][0]['id']
        sp.start_playback(device_id=device_id, uris=[track_uri])
        print(f"▶️ Now playing: {track_name} by {artist}")
    except:
        traceback.print_exc()

def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎧 SpotiBuddy is listening for commands...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                print("🗣️ Listening...")
                audio = recognizer.listen(source, timeout=10)

            command = recognizer.recognize_google(audio).lower()
            print(f"🔊 Heard: {command}")

            if "like this song" in command:
                like_current_song()
            elif "next song" in command:
                skip_song()
            elif "create playlist" in command:
                name = command.split("create playlist", 1)[1].strip()
                create_playlist(name)
            elif "add to playlist" in command:
                name = command.split("add to playlist", 1)[1].strip()
                add_song_to_playlist(name)
            elif "play" in command:
                name = command.split("play", 1)[1].strip()
                search_and_play_song(name)
            else:
                print("🤔 Unknown command.")
        except sr.UnknownValueError:
            print("🙉 Could not understand. Try again.")
        except KeyboardInterrupt:
            print("🛑 Exiting...")
            break
        except Exception as e:
            print("❌ Error:")
            traceback.print_exc()

if __name__ == "__main__":
    listen_for_commands()