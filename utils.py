from concurrent.futures import ThreadPoolExecutor
from downloader import download_track

def download_all_tracks(track_list, max_threads=4):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(download_track, track_list)
