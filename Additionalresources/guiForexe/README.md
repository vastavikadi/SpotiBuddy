# 🎧 SpotiBuddy – Voice-Controlled Spotify Assistant

SpotiBuddy lets you control your Spotify music **completely hands-free** using just your voice.  
Like songs, skip tracks, play any song, or manage playlists — no need to touch your device or get distracted.

---

## ✨ Features

| Command Example                   | Action                                      |
|----------------------------------|---------------------------------------------|
| `like this song`                 | ❤️ Like the currently playing song          |
| `next song`                      | ⏭️ Skip to the next track                   |
| `create playlist chill vibes`    | 🆕 Create a new playlist                     |
| `add to playlist chill vibes`    | ➕ Add current song to the playlist          |
| `play shape of you`              | ▶️ Search and play the song on your device  |

---

## 🧠 How It Works

1. Run the app — it will listen for your voice commands.
2. On the first run, it shows a GUI popup to collect your Spotify credentials.
3. It saves them in a `.env` file.
4. You speak, it responds. That simple.

---

## ⚙️ Prerequisites

1. Python 3.8 – 3.12 installed
2. Spotify Developer credentials:
   - Create your app at: https://developer.spotify.com/dashboard
   - Note down:
     - `Client ID`
     - `Client Secret`
     - Set redirect URI to: `http://127.0.0.1:8080`

---

## 📦 Setup (for development)

```bash
git clone https://github.com/<your-username>/SpotiBuddy.git
cd SpotiBuddy
python -m venv .venv
.venv\Scripts\activate  # or source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Build Windows .exe Bundle
# Turn it into a standalone app with one command!

# ✅ 1. Install PyInstaller & Pillow
```bash
pip install pyinstaller pillow
```

## ✅ 2. Build the Executable

```bash
pyinstaller --onefile --windowed --icon=spotibuddy.ico main.py
```
- --onefile = bundle into one .exe
- --windowed = no terminal window popup
- --icon=spotibuddy.ico = uses custom app icon (optional)

# ✅ 3. Output
- You’ll get your executable at:

dist\spotibuddy.exe

- Run it by double-clicking.


### Asks you for credentials through a simple GUI.