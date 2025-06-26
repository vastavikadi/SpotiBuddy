import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
import traceback

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-modify user-read-playback-state playlist-modify-public playlist-modify-private user-modify-playback-state streaming app-remote-control",
    cache_path=".cache"
))

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

def create_playlist(playlist_name):
    try:
        user_id = sp.me()['id']
        sp.user_playlist_create(user_id, playlist_name)
        print(f"🆕 Created playlist: {playlist_name}")
    except:
        traceback.print_exc()

def add_song_to_playlist(playlist_name):
    try:
        current = sp.current_playback()
        if not current or not current.get("is_playing"):
            print("⚠️ No song is playing.")
            return

        track_id = current["item"]["id"]
        user_id = sp.me()['id']
        playlists = sp.current_user_playlists(limit=50)
        
        playlist_id = None
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_id = playlist['id']
                break
        
        if not playlist_id:
            print(f"❌ Playlist '{playlist_name}' not found.")
            return
        
        sp.playlist_add_items(playlist_id, [track_id])
        print(f"🎵 Added to playlist '{playlist_name}'")

    except:
        traceback.print_exc()
        
def search_and_play_song(query):
    try:
        results = sp.search(q=query, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])
        if not tracks:
            print(f"❌ No track found for '{query}'")
            return

        track_uri = tracks[0]['uri']
        track_name = tracks[0]['name']
        artist = tracks[0]['artists'][0]['name']

        devices = sp.devices()
        if not devices['devices']:
            print("⚠️ No active Spotify device found. Please start playing from a device first.")
            return

        device_id = devices['devices'][0]['id']

        sp.start_playback(device_id=device_id, uris=[track_uri])
        print(f"▶️ Now playing: {track_name} by {artist}")

    except Exception as e:
        print("❌ Error in search_and_play_song:")
        traceback.print_exc()

def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Voice control ready. Say:")
    print("- 'like this song'")
    print("- 'next song'")
    print("- 'create playlist [name]'")
    print("- 'add to playlist [name]'")
    print("- 'play [song_name] by [artist_name]'")#not very good because of the web api search returns from spotify

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                print("🎧 Listening...")
                audio = recognizer.listen(source, timeout=10)

            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ Heard: {command}")

            if "like this song" in command:
                like_current_song()
            elif "next song" in command:
                skip_song()
            elif "create playlist" in command:
                playlist_name = command.split("create playlist", 1)[1].strip()
                if playlist_name:
                    create_playlist(playlist_name)
            elif "add to playlist" in command:
                playlist_name = command.split("add to playlist", 1)[1].strip()
                if playlist_name:
                    add_song_to_playlist(playlist_name)
            elif "play" in command:
                song_name = command.split("play", 1)[1].strip()
                if song_name:
                    search_and_play_song(song_name)
            else:
                print("🤔 Command not recognized.")

        except sr.UnknownValueError:
            print("🙉 Could not understand. Try again.")
        except sr.RequestError as e:
            print(f"🌐 API error: {e}")
        except KeyboardInterrupt:
            print("🛑 Stopped by user.")
            break
        except Exception as e:
            print("❌ Error:")
            traceback.print_exc()

if __name__ == "__main__":
    listen_for_commands()