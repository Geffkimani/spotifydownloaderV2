import os
import logging
from tqdm import tqdm
from typing import List, Dict
from downloader import download_track
from config import DOWNLOAD_DIR

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def show_progress_bar(tracks: List[Dict]):
    """
    Show a CLI progress bar for downloading tracks.
    """
    for track in tqdm(tracks, desc="Downloading", unit="track"):
        name = f"{track['name']} {track['artists'][0]['name']}"
        try:
            download_track(name)
        except Exception as e:
            logging.error(f"Failed to download {name}: {str(e)}")

def download_all_tracks(tracks: List[Dict]):
    """
    CLI bulk downloader.
    """
    show_progress_bar(tracks)

def download_track_with_status(name: str) -> bool:
    """
    Used by the web UI to show download status for each track.
    Returns True if successful, False otherwise.
    """
    try:
        download_track(name)
        logging.info(f"Downloaded: {name}")
        return True
    except Exception as e:
        logging.error(f"Error downloading {name}: {str(e)}")
        return False
