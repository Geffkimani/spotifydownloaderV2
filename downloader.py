import os
import subprocess

def download_track(query, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", filename,
        f"ytsearch1:{query}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)