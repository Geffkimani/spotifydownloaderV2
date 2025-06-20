import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import logging
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


def extract_playlist_id(url):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None


def get_tracks_from_playlist(playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_items(
        playlist_id,
        additional_types=('track',),  # important fix
        limit=100
    )
    if not playlist_id:
        raise ValueError("Invalid Spotify URL.")

    tracks = []
    while results:
        for item in results["items"]:
            track = item["track"]
            if track is not None:
                tracks.append({
                    "name": track["name"],
                    "artists": [{"name": artist["name"]} for artist in track["artists"]],
                })
        if results['next']:
            results = sp.next(results)
        else:
            break
    logging.info(f"Retrieved {len(tracks)} tracks.")
    return tracks
