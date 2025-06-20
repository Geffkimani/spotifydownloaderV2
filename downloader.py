import os
import subprocess
import logging
from config import DOWNLOAD_DIR
from decorators import retry

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@retry(attempts=3, delay=2)
def download_track(query):
    filename = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--add-metadata",
        "--embed-thumbnail",
        "-o", filename,
        f"ytsearch1:{query}"
    ]
    logging.info(f"Downloading: {query}")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
