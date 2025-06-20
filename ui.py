import gradio as gr
from spotify_api import get_tracks_from_playlist
from utils import download_all_tracks

def handle_input(url):
    try:
        tracks = get_tracks_from_playlist(url)
        download_all_tracks(tracks)
        return f"Downloaded {len(tracks)} tracks to your Downloads/music folder!"
    except Exception as e:
        return f"Error: {e}"

demo = gr.Interface(
    fn=handle_input,
    inputs="text",
    outputs="text",
    title="Spotify Playlist Downloader",
    description="Paste a Spotify playlist URL and download songs as MP3."
)

def launch_ui():
    demo.launch()
