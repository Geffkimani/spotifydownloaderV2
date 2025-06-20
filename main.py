from spotify_api import get_tracks_from_playlist
from utils import download_all_tracks
from ui import launch_ui
import logging
from config import LOG_FILE
import os

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    mode = input("Type 'cli' for terminal or 'web' for web UI: ").strip().lower()
    if mode == "cli":
        url = input("Enter Spotify Playlist URL: ").strip()
        tracks = get_tracks_from_playlist(url)
        print(f"Found {len(tracks)} tracks. Downloading...")
        download_all_tracks(tracks)
    elif mode == "web":
        launch_ui()
    else:
        print("Invalid mode.")

