import os
import subprocess
import logging
from config import DOWNLOAD_DIR
from decorators import retry

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@retry(attempts=3, delay=2)
def download_track(query: str) -> bool:
    """
    Downloads a single track from YouTube using yt-dlp based on the query string.
    Returns True if the command executed successfully, False otherwise.
    """
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

    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logging.error(f"Download failed for '{query}' with error: {e}")
        return False
