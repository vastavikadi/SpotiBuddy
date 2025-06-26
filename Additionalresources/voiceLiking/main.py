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
    scope="user-library-modify user-read-playback-state",
    cache_path=".cache"
))

def like_current_song():
    try:
        current = sp.current_playback()
        if current and current.get("is_playing"):
            track = current["item"]
            track_id = track["id"]
            track_name = track["name"]
            artists = ", ".join([a["name"] for a in track["artists"]])
            sp.current_user_saved_tracks_add([track_id])
            print(f"✅ Liked: {track_name} by {artists}")
        else:
            print("⚠️ No song is playing.")
    except Exception as e:
        print("❌ Error in like_current_song():")
        traceback.print_exc()

def listen_for_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Listening for 'like this song'...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                print("👂 Waiting for voice command...")
                audio = recognizer.listen(source, timeout=10)

            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ Heard: {command}")

            if "like this song" in command:
                print("🎯 Match found! Attempting to like song...")
                like_current_song()
            else:
                print("🔎 No match. Waiting...")

        except sr.UnknownValueError:
            print("🙉 Didn't understand. Try again.")
        except sr.RequestError as e:
            print(f"🌐 API error: {e}")
        except KeyboardInterrupt:
            print("🛑 Exiting.")
            break
        except Exception as e:
            print("❌ General error:")
            traceback.print_exc()

if __name__ == "__main__":
    listen_for_command()