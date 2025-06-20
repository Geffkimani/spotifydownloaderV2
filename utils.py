import os
import logging
from tqdm import tqdm
from typing import List, Dict
from downloader import download_track
from config import DOWNLOAD_DIR

def show_progress_bar(tracks: List[Dict]):
    for track in tqdm(tracks, desc="Downloading", unit="track"):
        name = f"{track['name']} {track['artists'][0]['name']}"
        try:
            download_track(name)
        except Exception as e:
            logging.error(f"Failed to download {name}: {str(e)}")

def download_all_tracks(tracks: List[Dict]):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    show_progress_bar(tracks)
