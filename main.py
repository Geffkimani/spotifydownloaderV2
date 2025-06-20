from spotify_api import get_tracks_from_playlist
from utils import download_all_tracks

if __name__ == "__main__":
    playlist_url = input("Enter Spotify Playlist URL: ")
    print("Fetching track list...")
    tracks = get_tracks_from_playlist(playlist_url)
    print(f"Found {len(tracks)} tracks. Starting download...")
    download_all_tracks(tracks)
    print("Done.")

