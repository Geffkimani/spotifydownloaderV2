# spotify_api.py

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import logging
from dotenv import load_dotenv
import os

# Load credentials from .env
load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def extract_playlist_id(url):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None

def get_tracks_from_playlist(playlist_url):
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        logging.error("Invalid Spotify playlist URL.")
        return []

    try:
        results = sp.playlist_items(
            playlist_id,
            additional_types=('track',),  # Essential for real tracks
            limit=100
        )

        tracks = []
        while results:
            for item in results.get("items", []):
                track = item.get("track")
                if track:
                    tracks.append({
                        "name": track.get("name"),
                        "artists": [{"name": artist.get("name")} for artist in track.get("artists", [])],
                    })
            results = sp.next(results) if results.get("next") else None

        logging.info(f"Retrieved {len(tracks)} tracks.")
        return tracks

    except Exception as e:
        logging.error(f"Error fetching playlist: {str(e)}")
        return []
